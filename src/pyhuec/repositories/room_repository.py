from pyhuec.models.dto import (
    RoomCreateDTO,
    RoomCreateResponseDTO,
    RoomDeleteResponseDTO,
    RoomListResponseDTO,
    RoomResponseDTO,
    RoomUpdateDTO,
    RoomUpdateResponseDTO,
)
from pyhuec.models.protocols import RoomRepositoryProtocol


class RoomRepository(RoomRepositoryProtocol):
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
        self, room_id: str, update: RoomUpdateDTO
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
