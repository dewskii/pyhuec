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
from pyhuec.transport.http_client import HttpClient


class RoomRepository(RoomRepositoryProtocol):
    """Repository for Room data access operations."""

    def __init__(self, http_client: HttpClient):
        """Initialize the repository with an HTTP client."""
        self._client = http_client

    async def get_room(self, room_id: str) -> RoomResponseDTO:
        """
        Retrieve a single room by ID.

        Args:
            room_id: UUID of the room

        Returns:
            RoomResponseDTO with room details
        """
        response = await self._client.get(f"/clip/v2/resource/room/{room_id}")
        return RoomResponseDTO(**response)

    async def get_rooms(self) -> RoomListResponseDTO:
        """
        Retrieve all rooms.

        Returns:
            RoomListResponseDTO with list of all rooms
        """
        response = await self._client.get("/clip/v2/resource/room")
        return RoomListResponseDTO(**response)

    async def create_room(self, create: RoomCreateDTO) -> RoomCreateResponseDTO:
        """
        Create a new room.

        Args:
            create: RoomCreateDTO with room configuration

        Returns:
            RoomCreateResponseDTO with created room ID
        """
        response = await self._client.post(
            "/clip/v2/resource/room",
            data=create.model_dump(exclude_none=True)
        )
        return RoomCreateResponseDTO(**response)

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
        response = await self._client.put(
            f"/clip/v2/resource/room/{room_id}",
            data=update.model_dump(exclude_none=True)
        )
        return RoomUpdateResponseDTO(**response)

    async def delete_room(self, room_id: str) -> RoomDeleteResponseDTO:
        """
        Delete a room.

        Args:
            room_id: UUID of the room

        Returns:
            RoomDeleteResponseDTO with confirmation
        """
        response = await self._client.delete(f"/clip/v2/resource/room/{room_id}")
        return RoomDeleteResponseDTO(**response)
