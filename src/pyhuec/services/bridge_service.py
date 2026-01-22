from pyhuec.models.dto import BridgeResponseDTO, ResourceCollectionDTO, ResourceDTO
from pyhuec.models.protocols import BridgeRepositoryProtocol, BridgeServiceProtocol


class BridgeService(BridgeServiceProtocol):
    """Bridge business logic."""

    def __init__(self, bridge_repository: BridgeRepositoryProtocol):
        """Initialize service.

        Args:
            bridge_repository: Bridge repository
        """
        self.bridge_repository = bridge_repository
        self._connected = False
        self._authenticated = False
        self._app_key: str | None = None

    async def connect(self) -> bool:
        """Connect to bridge.

        Returns:
            True if successful
        """
        try:
            
            await self.bridge_repository.get_bridge_info()
            self._connected = True
            return True
        except Exception:
            self._connected = False
            return False

    async def disconnect(self) -> bool:
        """Disconnect from bridge.

        Returns:
            True if successful
        """
        self._connected = False
        self._authenticated = False
        self._app_key = None
        return True

    async def authenticate(self, app_key: str) -> bool:
        """Authenticate with bridge.

        Args:
            app_key: Application key

        Returns:
            True if successful
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
        """Register application.

        Args:
            app_name: Application name

        Returns:
            Application key

        Raises:
            NotImplementedError: Not implemented
        """
        raise NotImplementedError(
            "Application registration requires pressing the bridge button and "
            "using the /api endpoint, which should be handled at the transport level"
        )

    async def get_bridge_info(self) -> BridgeResponseDTO:
        """Get bridge information.

        Returns:
            Bridge information
        """
        return await self.bridge_repository.get_bridge_info()

    async def discover_resources(self) -> ResourceCollectionDTO:
        """Discover all resources.

        Returns:
            All resources
        """
        return await self.bridge_repository.get_all_resources()

    async def get_resource(self, resource_type: str, resource_id: str) -> ResourceDTO:
        """Get resource.

        Args:
            resource_type: Resource type
            resource_id: Resource UUID

        Returns:
            Resource details
        """
        return await self.bridge_repository.get_resource(resource_type, resource_id)

    async def is_connected(self) -> bool:
        """Check connection status.

        Returns:
            True if connected
        """
        return self._connected

    async def get_api_version(self) -> str:
        """Get API version.

        Returns:
            API version
        """
        bridge_info = await self.bridge_repository.get_bridge_info()
        return getattr(bridge_info, "api_version", "unknown")

    async def get_software_version(self) -> str:
        """Get software version.

        Returns:
            Software version
        """
        bridge_info = await self.bridge_repository.get_bridge_info()
        return getattr(bridge_info, "software_version", "unknown")
