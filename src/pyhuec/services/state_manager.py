"""
State manager for synchronizing REST API state with SSE stream updates.
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from pyhuec.models.dto.event_dto import (
    EventType,
    InternalEventDTO,
    ResourceType,
)
from pyhuec.models.dto.grouped_light_dto import GroupedLightResponseDTO
from pyhuec.models.dto.light_dto import LightResponseDTO
from pyhuec.models.dto.room_dto import RoomResponseDTO
from pyhuec.models.dto.scene_dto import SceneResponseDTO

logger = logging.getLogger(__name__)


class StateManager:
    """
    Manages local state cache synchronized with Hue Bridge.

    Provides immediate state access from cache while keeping it updated
    via SSE stream. Falls back to REST API when cache is stale or empty.
    """

    def __init__(self):
        """Initialize the state manager."""
        self._lights: Dict[str, LightResponseDTO] = {}
        self._grouped_lights: Dict[str, GroupedLightResponseDTO] = {}
        self._rooms: Dict[str, RoomResponseDTO] = {}
        self._scenes: Dict[str, SceneResponseDTO] = {}
        self._last_update: Dict[str, datetime] = {}
        self._initialized = False

    def get_light(self, light_id: str) -> Optional[LightResponseDTO]:
        """Get cached light state."""
        return self._lights.get(light_id)

    def get_all_lights(self) -> Dict[str, LightResponseDTO]:
        """Get all cached lights."""
        return self._lights.copy()

    def get_grouped_light(self, group_id: str) -> Optional[GroupedLightResponseDTO]:
        """Get cached grouped light state."""
        return self._grouped_lights.get(group_id)

    def get_room(self, room_id: str) -> Optional[RoomResponseDTO]:
        """Get cached room state."""
        return self._rooms.get(room_id)

    def get_all_rooms(self) -> Dict[str, RoomResponseDTO]:
        """Get all cached rooms."""
        return self._rooms.copy()

    def get_scene(self, scene_id: str) -> Optional[SceneResponseDTO]:
        """Get cached scene state."""
        return self._scenes.get(scene_id)

    def update_from_rest(
        self,
        resource_type: ResourceType,
        resource_id: str,
        data: Any,
    ) -> None:
        """
        Update cache from REST API response.

        Args:
            resource_type: Type of resource
            resource_id: Resource UUID
            data: Resource data DTO
        """
        if resource_type == ResourceType.LIGHT:
            self._lights[resource_id] = data
        elif resource_type == ResourceType.GROUPED_LIGHT:
            self._grouped_lights[resource_id] = data
        elif resource_type == ResourceType.ROOM:
            self._rooms[resource_id] = data
        elif resource_type == ResourceType.SCENE:
            self._scenes[resource_id] = data

        self._last_update[resource_id] = datetime.now()
        logger.debug(f"Updated {resource_type} {resource_id} from REST API")

    def update_from_event(self, event: InternalEventDTO) -> None:
        """
        Update cache from SSE stream.

        Args:
            event: Internal SSE with resource changes
        """
        resource_id = event.resource_id
        resource_type = event.resource_type

        if event.event_type == EventType.DELETE:
            self._handle_delete(resource_type, resource_id)
            return

        if event.event_type in (EventType.UPDATE, EventType.ADD):
            self._handle_update(event)
            return

    def _handle_update(self, event: InternalEventDTO) -> None:
        """Handle update/add events by patching cached state."""
        resource_id = event.resource_id
        resource_type = event.resource_type

        current = None
        if resource_type == ResourceType.LIGHT:
            current = self._lights.get(resource_id)
        elif resource_type == ResourceType.GROUPED_LIGHT:
            current = self._grouped_lights.get(resource_id)
        elif resource_type == ResourceType.ROOM:
            current = self._rooms.get(resource_id)
        elif resource_type == ResourceType.SCENE:
            current = self._scenes.get(resource_id)

        if not current:
            logger.debug(
                f"Resource {resource_type} {resource_id} not in cache, "
                "will fetch on next access"
            )
            return

        self._patch_state(current, event)
        self._last_update[resource_id] = event.timestamp
        logger.debug(f"Updated {resource_type} {resource_id} from event")

    def _patch_state(self, current_state: Any, event: InternalEventDTO) -> None:
        """
        Patch current state with SSE data.

        Args:
            current_state: Current cached DTO
            event: SSE with updated data
        """

        if event.data.on is not None:
            if hasattr(current_state, "on"):
                current_state.on = event.data.on

        if event.data.dimming is not None:
            if hasattr(current_state, "dimming"):
                current_state.dimming = event.data.dimming

    def _handle_delete(self, resource_type: ResourceType, resource_id: str) -> None:
        """Handle delete events by removing from cache."""
        if resource_type == ResourceType.LIGHT:
            self._lights.pop(resource_id, None)
        elif resource_type == ResourceType.GROUPED_LIGHT:
            self._grouped_lights.pop(resource_id, None)
        elif resource_type == ResourceType.ROOM:
            self._rooms.pop(resource_id, None)
        elif resource_type == ResourceType.SCENE:
            self._scenes.pop(resource_id, None)

        self._last_update.pop(resource_id, None)
        logger.info(f"Removed {resource_type} {resource_id} from cache")

    def clear(self) -> None:
        """Clear all cached state."""
        self._lights.clear()
        self._grouped_lights.clear()
        self._rooms.clear()
        self._scenes.clear()
        self._last_update.clear()
        self._initialized = False
        logger.info("Cleared state cache")

    def is_initialized(self) -> bool:
        """Check if state has been initialized."""
        return self._initialized

    def mark_initialized(self) -> None:
        """Mark state as initialized."""
        self._initialized = True

    def get_last_update(self, resource_id: str) -> Optional[datetime]:
        """Get timestamp of last update for a resource."""
        return self._last_update.get(resource_id)
