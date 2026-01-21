from pyhuec.models import BridgeControllerProtocol
from pyhuec.models.dto import BridgeResponseDTO, ResourceCollectionDTO, ResourceDTO


class BridgeController(BridgeControllerProtocol):
    """Protocol for Bridge controller operations."""
    
    async def handle_get_bridge_info(self) -> BridgeResponseDTO:
        """Handle GET /resource/bridge request."""
        ...
    
    async def handle_get_resources(self) -> ResourceCollectionDTO:
        """Handle GET /resource request."""
        ...
    
    async def handle_get_resource(
        self, 
        resource_type: str, 
        resource_id: str
    ) -> ResourceDTO:
        """Handle GET /resource/{type}/{id} request."""
        ...
