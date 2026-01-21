from pyhuec.models.dto.room_dto import RoomCreateDTO, RoomCreateResponseDTO, RoomDeleteResponseDTO, RoomListResponseDTO, RoomResponseDTO, RoomUpdateDTO, RoomUpdateResponseDTO
from pyhuec.models.protocols.room_protocol import RoomControllerProtocol


class RoomController(RoomControllerProtocol):
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
