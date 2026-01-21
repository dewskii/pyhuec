from pyhuec.models.dto.light_dto import (
    LightListResponseDTO,
    LightResponseDTO,
    LightUpdateDTO,
    LightUpdateResponseDTO,
)
from pyhuec.models.protocols import LightControllerProtocol


class LightController(LightControllerProtocol):
    """Protocol for Light controller operations (API endpoint handlers)."""

    async def handle_get_light(self, light_id: str) -> LightResponseDTO:
        """Handle GET /light/{id} request."""
        ...

    async def handle_get_lights(self) -> LightListResponseDTO:
        """Handle GET /light request."""
        ...

    async def handle_update_light(
        self, light_id: str, update: LightUpdateDTO
    ) -> LightUpdateResponseDTO:
        """Handle PUT /light/{id} request."""
        ...

    async def handle_identify_light(self, light_id: str) -> LightUpdateResponseDTO:
        """Handle PUT /light/{id}/identify request."""
        ...
