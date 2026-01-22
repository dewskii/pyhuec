"""
Unified Hue Client providing both REST API and event stream capabilities.

This is the main entry point for interacting with the Hue Bridge, combining:
- REST API operations via repositories
- Real-time event stream via event service
- Local state caching via state manager
"""

import logging
from typing import Callable, List, Optional

from pyhuec.models.dto.event_dto import (
    EventFilterDTO,
    InternalEventDTO,
    ResourceType,
)
from pyhuec.models.dto.light_dto import (
    LightListResponseDTO,
    LightResponseDTO,
    LightUpdateDTO,
)
from pyhuec.models.dto.room_dto import RoomListResponseDTO, RoomResponseDTO
from pyhuec.models.dto.scene_dto import SceneListResponseDTO, SceneResponseDTO
from pyhuec.models.protocols.event_protocols import EventServiceProtocol
from pyhuec.models.protocols.grouped_light_protocols import (
    GroupedLightRepositoryProtocol,
)
from pyhuec.models.protocols.light_protocols import LightRepositoryProtocol
from pyhuec.models.protocols.room_protocols import RoomRepositoryProtocol
from pyhuec.models.protocols.scene_protocols import SceneRepositoryProtocol
from pyhuec.services.state_manager import StateManager

logger = logging.getLogger(__name__)


class HueClient:
    """
    Unified client for Hue Bridge interaction.

    Provides:
    - REST API operations (lights, rooms, scenes, etc.)
    - Real-time event streaming
    - Automatic state synchronization
    - Local state caching

    Usage:

        client = HueClient(
            light_repository=light_repo,
            event_service=event_service,

        )


        await client.start_event_stream()


        await client.subscribe_to_light_events(my_handler)


        lights = await client.get_lights()
        await client.turn_on_light(light_id, brightness=75.0)


        cached_light = client.get_cached_light(light_id)
    """

    def __init__(
        self,
        light_repository: LightRepositoryProtocol,
        grouped_light_repository: GroupedLightRepositoryProtocol,
        room_repository: RoomRepositoryProtocol,
        scene_repository: SceneRepositoryProtocol,
        event_service: EventServiceProtocol,
        enable_state_cache: bool = True,
        auto_sync_on_command: bool = True,
    ):
        """
        Initialize the Hue client.

        Args:
            light_repository: Light data access
            grouped_light_repository: Grouped light data access
            room_repository: Room data access
            scene_repository: Scene data access
            event_service: Event stream service
            enable_state_cache: Enable local state caching
            auto_sync_on_command: Auto-refresh cache after commands
        """

        self._light_repo = light_repository
        self._grouped_light_repo = grouped_light_repository
        self._room_repo = room_repository
        self._scene_repo = scene_repository

        self._event_service = event_service
        self._event_subscription_id: Optional[str] = None

        self._state_manager = StateManager() if enable_state_cache else None
        self._auto_sync = auto_sync_on_command

    async def start_event_stream(self) -> None:
        """
        Start listening to the Hue Bridge event stream.

        This enables real-time state updates and keeps the local cache
        synchronized automatically. Recommended for best experience.
        """
        logger.info("Starting Hue client event stream")
        await self._event_service.start_event_stream()

        if self._state_manager:
            self._event_subscription_id = await self._event_service.subscribe_to_events(
                handler=self._handle_internal_event,
                event_filter=None,
            )
            logger.info("Subscribed to events for state synchronization")

    async def stop_event_stream(self) -> None:
        """Stop the event stream and cleanup resources."""
        logger.info("Stopping Hue client event stream")

        if self._event_subscription_id:
            await self._event_service.unsubscribe_from_events(
                self._event_subscription_id
            )
            self._event_subscription_id = None

        await self._event_service.stop_event_stream()

    def is_streaming(self) -> bool:
        """Check if currently streaming events."""
        return self._event_service.is_streaming()

    async def initialize_cache(self) -> None:
        """
        Initialize local state cache with current bridge state.

        This fetches all resources via REST API and populates the cache.
        Recommended to call once during startup.
        """
        if not self._state_manager:
            logger.warning("State cache is disabled")
            return

        logger.info("Initializing state cache from bridge")

        lights_response = await self._light_repo.get_lights()
        for light in lights_response.data:
            self._state_manager.update_from_rest(ResourceType.LIGHT, light.id, light)

        rooms_response = await self._room_repo.get_rooms()
        for room in rooms_response.data:
            self._state_manager.update_from_rest(ResourceType.ROOM, room.id, room)

        scenes_response = await self._scene_repo.get_scenes()
        for scene in scenes_response.data:
            self._state_manager.update_from_rest(ResourceType.SCENE, scene.id, scene)

        self._state_manager.mark_initialized()
        logger.info("State cache initialized")

    def _handle_internal_event(self, event: InternalEventDTO) -> None:
        """Internal handler for state synchronization."""
        if self._state_manager:
            self._state_manager.update_from_event(event)

    async def get_lights(self) -> LightListResponseDTO:
        """Get all lights from bridge (REST API)."""
        response = await self._light_repo.get_lights()

        if self._state_manager:
            for light in response.data:
                self._state_manager.update_from_rest(
                    ResourceType.LIGHT, light.id, light
                )

        return response

    async def get_light(self, light_id: str) -> LightResponseDTO:
        """Get specific light from bridge (REST API)."""
        response = await self._light_repo.get_light(light_id)

        if self._state_manager:
            self._state_manager.update_from_rest(
                ResourceType.LIGHT, light_id, response.data[0]
            )

        return response

    async def update_light(self, light_id: str, update: LightUpdateDTO) -> None:
        """Update light state (REST API)."""
        await self._light_repo.update_light(light_id, update)

        if self._auto_sync and self._state_manager:
            await self.get_light(light_id)

    async def turn_on_light(
        self, light_id: str, brightness: Optional[float] = None
    ) -> None:
        """
        Turn on a light with optional brightness.

        Args:
            light_id: Light UUID
            brightness: Optional brightness (0-100)
        """
        update = LightUpdateDTO(on={"on": True})
        if brightness is not None:
            update.dimming = {"brightness": brightness}

        await self.update_light(light_id, update)

    async def turn_off_light(self, light_id: str) -> None:
        """Turn off a light."""
        update = LightUpdateDTO(on={"on": False})
        await self.update_light(light_id, update)

    def get_cached_light(self, light_id: str) -> Optional[LightResponseDTO]:
        """
        Get light from local cache (instant, no network).

        Returns None if not cached or cache disabled.
        """
        if not self._state_manager:
            return None
        return self._state_manager.get_light(light_id)

    def get_all_cached_lights(self) -> List[LightResponseDTO]:
        """Get all cached lights."""
        if not self._state_manager:
            return []
        return list(self._state_manager.get_all_lights().values())

    async def get_rooms(self) -> RoomListResponseDTO:
        """Get all rooms from bridge (REST API)."""
        response = await self._room_repo.get_rooms()

        if self._state_manager:
            for room in response.data:
                self._state_manager.update_from_rest(ResourceType.ROOM, room.id, room)

        return response

    async def get_room(self, room_id: str) -> RoomResponseDTO:
        """Get specific room from bridge (REST API)."""
        response = await self._room_repo.get_room(room_id)

        if self._state_manager:
            self._state_manager.update_from_rest(
                ResourceType.ROOM, room_id, response.data[0]
            )

        return response

    def get_cached_room(self, room_id: str) -> Optional[RoomResponseDTO]:
        """Get room from local cache."""
        if not self._state_manager:
            return None
        return self._state_manager.get_room(room_id)

    async def get_scenes(self) -> SceneListResponseDTO:
        """Get all scenes from bridge (REST API)."""
        response = await self._scene_repo.get_scenes()

        if self._state_manager:
            for scene in response.data:
                self._state_manager.update_from_rest(
                    ResourceType.SCENE, scene.id, scene
                )

        return response

    async def activate_scene(self, scene_id: str) -> None:
        """Activate a scene."""
        await self._scene_repo.update_scene(scene_id, {"recall": {"action": "active"}})

    async def subscribe_to_light_events(
        self, handler: Callable[[InternalEventDTO], None]
    ) -> str:
        """
        Subscribe to light events only.

        Args:
            handler: Callback function for light events

        Returns:
            Subscription ID for later unsubscription
        """
        event_filter = EventFilterDTO(
            resource_types=[ResourceType.LIGHT],
        )
        return await self._event_service.subscribe_to_events(handler, event_filter)

    async def subscribe_to_room_events(
        self, handler: Callable[[InternalEventDTO], None]
    ) -> str:
        """Subscribe to room events only."""
        event_filter = EventFilterDTO(
            resource_types=[ResourceType.ROOM],
        )
        return await self._event_service.subscribe_to_events(handler, event_filter)

    async def subscribe_to_all_events(
        self, handler: Callable[[InternalEventDTO], None]
    ) -> str:
        """Subscribe to all events."""
        return await self._event_service.subscribe_to_events(handler, None)

    async def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from events."""
        return await self._event_service.unsubscribe_from_events(subscription_id)

    def clear_cache(self) -> None:
        """Clear the local state cache."""
        if self._state_manager:
            self._state_manager.clear()

    def is_cache_initialized(self) -> bool:
        """Check if cache has been initialized."""
        if not self._state_manager:
            return False
        return self._state_manager.is_initialized()
