
from pyhuec.infrastructure import BridgeConfigDTO, BridgeResponseDTO, ResourceCollectionDTO, ResourceDTO
from pyhuec.infrastructure import BridgeRepositoryProtocol


class BridgeRepository(BridgeRepositoryProtocol):
    """Protocol for Bridge data access operations."""
    
    async def get_bridge_info(self) -> BridgeResponseDTO:
        """
        Retrieve bridge information.
        
        Returns:
            BridgeResponseDTO with bridge details
        """
        ...
    
    async def get_bridge_config(self) -> BridgeConfigDTO:
        """
        Retrieve bridge configuration.
        
        Returns:
            BridgeConfigDTO with configuration details
        """
        ...
    
    async def get_all_resources(self) -> ResourceCollectionDTO:
        """
        Retrieve all resources from the bridge.
        
        Returns:
            ResourceCollectionDTO with all resources
        """
        ...
    
    async def get_resource(self, resource_type: str, resource_id: str) -> ResourceDTO:
        """
        Retrieve a specific resource by type and ID.
        
        Args:
            resource_type: Type of resource (light, room, scene, etc.)
            resource_id: UUID of the resource
            
        Returns:
            ResourceDTO with resource details
        """
        ...