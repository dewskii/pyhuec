from pyhuec.models.dto import (
    RoomCreateDTO,
    RoomCreateResponseDTO,
    RoomDeleteResponseDTO,
    RoomListResponseDTO,
    RoomResponseDTO,
    RoomUpdateDTO,
    RoomUpdateResponseDTO,
)
from pyhuec.models.protocols import RoomControllerProtocol, RoomRepositoryProtocol


class RoomController(RoomControllerProtocol):
    """Room controller for handling API endpoint requests."""

    def __init__(self, room_repository: RoomRepositoryProtocol) -> None:
        """
        Initialize room controller.
        
        Args:
            room_repository: Repository for room data access
        """
        self._room_repository = room_repository

    async def handle_get_room(self, room_id: str) -> RoomResponseDTO:
        """
        Handle GET /room/{id} request.
        
        Args:
            room_id: UUID of the room
            
        Returns:
            Room details
        """
        return await self._room_repository.get_room(room_id)

    async def handle_get_rooms(self) -> RoomListResponseDTO:
        """
        Handle GET /room request.
        
        Returns:
            List of all rooms
        """
        return await self._room_repository.get_rooms()

    async def handle_create_room(self, create: RoomCreateDTO) -> RoomCreateResponseDTO:
        """
        Handle POST /room request.
        
        Args:
            create: Room creation data
            
        Returns:
            Creation response with new room ID
        """
        return await self._room_repository.create_room(create)

    async def handle_update_room(
        self, room_id: str, update: RoomUpdateDTO
    ) -> RoomUpdateResponseDTO:
        """
        Handle PUT /room/{id} request.
        
        Args:
            room_id: UUID of the room
            update: Room update data
            
        Returns:
            Update response
        """
        return await self._room_repository.update_room(room_id, update)

    async def handle_delete_room(self, room_id: str) -> RoomDeleteResponseDTO:
        """
        Handle DELETE /room/{id} request.
        
        Args:
            room_id: UUID of the room
            
        Returns:
            Deletion response
        """
        return await self._room_repository.delete_room(room_id)
