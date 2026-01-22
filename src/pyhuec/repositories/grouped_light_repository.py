"""
Grouped Light Repository for Hue API v2 operations.
"""

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
    """Repository for Grouped Light data access operations."""

    def __init__(self, http_client: HttpClient):
        """
        Initialize the repository.

        Args:
            http_client: HTTP client for API requests
        """
        self._client = http_client

    async def get_grouped_light(self, grouped_light_id: str) -> GroupedLightResponseDTO:
        """
        Retrieve a single grouped light by ID.

        Args:
            grouped_light_id: UUID of the grouped light

        Returns:
            GroupedLightResponseDTO with grouped light details
        """
        response = await self._client.get(
            f"/clip/v2/resource/grouped_light/{grouped_light_id}"
        )
        return GroupedLightResponseDTO(**response)

    async def get_grouped_lights(self) -> GroupedLightListResponseDTO:
        """
        Retrieve all grouped lights.

        Returns:
            GroupedLightListResponseDTO with list of all grouped lights
        """
        response = await self._client.get("/clip/v2/resource/grouped_light")
        return GroupedLightListResponseDTO(**response)

    async def update_grouped_light(
        self, grouped_light_id: str, update: GroupedLightUpdateDTO
    ) -> GroupedLightUpdateResponseDTO:
        """
        Update a grouped light's state (affects all lights in the group).

        Args:
            grouped_light_id: UUID of the grouped light
            update: GroupedLightUpdateDTO with desired changes

        Returns:
            GroupedLightUpdateResponseDTO with confirmation
        """
        response = await self._client.put(
            f"/clip/v2/resource/grouped_light/{grouped_light_id}",
            data=update.model_dump(exclude_none=True),
        )
        return GroupedLightUpdateResponseDTO(**response)

    async def identify_grouped_light(
        self, grouped_light_id: str, identify: GroupedLightIdentifyDTO
    ) -> GroupedLightUpdateResponseDTO:
        """
        Flash all lights in a grouped light for identification.

        Args:
            grouped_light_id: UUID of the grouped light
            identify: GroupedLightIdentifyDTO with identify action

        Returns:
            GroupedLightUpdateResponseDTO with confirmation
        """
        response = await self._client.put(
            f"/clip/v2/resource/grouped_light/{grouped_light_id}",
            data=identify.model_dump(exclude_none=True),
        )
        return GroupedLightUpdateResponseDTO(**response)
