from pyhuec.models import (
    BridgeConfigDTO,
    BridgeRepositoryProtocol,
    BridgeResponseDTO,
    HttpClientProtocol,
    ResourceCollectionDTO,
    ResourceDTO,
)


class BridgeRepository(BridgeRepositoryProtocol):
    """Repository for Bridge data access operations using HTTP transport."""

    def __init__(self, http_client: HttpClientProtocol):
        """
        Initialize repository with HTTP client.

        Args:
            http_client: HTTP client for making API requests
        """
        self.http_client = http_client

    async def get_bridge_info(self) -> BridgeResponseDTO:
        """
        Retrieve bridge information.

        Returns:
            BridgeResponseDTO with bridge details
        """
        response = await self.http_client.get("/resource/bridge")
        return BridgeResponseDTO(**response)

    async def get_bridge_config(self) -> BridgeConfigDTO:
        """
        Retrieve bridge configuration.

        Returns:
            BridgeConfigDTO with configuration details
        """
        response = await self.http_client.get("/config")
        return BridgeConfigDTO(**response)

    async def get_all_resources(self) -> ResourceCollectionDTO:
        """
        Retrieve all resources from the bridge.

        Returns:
            ResourceCollectionDTO with all resources
        """
        response = await self.http_client.get("/resource")
        return ResourceCollectionDTO(**response)

    async def get_resource(self, resource_type: str, resource_id: str) -> ResourceDTO:
        """
        Retrieve a specific resource by type and ID.

        Args:
            resource_type: Type of resource (light, room, scene, etc.)
            resource_id: UUID of the resource

        Returns:
            ResourceDTO with resource details
        """
        response = await self.http_client.get(f"/resource/{resource_type}/{resource_id}")
        return ResourceDTO(**response)
