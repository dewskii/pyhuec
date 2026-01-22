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
    """Light data access."""

    def __init__(self, http_client: HttpClient):
        """Initialize repository.

        Args:
            http_client: HTTP client
        """
        self._client = http_client

    async def get_light(self, light_id: str) -> LightResponseDTO:
        """Get light by ID.

        Args:
            light_id: Light UUID

        Returns:
            Light details
        """
        response = await self._client.get(f"/clip/v2/resource/light/{light_id}")
        return LightResponseDTO(**response["data"][0])

    async def get_lights(self) -> LightListResponseDTO:
        """Get all lights.

        Returns:
            All lights
        """
        response = await self._client.get("/clip/v2/resource/light")
        return LightListResponseDTO(**response)

    async def update_light(
        self, light_id: str, update: LightUpdateDTO
    ) -> LightUpdateResponseDTO:
        """Update light state.

        Args:
            light_id: Light UUID
            update: Light update

        Returns:
            Update confirmation
        """
        response = await self._client.put(
            f"/clip/v2/resource/light/{light_id}",
            body=update.model_dump(exclude_none=True),
        )
        return LightUpdateResponseDTO(**response)

    async def identify_light(self, light_id: str) -> LightUpdateResponseDTO:
        """Flash light for identification.

        Args:
            light_id: Light UUID

        Returns:
            Update confirmation
        """
        identify = LightIdentifyDTO(action="identify")
        response = await self._client.put(
            f"/clip/v2/resource/light/{light_id}",
            body=identify.model_dump(exclude_none=True),
        )
        return LightUpdateResponseDTO(**response)
