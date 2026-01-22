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
    """Room data access."""

    def __init__(self, http_client: HttpClient):
        """Initialize repository.

        Args:
            http_client: HTTP client
        """
        self._client = http_client

    async def get_room(self, room_id: str) -> RoomResponseDTO:
        """Get room by ID.

        Args:
            room_id: Room UUID

        Returns:
            Room details
        """
        response = await self._client.get(f"/clip/v2/resource/room/{room_id}")
        return RoomResponseDTO(**response["data"][0])

    async def get_rooms(self) -> RoomListResponseDTO:
        """Get all rooms.

        Returns:
            All rooms
        """
        response = await self._client.get("/clip/v2/resource/room")
        return RoomListResponseDTO(**response)

    async def create_room(self, create: RoomCreateDTO) -> RoomCreateResponseDTO:
        """Create room.

        Args:
            create: Room configuration

        Returns:
            Created room ID
        """
        response = await self._client.post(
            "/clip/v2/resource/room",
            data=create.model_dump(exclude_none=True)
        )
        return RoomCreateResponseDTO(**response)

    async def update_room(
        self, room_id: str, update: RoomUpdateDTO
    ) -> RoomUpdateResponseDTO:
        """Update room.

        Args:
            room_id: Room UUID
            update: Room update

        Returns:
            Update confirmation
        """
        response = await self._client.put(
            f"/clip/v2/resource/room/{room_id}",
            data=update.model_dump(exclude_none=True)
        )
        return RoomUpdateResponseDTO(**response)

    async def delete_room(self, room_id: str) -> RoomDeleteResponseDTO:
        """Delete room.

        Args:
            room_id: Room UUID

        Returns:
            Delete confirmation
        """
        response = await self._client.delete(f"/clip/v2/resource/room/{room_id}")
        return RoomDeleteResponseDTO(**response)
