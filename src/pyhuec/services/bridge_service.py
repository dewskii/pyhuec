from pyhuec.models.dto import BridgeResponseDTO, ResourceCollectionDTO, ResourceDTO
from pyhuec.models.protocols import BridgeRepositoryProtocol, BridgeServiceProtocol


class BridgeService(BridgeServiceProtocol):
    """Service for Bridge business logic operations."""

    def __init__(self, bridge_repository: BridgeRepositoryProtocol):
        """
        Initialize service with bridge repository.

        Args:
            bridge_repository: Repository for bridge data access
        """
        self.bridge_repository = bridge_repository
        self._connected = False
        self._authenticated = False
        self._app_key: str | None = None

    async def connect(self) -> bool:
        """
        Establish connection to the bridge.

        Returns:
            True if connection successful
        """
        try:
            
            await self.bridge_repository.get_bridge_info()
            self._connected = True
            return True
        except Exception:
            self._connected = False
            return False

    async def disconnect(self) -> bool:
        """
        Disconnect from the bridge.

        Returns:
            True if disconnection successful
        """
        self._connected = False
        self._authenticated = False
        self._app_key = None
        return True

    async def authenticate(self, app_key: str) -> bool:
        """
        Authenticate with the bridge using an app key.

        Args:
            app_key: Application key for authentication

        Returns:
            True if authentication successful
        """
        try:
            
            self._app_key = app_key
            await self.bridge_repository.get_bridge_config()
            self._authenticated = True
            return True
        except Exception:
            self._authenticated = False
            self._app_key = None
            return False

    async def register_application(self, app_name: str) -> str:
        """
        Register a new application with the bridge.

        Args:
            app_name: Name of the application

        Returns:
            Generated application key

        Raises:
            NotImplementedError: Registration requires special bridge endpoint
        """
        raise NotImplementedError(
            "Application registration requires pressing the bridge button and "
            "using the /api endpoint, which should be handled at the transport level"
        )

    async def get_bridge_info(self) -> BridgeResponseDTO:
        """
        Get detailed bridge information.

        Returns:
            BridgeResponseDTO with complete bridge details
        """
        return await self.bridge_repository.get_bridge_info()

    async def discover_resources(self) -> ResourceCollectionDTO:
        """
        Discover all available resources on the bridge.

        Returns:
            ResourceCollectionDTO with all discovered resources
        """
        return await self.bridge_repository.get_all_resources()

    async def get_resource(self, resource_type: str, resource_id: str) -> ResourceDTO:
        """
        Get a specific resource by type and ID.

        Args:
            resource_type: Type of resource (light, room, scene, etc.)
            resource_id: UUID of the resource

        Returns:
            ResourceDTO with resource details
        """
        return await self.bridge_repository.get_resource(resource_type, resource_id)

    async def is_connected(self) -> bool:
        """
        Check if connected to the bridge.

        Returns:
            True if connected
        """
        return self._connected

    async def get_api_version(self) -> str:
        """
        Get the API version of the bridge.

        Returns:
            API version string
        """
        bridge_info = await self.bridge_repository.get_bridge_info()
        
        
        return getattr(bridge_info, "api_version", "unknown")

    async def get_software_version(self) -> str:
        """
        Get the software version of the bridge.

        Returns:
            Software version string
        """
        bridge_info = await self.bridge_repository.get_bridge_info()
        
        return getattr(bridge_info, "software_version", "unknown")
