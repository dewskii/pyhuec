from typing import List, Optional
from pyhuec.models.dto.light_dto import LightResponseDTO
from pyhuec.models.protocols.light_protocol import LightServiceProtocol


class LightService(LightServiceProtocol):
    """Protocol for Light business logic operations."""
    
    async def turn_on(self, light_id: str, brightness: Optional[float] = None) -> bool:
        """
        Turn on a light with optional brightness.
        
        Args:
            light_id: UUID of the light
            brightness: Optional brightness level (0.0-100.0)
            
        Returns:
            True if successful
        """
        ...
    
    async def turn_off(self, light_id: str) -> bool:
        """
        Turn off a light.
        
        Args:
            light_id: UUID of the light
            
        Returns:
            True if successful
        """
        ...
    
    async def set_brightness(self, light_id: str, brightness: float) -> bool:
        """
        Set light brightness.
        
        Args:
            light_id: UUID of the light
            brightness: Brightness level (0.0-100.0)
            
        Returns:
            True if successful
        """
        ...
    
    async def set_color_xy(self, light_id: str, x: float, y: float) -> bool:
        """
        Set light color using CIE XY coordinates.
        
        Args:
            light_id: UUID of the light
            x: X coordinate (0.0-1.0)
            y: Y coordinate (0.0-1.0)
            
        Returns:
            True if successful
        """
        ...
    
    async def set_color_temperature(self, light_id: str, mirek: int) -> bool:
        """
        Set light color temperature.
        
        Args:
            light_id: UUID of the light
            mirek: Color temperature in mirek (153-500)
            
        Returns:
            True if successful
        """
        ...
    
    async def set_effect(self, light_id: str, effect: str) -> bool:
        """
        Apply an effect to the light.
        
        Args:
            light_id: UUID of the light
            effect: Effect name (prism, opal, fire, etc.)
            
        Returns:
            True if successful
        """
        ...
    
    async def flash(self, light_id: str) -> bool:
        """
        Flash a light (breathe alert).
        
        Args:
            light_id: UUID of the light
            
        Returns:
            True if successful
        """
        ...
    
    async def get_light_info(self, light_id: str) -> LightResponseDTO:
        """
        Get detailed light information.
        
        Args:
            light_id: UUID of the light
            
        Returns:
            LightResponseDTO with complete light details
        """
        ...
    
    async def list_lights(self) -> List[LightResponseDTO]:
        """
        List all available lights.
        
        Returns:
            List of LightResponseDTO
        """
        ...
