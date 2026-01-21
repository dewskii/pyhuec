"""
Protocol definitions for Bridge operations.
These protocols define the interface contracts for bridge management and configuration.
"""

from typing import Dict, List, Optional, Protocol
from pyhuec.models.dto import (
    BridgeResponseDTO,
    BridgeConfigDTO,
    ResourceDTO,
    ResourceCollectionDTO,
    EventDTO,
)


class BridgeRepositoryProtocol(Protocol):
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


class BridgeServiceProtocol(Protocol):
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


class BridgeEventStreamProtocol(Protocol):
    """Protocol for Bridge event streaming operations."""
    
    async def subscribe_to_events(self) -> None:
        """
        Subscribe to server-sent events from the bridge.
        """
        ...
    
    async def unsubscribe_from_events(self) -> None:
        """
        Unsubscribe from server-sent events.
        """
        ...
    
    async def get_event_stream(self) -> List[EventDTO]:
        """
        Get stream of events from the bridge.
        
        Returns:
            List of EventDTO representing changes
        """
        ...
    
    def is_subscribed(self) -> bool:
        """
        Check if currently subscribed to events.
        
        Returns:
            True if subscribed
        """
        ...


class BridgeControllerProtocol(Protocol):
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
