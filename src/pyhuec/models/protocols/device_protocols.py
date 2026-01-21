"""
Protocol definitions for Device operations.
These protocols define the interface contracts for device repositories and services.
"""

from typing import List, Protocol
from pyhuec.models.dto import (
    DeviceResponseDTO,
    DeviceUpdateDTO,
    DeviceIdentifyDTO,
    DeviceListResponseDTO,
    DeviceUpdateResponseDTO,
    DeviceDeleteResponseDTO,
    ResourceIdentifierDTO,
)


class DeviceRepositoryProtocol(Protocol):
    """Protocol for Device data access operations."""
    
    async def get_device(self, device_id: str) -> DeviceResponseDTO:
        """
        Retrieve a single device by ID.
        
        Args:
            device_id: UUID of the device
            
        Returns:
            DeviceResponseDTO with device details
        """
        ...
    
    async def get_devices(self) -> DeviceListResponseDTO:
        """
        Retrieve all devices.
        
        Returns:
            DeviceListResponseDTO with list of all devices
        """
        ...
    
    async def update_device(
        self, 
        device_id: str, 
        update: DeviceUpdateDTO
    ) -> DeviceUpdateResponseDTO:
        """
        Update a device's configuration.
        
        Args:
            device_id: UUID of the device
            update: DeviceUpdateDTO with desired changes
            
        Returns:
            DeviceUpdateResponseDTO with confirmation
        """
        ...
    
    async def identify_device(
        self, 
        device_id: str, 
        identify: DeviceIdentifyDTO
    ) -> DeviceUpdateResponseDTO:
        """
        Identify a device (flash/signal).
        
        Args:
            device_id: UUID of the device
            identify: DeviceIdentifyDTO with identify action
            
        Returns:
            DeviceUpdateResponseDTO with confirmation
        """
        ...
    
    async def delete_device(self, device_id: str) -> DeviceDeleteResponseDTO:
        """
        Delete a device.
        
        Args:
            device_id: UUID of the device
            
        Returns:
            DeviceDeleteResponseDTO with confirmation
        """
        ...


class DeviceServiceProtocol(Protocol):
    """Protocol for Device business logic operations."""
    
    async def get_device_info(self, device_id: str) -> DeviceResponseDTO:
        """
        Get detailed device information.
        
        Args:
            device_id: UUID of the device
            
        Returns:
            DeviceResponseDTO with complete device details
        """
        ...
    
    async def list_devices(self) -> List[DeviceResponseDTO]:
        """
        List all available devices.
        
        Returns:
            List of DeviceResponseDTO
        """
        ...
    
    async def rename_device(self, device_id: str, name: str) -> bool:
        """
        Rename a device.
        
        Args:
            device_id: UUID of the device
            name: New device name
            
        Returns:
            True if successful
        """
        ...
    
    async def set_device_archetype(
        self, 
        device_id: str, 
        archetype: str
    ) -> bool:
        """
        Update device archetype.
        
        Args:
            device_id: UUID of the device
            archetype: New archetype (classic_bulb, spot_bulb, etc.)
            
        Returns:
            True if successful
        """
        ...
    
    async def identify_device(self, device_id: str) -> bool:
        """
        Flash/signal a device for identification.
        
        Args:
            device_id: UUID of the device
            
        Returns:
            True if successful
        """
        ...
    
    async def get_device_services(
        self, 
        device_id: str
    ) -> List[ResourceIdentifierDTO]:
        """
        Get all services provided by a device.
        
        Args:
            device_id: UUID of the device
            
        Returns:
            List of service resource identifiers
        """
        ...
    
    async def enable_user_test_mode(self, device_id: str) -> bool:
        """
        Enable user test mode for device.
        
        Args:
            device_id: UUID of the device
            
        Returns:
            True if successful
        """
        ...
    
    async def disable_user_test_mode(self, device_id: str) -> bool:
        """
        Disable user test mode for device.
        
        Args:
            device_id: UUID of the device
            
        Returns:
            True if successful
        """
        ...
    
    async def delete_device(self, device_id: str) -> bool:
        """
        Delete a device.
        
        Args:
            device_id: UUID of the device
            
        Returns:
            True if successful
        """
        ...


class DeviceControllerProtocol(Protocol):
    """Protocol for Device controller operations (API endpoint handlers)."""
    
    async def handle_get_device(self, device_id: str) -> DeviceResponseDTO:
        """Handle GET /device/{id} request."""
        ...
    
    async def handle_get_devices(self) -> DeviceListResponseDTO:
        """Handle GET /device request."""
        ...
    
    async def handle_update_device(
        self, 
        device_id: str, 
        update: DeviceUpdateDTO
    ) -> DeviceUpdateResponseDTO:
        """Handle PUT /device/{id} request."""
        ...
    
    async def handle_identify_device(
        self, 
        device_id: str
    ) -> DeviceUpdateResponseDTO:
        """Handle PUT /device/{id}/identify request."""
        ...
    
    async def handle_delete_device(
        self, 
        device_id: str
    ) -> DeviceDeleteResponseDTO:
        """Handle DELETE /device/{id} request."""
        ...
