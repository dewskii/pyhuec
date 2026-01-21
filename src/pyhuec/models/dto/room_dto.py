"""
Room/Zone DTOs for Hue API v2 requests and responses.
Based on: https://developers.meethue.com/develop/hue-api-v2/api-reference/
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ResourceIdentifierDTO(BaseModel):
    """Reference to another resource by ID and type."""
    rid: str
    rtype: str


class MetadataDTO(BaseModel):
    """Metadata information for a room/zone."""
    name: str
    archetype: Optional[str] = Field(
        None,
        description="Room archetype (living_room, kitchen, bedroom, etc.)",
        pattern="^(living_room|kitchen|dining|bedroom|kids_bedroom|bathroom|nursery|recreation|office|gym|hallway|toilet|front_door|garage|terrace|garden|driveway|carport|home|downstairs|upstairs|top_floor|attic|guest_room|staircase|lounge|man_cave|computer|studio|music|tv|reading|closet|storage|laundry_room|balcony|porch|barbecue|pool|other)$"
    )


# ===== Request DTOs =====

class RoomCreateDTO(BaseModel):
    """DTO for creating a new room/zone (POST request)."""
    metadata: MetadataDTO
    children: List[ResourceIdentifierDTO] = Field(
        description="List of lights and devices to include in the room"
    )
    type: str = Field(default="room", pattern="^(room|zone)$")

    class Config:
        extra = "forbid"


class RoomUpdateDTO(BaseModel):
    """DTO for updating a room/zone (PUT request)."""
    metadata: Optional[MetadataDTO] = None
    children: Optional[List[ResourceIdentifierDTO]] = Field(
        None,
        description="Update the list of lights and devices in the room"
    )

    class Config:
        extra = "forbid"


# ===== Response DTOs =====

class RoomResponseDTO(BaseModel):
    """DTO for room/zone resource response (GET)."""
    id: str
    id_v1: Optional[str] = None
    metadata: MetadataDTO
    children: List[ResourceIdentifierDTO] = Field(
        description="Lights and devices assigned to this room"
    )
    services: List[ResourceIdentifierDTO] = Field(
        default_factory=list,
        description="Services provided by this room (grouped_light, etc.)"
    )
    type: str = Field(pattern="^(room|zone)$")

    class Config:
        extra = "allow"


class RoomListResponseDTO(BaseModel):
    """DTO for list of rooms/zones response."""
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[RoomResponseDTO]


class RoomCreateResponseDTO(BaseModel):
    """DTO for room creation response."""
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[ResourceIdentifierDTO]


class RoomUpdateResponseDTO(BaseModel):
    """DTO for room update response."""
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[ResourceIdentifierDTO]


class RoomDeleteResponseDTO(BaseModel):
    """DTO for room deletion response."""
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[ResourceIdentifierDTO]
