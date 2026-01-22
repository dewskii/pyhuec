from pyhuec.models.dto import BridgeResponseDTO, ResourceCollectionDTO, ResourceDTO
from pyhuec.models.protocols import BridgeControllerProtocol, BridgeServiceProtocol


class BridgeController(BridgeControllerProtocol):
    """Bridge request handler."""

    def __init__(self, bridge_service: BridgeServiceProtocol):
        """Initialize controller.

        Args:
            bridge_service: Bridge service
        """
        self.bridge_service = bridge_service

    async def handle_get_bridge_info(self) -> BridgeResponseDTO:
        """Handle GET /resource/bridge.

        Returns:
            Bridge information
        """
        return await self.bridge_service.get_bridge_info()

    async def handle_get_resources(self) -> ResourceCollectionDTO:
        """Handle GET /resource.

        Returns:
            All resources
        """
        return await self.bridge_service.discover_resources()

    async def handle_get_resource(
        self, resource_type: str, resource_id: str
    ) -> ResourceDTO:
        """Handle GET /resource/{type}/{id}.

        Args:
            resource_type: Resource type
            resource_id: Resource UUID

        Returns:
            Resource details
        """
        return await self.bridge_service.get_resource(resource_type, resource_id)
