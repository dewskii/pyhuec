from pyhuec.models import (
    BridgeConfigDTO,
    BridgeRepositoryProtocol,
    BridgeResponseDTO,
    HttpClientProtocol,
    ResourceCollectionDTO,
    ResourceDTO,
)


class BridgeRepository(BridgeRepositoryProtocol):
    """Bridge data access operations."""

    def __init__(self, http_client: HttpClientProtocol):
        """Initialize repository.

        Args:
            http_client: HTTP client for API requests
        """
        self.http_client = http_client

    async def get_bridge_info(self) -> BridgeResponseDTO:
        """Get bridge information.

        Returns:
            Bridge information
        """
        response = await self.http_client.get("/resource/bridge")
        return BridgeResponseDTO(**response)

    async def get_bridge_config(self) -> BridgeConfigDTO:
        """Get bridge configuration.

        Returns:
            Bridge configuration
        """
        response = await self.http_client.get("/config")
        return BridgeConfigDTO(**response)

    async def get_all_resources(self) -> ResourceCollectionDTO:
        """Get all resources.

        Returns:
            All resources
        """
        response = await self.http_client.get("/resource")
        return ResourceCollectionDTO(**response)

    async def get_resource(self, resource_type: str, resource_id: str) -> ResourceDTO:
        """Get specific resource.

        Args:
            resource_type: Resource type
            resource_id: Resource UUID

        Returns:
            Resource details
        """
        response = await self.http_client.get(
            f"/resource/{resource_type}/{resource_id}"
        )
        return ResourceDTO(**response)
