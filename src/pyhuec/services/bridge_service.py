from pyhuec.models import BridgeResponseDTO, ResourceCollectionDTO
from pyhuec.models import BridgeServiceProtocol


class BridgeService(BridgeServiceProtocol):
    """Protocol for Bridge business logic operations."""
    
    async def connect(self) -> bool:
        """
        Establish connection to the bridge.
        
        Returns:
            True if connection successful
        """
        ...
    
    async def disconnect(self) -> bool:
        """
        Disconnect from the bridge.
        
        Returns:
            True if disconnection successful
        """
        ...
    
    async def authenticate(self, app_key: str) -> bool:
        """
        Authenticate with the bridge using an app key.
        
        Args:
            app_key: Application key for authentication
            
        Returns:
            True if authentication successful
        """
        ...
    
    async def register_application(self, app_name: str) -> str:
        """
        Register a new application with the bridge.
        
        Args:
            app_name: Name of the application
            
        Returns:
            Generated application key
        """
        ...
    
    async def get_bridge_info(self) -> BridgeResponseDTO:
        """
        Get detailed bridge information.
        
        Returns:
            BridgeResponseDTO with complete bridge details
        """
        ...
    
    async def discover_resources(self) -> ResourceCollectionDTO:
        """
        Discover all available resources on the bridge.
        
        Returns:
            ResourceCollectionDTO with all discovered resources
        """
        ...
    
    async def is_connected(self) -> bool:
        """
        Check if connected to the bridge.
        
        Returns:
            True if connected
        """
        ...
    
    async def get_api_version(self) -> str:
        """
        Get the API version of the bridge.
        
        Returns:
            API version string
        """
        ...
    
    async def get_software_version(self) -> str:
        """
        Get the software version of the bridge.
        
        Returns:
            Software version string
        """
        ...