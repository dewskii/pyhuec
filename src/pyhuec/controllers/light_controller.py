from pyhuec.models.dto.light_dto import (
    LightListResponseDTO,
    LightResponseDTO,
    LightUpdateDTO,
    LightUpdateResponseDTO,
)
from pyhuec.models.protocols import LightControllerProtocol, LightRepositoryProtocol


class LightController(LightControllerProtocol):
    """Light controller for handling API endpoint requests."""

    def __init__(self, light_repository: LightRepositoryProtocol) -> None:
        """
        Initialize light controller.
        
        Args:
            light_repository: Repository for light data access
        """
        self._light_repository = light_repository

    async def handle_get_light(self, light_id: str) -> LightResponseDTO:
        """
        Handle GET /light/{id} request.
        
        Args:
            light_id: UUID of the light
            
        Returns:
            Light details
        """
        return await self._light_repository.get_light(light_id)

    async def handle_get_lights(self) -> LightListResponseDTO:
        """
        Handle GET /light request.
        
        Returns:
            List of all lights
        """
        return await self._light_repository.get_lights()

    async def handle_update_light(
        self, light_id: str, update: LightUpdateDTO
    ) -> LightUpdateResponseDTO:
        """
        Handle PUT /light/{id} request.
        
        Args:
            light_id: UUID of the light
            update: Light update data
            
        Returns:
            Update response
        """
        return await self._light_repository.update_light(light_id, update)

    async def handle_identify_light(self, light_id: str) -> LightUpdateResponseDTO:
        """
        Handle PUT /light/{id}/identify request.
        
        Args:
            light_id: UUID of the light
            
        Returns:
            Update response
        """
        return await self._light_repository.identify_light(light_id)
