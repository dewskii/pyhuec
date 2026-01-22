from pyhuec.models.dto import BridgeResponseDTO, ResourceCollectionDTO, ResourceDTO
from pyhuec.models.protocols import BridgeControllerProtocol, BridgeServiceProtocol


class BridgeController(BridgeControllerProtocol):
    """Controller for Bridge operations, coordinating HTTP requests to service layer."""

    def __init__(self, bridge_service: BridgeServiceProtocol):
        """
        Initialize controller with bridge service.

        Args:
            bridge_service: Service for bridge business logic
        """
        self.bridge_service = bridge_service

    async def handle_get_bridge_info(self) -> BridgeResponseDTO:
        """
        Handle GET /resource/bridge request.

        Returns:
            BridgeResponseDTO with bridge information
        """
        return await self.bridge_service.get_bridge_info()

    async def handle_get_resources(self) -> ResourceCollectionDTO:
        """
        Handle GET /resource request.

        Returns:
            ResourceCollectionDTO with all resources
        """
        return await self.bridge_service.discover_resources()

    async def handle_get_resource(
        self, resource_type: str, resource_id: str
    ) -> ResourceDTO:
        """
        Handle GET /resource/{type}/{id} request.

        Args:
            resource_type: Type of resource (light, room, scene, etc.)
            resource_id: UUID of the resource

        Returns:
            ResourceDTO with resource details
        """
        return await self.bridge_service.get_resource(resource_type, resource_id)
