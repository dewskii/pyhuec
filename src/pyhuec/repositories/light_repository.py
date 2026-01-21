from pyhuec.models.dto.light_dto import (
    LightIdentifyDTO,
    LightListResponseDTO,
    LightResponseDTO,
    LightUpdateDTO,
    LightUpdateResponseDTO,
)
from pyhuec.models.protocols import LightRepositoryProtocol


class LightRepository(LightRepositoryProtocol):
    """Protocol for Light data access operations."""

    async def get_light(self, light_id: str) -> LightResponseDTO:
        """
        Retrieve a single light by ID.

        Args:
            light_id: UUID of the light

        Returns:
            LightResponseDTO with light details
        """
        ...

    async def get_lights(self) -> LightListResponseDTO:
        """
        Retrieve all lights.

        Returns:
            LightListResponseDTO with list of all lights
        """
        ...

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
        ...

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
        ...
