"""
Entertainment DTOs for Hue API v2 requests and responses.
Based on: https://developers.meethue.com/develop/hue-api-v2/api-reference/
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .common_dto import ResourceIdentifierDTO


class EntertainmentChannelDTO(BaseModel):
    """Entertainment channel configuration."""

    channel_id: int = Field(ge=0, le=255)
    position: Dict[str, float] = Field(
        description="3D position with x, y, z coordinates"
    )
    members: List[ResourceIdentifierDTO]


class EntertainmentConfigurationDTO(BaseModel):
    """Entertainment configuration for synchronized lighting."""

    id: str
    metadata: Dict[str, str]
    name: str
    configuration_type: str = Field(pattern="^(screen|music|3dspace)$")
    status: str = Field(pattern="^(active|inactive)$")
    active_streamer: Optional[ResourceIdentifierDTO] = None
    stream_proxy: Dict[str, Any]
    channels: List[EntertainmentChannelDTO]
    locations: Dict[str, Any]
    light_services: List[ResourceIdentifierDTO]
    type: str = Field(default="entertainment_configuration")
