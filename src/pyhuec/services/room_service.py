from typing import List
from pyhuec.models.dto.room_dto import ResourceIdentifierDTO, RoomResponseDTO
from pyhuec.models.protocols.room_protocol import RoomServiceProtocol


class RoomService(RoomServiceProtocol):
    """Protocol for Room business logic operations."""
    
    async def create_room(
        self, 
        name: str, 
        archetype: str, 
        children: List[ResourceIdentifierDTO]
    ) -> str:
        """
        Create a new room with lights.
        
        Args:
            name: Room name
            archetype: Room type (living_room, bedroom, etc.)
            children: List of lights/devices to include
            
        Returns:
            UUID of created room
        """
        ...
    
    async def add_light_to_room(
        self, 
        room_id: str, 
        light_id: str
    ) -> bool:
        """
        Add a light to a room.
        
        Args:
            room_id: UUID of the room
            light_id: UUID of the light
            
        Returns:
            True if successful
        """
        ...
    
    async def remove_light_from_room(
        self, 
        room_id: str, 
        light_id: str
    ) -> bool:
        """
        Remove a light from a room.
        
        Args:
            room_id: UUID of the room
            light_id: UUID of the light
            
        Returns:
            True if successful
        """
        ...
    
    async def rename_room(self, room_id: str, name: str) -> bool:
        """
        Rename a room.
        
        Args:
            room_id: UUID of the room
            name: New room name
            
        Returns:
            True if successful
        """
        ...
    
    async def get_room_lights(
        self, 
        room_id: str
    ) -> List[ResourceIdentifierDTO]:
        """
        Get all lights in a room.
        
        Args:
            room_id: UUID of the room
            
        Returns:
            List of light resource identifiers
        """
        ...
    
    async def get_room_info(self, room_id: str) -> RoomResponseDTO:
        """
        Get detailed room information.
        
        Args:
            room_id: UUID of the room
            
        Returns:
            RoomResponseDTO with complete room details
        """
        ...
    
    async def list_rooms(self) -> List[RoomResponseDTO]:
        """
        List all available rooms.
        
        Returns:
            List of RoomResponseDTO
        """
        ...
    
    async def delete_room(self, room_id: str) -> bool:
        """
        Delete a room.
        
        Args:
            room_id: UUID of the room
            
        Returns:
            True if successful
        """
        ...