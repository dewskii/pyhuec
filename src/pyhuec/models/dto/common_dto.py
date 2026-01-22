"""
Common API DTOs for Hue API v2 requests and responses.
These are generic DTOs used across all endpoints.
Based on: https://developers.meethue.com/develop/hue-api-v2/api-reference/
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class ResourceIdentifierDTO(BaseModel):
    """Reference to another resource by ID and type."""

    rid: str = Field(description="Resource ID (UUID)")
    rtype: str = Field(
        description="Resource type (light, room, scene, device, etc.)",
        pattern="^(device|bridge_home|room|zone|light|button|relative_rotary|temperature|light_level|motion|camera_motion|entertainment|contact|tamper|grouped_light|device_power|zigbee_bridge_connectivity|zgp_connectivity|zigbee_connectivity|zdp_connectivity|bridge|zigbee_device_discovery|homekit|matter|matter_fabric|scene|entertainment_configuration|public_image|auth_v1|behavior_script|behavior_instance|geofence|geofence_client|geolocation)$",
    )


class ApiErrorDTO(BaseModel):
    """Individual error in an API response."""

    description: str = Field(description="Human-readable error description")
    type: Optional[int] = Field(None, description="Numeric error type (legacy)")
    address: Optional[str] = Field(
        None, description="Resource address where error occurred"
    )


class ErrorResponseDTO(BaseModel):
    """Error response from the API."""

    errors: List[ApiErrorDTO]


T = TypeVar("T")


class ApiResponseDTO(BaseModel, Generic[T]):
    """Generic API response wrapper with errors and data."""

    errors: List[ApiErrorDTO] = Field(default_factory=list)
    data: List[T] = Field(default_factory=list)


class SingleResourceResponseDTO(BaseModel, Generic[T]):
    """Response containing a single resource."""

    errors: List[ApiErrorDTO] = Field(default_factory=list)
    data: List[T]


class ResourceListResponseDTO(BaseModel, Generic[T]):
    """Response containing a list of resources."""

    errors: List[ApiErrorDTO] = Field(default_factory=list)
    data: List[T]


class ResourceDTO(BaseModel):
    """Generic resource representation."""

    id: str
    type: str
    data: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")


class ResourceCollectionDTO(BaseModel):
    """Collection of all resources."""

    errors: List[ApiErrorDTO] = Field(default_factory=list)
    data: List[ResourceDTO]
