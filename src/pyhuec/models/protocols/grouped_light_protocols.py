"""
Protocol definitions for Grouped Light operations.
These protocols define the interface contracts for grouped light repositories and services.
"""

from typing import List, Optional, Protocol
from pyhuec.models.dto import (
    GroupedLightResponseDTO,
    GroupedLightUpdateDTO,
    GroupedLightIdentifyDTO,
    GroupedLightListResponseDTO,
    GroupedLightUpdateResponseDTO,
)


class GroupedLightRepositoryProtocol(Protocol):
    """Protocol for Grouped Light data access operations."""
    
    async def get_grouped_light(self, grouped_light_id: str) -> GroupedLightResponseDTO:
        """
        Retrieve a single grouped light by ID.
        
        Args:
            grouped_light_id: UUID of the grouped light
            
        Returns:
            GroupedLightResponseDTO with grouped light details
        """
        ...
    
    async def get_grouped_lights(self) -> GroupedLightListResponseDTO:
        """
        Retrieve all grouped lights.
        
        Returns:
            GroupedLightListResponseDTO with list of all grouped lights
        """
        ...
    
    async def update_grouped_light(
        self, 
        grouped_light_id: str, 
        update: GroupedLightUpdateDTO
    ) -> GroupedLightUpdateResponseDTO:
        """
        Update a grouped light's state (affects all lights in the group).
        
        Args:
            grouped_light_id: UUID of the grouped light
            update: GroupedLightUpdateDTO with desired changes
            
        Returns:
            GroupedLightUpdateResponseDTO with confirmation
        """
        ...
    
    async def identify_grouped_light(
        self, 
        grouped_light_id: str, 
        identify: GroupedLightIdentifyDTO
    ) -> GroupedLightUpdateResponseDTO:
        """
        Flash all lights in a grouped light for identification.
        
        Args:
            grouped_light_id: UUID of the grouped light
            identify: GroupedLightIdentifyDTO with identify action
            
        Returns:
            GroupedLightUpdateResponseDTO with confirmation
        """
        ...


class GroupedLightServiceProtocol(Protocol):
    """Protocol for Grouped Light business logic operations."""
    
    async def turn_on_group(
        self, 
        grouped_light_id: str, 
        brightness: Optional[float] = None
    ) -> bool:
        """
        Turn on all lights in a group.
        
        Args:
            grouped_light_id: UUID of the grouped light
            brightness: Optional brightness level (0.0-100.0)
            
        Returns:
            True if successful
        """
        ...
    
    async def turn_off_group(self, grouped_light_id: str) -> bool:
        """
        Turn off all lights in a group.
        
        Args:
            grouped_light_id: UUID of the grouped light
            
        Returns:
            True if successful
        """
        ...
    
    async def set_group_brightness(
        self, 
        grouped_light_id: str, 
        brightness: float
    ) -> bool:
        """
        Set brightness for all lights in a group.
        
        Args:
            grouped_light_id: UUID of the grouped light
            brightness: Brightness level (0.0-100.0)
            
        Returns:
            True if successful
        """
        ...
    
    async def set_group_color_xy(
        self, 
        grouped_light_id: str, 
        x: float, 
        y: float
    ) -> bool:
        """
        Set color for all lights in a group using CIE XY coordinates.
        
        Args:
            grouped_light_id: UUID of the grouped light
            x: X coordinate (0.0-1.0)
            y: Y coordinate (0.0-1.0)
            
        Returns:
            True if successful
        """
        ...
    
    async def set_group_color_temperature(
        self, 
        grouped_light_id: str, 
        mirek: int
    ) -> bool:
        """
        Set color temperature for all lights in a group.
        
        Args:
            grouped_light_id: UUID of the grouped light
            mirek: Color temperature in mirek (153-500)
            
        Returns:
            True if successful
        """
        ...
    
    async def flash_group(self, grouped_light_id: str) -> bool:
        """
        Flash all lights in a group (breathe alert).
        
        Args:
            grouped_light_id: UUID of the grouped light
            
        Returns:
            True if successful
        """
        ...
    
    async def get_grouped_light_info(
        self, 
        grouped_light_id: str
    ) -> GroupedLightResponseDTO:
        """
        Get detailed grouped light information.
        
        Args:
            grouped_light_id: UUID of the grouped light
            
        Returns:
            GroupedLightResponseDTO with complete grouped light details
        """
        ...
    
    async def list_grouped_lights(self) -> List[GroupedLightResponseDTO]:
        """
        List all available grouped lights.
        
        Returns:
            List of GroupedLightResponseDTO
        """
        ...
    
    async def get_group_state(self, grouped_light_id: str) -> dict:
        """
        Get aggregated state of all lights in the group.
        
        Args:
            grouped_light_id: UUID of the grouped light
            
        Returns:
            Dictionary with aggregated on/off, brightness, color, etc.
        """
        ...


class GroupedLightControllerProtocol(Protocol):
    """Protocol for Grouped Light controller operations (API endpoint handlers)."""
    
    async def handle_get_grouped_light(
        self, 
        grouped_light_id: str
    ) -> GroupedLightResponseDTO:
        """Handle GET /grouped_light/{id} request."""
        ...
    
    async def handle_get_grouped_lights(self) -> GroupedLightListResponseDTO:
        """Handle GET /grouped_light request."""
        ...
    
    async def handle_update_grouped_light(
        self, 
        grouped_light_id: str, 
        update: GroupedLightUpdateDTO
    ) -> GroupedLightUpdateResponseDTO:
        """Handle PUT /grouped_light/{id} request."""
        ...
    
    async def handle_identify_grouped_light(
        self, 
        grouped_light_id: str
    ) -> GroupedLightUpdateResponseDTO:
        """Handle PUT /grouped_light/{id}/identify request."""
        ...
