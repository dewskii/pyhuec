"""
Protocol definitions for Room/Zone operations.
These protocols define the interface contracts for room repositories and services.
"""

from typing import List, Protocol
from pyhuec.models.dto import (
    RoomResponseDTO,
    RoomCreateDTO,
    RoomUpdateDTO,
    RoomListResponseDTO,
    RoomCreateResponseDTO,
    RoomUpdateResponseDTO,
    RoomDeleteResponseDTO,
    ResourceIdentifierDTO,
)


class RoomRepositoryProtocol(Protocol):
    """Protocol for Room data access operations."""
    
    async def get_room(self, room_id: str) -> RoomResponseDTO:
        """
        Retrieve a single room by ID.
        
        Args:
            room_id: UUID of the room
            
        Returns:
            RoomResponseDTO with room details
        """
        ...
    
    async def get_rooms(self) -> RoomListResponseDTO:
        """
        Retrieve all rooms.
        
        Returns:
            RoomListResponseDTO with list of all rooms
        """
        ...
    
    async def create_room(self, create: RoomCreateDTO) -> RoomCreateResponseDTO:
        """
        Create a new room.
        
        Args:
            create: RoomCreateDTO with room configuration
            
        Returns:
            RoomCreateResponseDTO with created room ID
        """
        ...
    
    async def update_room(
        self, 
        room_id: str, 
        update: RoomUpdateDTO
    ) -> RoomUpdateResponseDTO:
        """
        Update a room's configuration.
        
        Args:
            room_id: UUID of the room
            update: RoomUpdateDTO with desired changes
            
        Returns:
            RoomUpdateResponseDTO with confirmation
        """
        ...
    
    async def delete_room(self, room_id: str) -> RoomDeleteResponseDTO:
        """
        Delete a room.
        
        Args:
            room_id: UUID of the room
            
        Returns:
            RoomDeleteResponseDTO with confirmation
        """
        ...


class RoomServiceProtocol(Protocol):
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


class RoomControllerProtocol(Protocol):
    """Protocol for Room controller operations (API endpoint handlers)."""
    
    async def handle_get_room(self, room_id: str) -> RoomResponseDTO:
        """Handle GET /room/{id} request."""
        ...
    
    async def handle_get_rooms(self) -> RoomListResponseDTO:
        """Handle GET /room request."""
        ...
    
    async def handle_create_room(
        self, 
        create: RoomCreateDTO
    ) -> RoomCreateResponseDTO:
        """Handle POST /room request."""
        ...
    
    async def handle_update_room(
        self, 
        room_id: str, 
        update: RoomUpdateDTO
    ) -> RoomUpdateResponseDTO:
        """Handle PUT /room/{id} request."""
        ...
    
    async def handle_delete_room(
        self, 
        room_id: str
    ) -> RoomDeleteResponseDTO:
        """Handle DELETE /room/{id} request."""
        ...
