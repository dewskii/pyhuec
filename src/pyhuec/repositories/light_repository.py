from pyhuec.models.dto.light_dto import (
    LightIdentifyDTO,
    LightListResponseDTO,
    LightResponseDTO,
    LightUpdateDTO,
    LightUpdateResponseDTO,
)
from pyhuec.models.protocols import LightRepositoryProtocol
from pyhuec.transport.http_client import HttpClient


class LightRepository(LightRepositoryProtocol):
    """Repository for Light data access operations."""

    def __init__(self, http_client: HttpClient):
        """Initialize the repository with an HTTP client."""
        self._client = http_client

    async def get_light(self, light_id: str) -> LightResponseDTO:
        """
        Retrieve a single light by ID.

        Args:
            light_id: UUID of the light

        Returns:
            LightResponseDTO with light details
        """
        response = await self._client.get(f"/clip/v2/resource/light/{light_id}")
        return LightResponseDTO(**response)

    async def get_lights(self) -> LightListResponseDTO:
        """
        Retrieve all lights.

        Returns:
            LightListResponseDTO with list of all lights
        """
        response = await self._client.get("/clip/v2/resource/light")
        return LightListResponseDTO(**response)

    async def update_light(
        self, light_id: str, update: LightUpdateDTO
    ) -> LightUpdateResponseDTO:
        """
        Update a light's state.

        Args:
            light_id: UUID of the light
            update: LightUpdateDTO with desired changes

        Returns:
            LightUpdateResponseDTO with confirmation
        """
        response = await self._client.put(
            f"/clip/v2/resource/light/{light_id}",
            data=update.model_dump(exclude_none=True)
        )
        return LightUpdateResponseDTO(**response)

    async def identify_light(
        self, light_id: str, identify: LightIdentifyDTO
    ) -> LightUpdateResponseDTO:
        """
        Flash a light for identification.

        Args:
            light_id: UUID of the light
            identify: LightIdentifyDTO with identify action

        Returns:
            LightUpdateResponseDTO with confirmation
        """
        response = await self._client.put(
            f"/clip/v2/resource/light/{light_id}",
            data=identify.model_dump(exclude_none=True)
        )
        return LightUpdateResponseDTO(**response)
