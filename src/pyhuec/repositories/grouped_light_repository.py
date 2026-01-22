"""Grouped Light Repository."""

from pyhuec.models.dto.grouped_light_dto import (
    GroupedLightIdentifyDTO,
    GroupedLightListResponseDTO,
    GroupedLightResponseDTO,
    GroupedLightUpdateDTO,
    GroupedLightUpdateResponseDTO,
)
from pyhuec.models.protocols import GroupedLightRepositoryProtocol
from pyhuec.transport.http_client import HttpClient


class GroupedLightRepository(GroupedLightRepositoryProtocol):
    """Grouped light data access."""

    def __init__(self, http_client: HttpClient):
        """Initialize repository.

        Args:
            http_client: HTTP client
        """
        self._client = http_client

    async def get_grouped_light(self, grouped_light_id: str) -> GroupedLightResponseDTO:
        """Get grouped light by ID.

        Args:
            grouped_light_id: Grouped light UUID

        Returns:
            Grouped light details
        """
        response = await self._client.get(
            f"/clip/v2/resource/grouped_light/{grouped_light_id}"
        )
        return GroupedLightResponseDTO(**response)

    async def get_grouped_lights(self) -> GroupedLightListResponseDTO:
        """Get all grouped lights.

        Returns:
            All grouped lights
        """
        response = await self._client.get("/clip/v2/resource/grouped_light")
        return GroupedLightListResponseDTO(**response)

    async def update_grouped_light(
        self, grouped_light_id: str, update: GroupedLightUpdateDTO
    ) -> GroupedLightUpdateResponseDTO:
        """Update grouped light state.

        Args:
            grouped_light_id: Grouped light UUID
            update: Grouped light update

        Returns:
            Update confirmation
        """
        response = await self._client.put(
            f"/clip/v2/resource/grouped_light/{grouped_light_id}",
            data=update.model_dump(exclude_none=True),
        )
        return GroupedLightUpdateResponseDTO(**response)

    async def identify_grouped_light(
        self, grouped_light_id: str, identify: GroupedLightIdentifyDTO
    ) -> GroupedLightUpdateResponseDTO:
        """Flash grouped light for identification.

        Args:
            grouped_light_id: Grouped light UUID
            identify: Identify action

        Returns:
            Update confirmation
        """
        response = await self._client.put(
            f"/clip/v2/resource/grouped_light/{grouped_light_id}",
            data=identify.model_dump(exclude_none=True),
        )
        return GroupedLightUpdateResponseDTO(**response)
