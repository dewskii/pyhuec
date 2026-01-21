"""
Common API DTOs for Hue API v2 requests and responses.
These are generic DTOs used across all endpoints.
Based on: https://developers.meethue.com/develop/hue-api-v2/api-reference/
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

# ===== Resource Reference =====


class ResourceIdentifierDTO(BaseModel):
    """Reference to another resource by ID and type."""

    rid: str = Field(description="Resource ID (UUID)")
    rtype: str = Field(
        description="Resource type (light, room, scene, device, etc.)",
        pattern="^(device|bridge_home|room|zone|light|button|relative_rotary|temperature|light_level|motion|camera_motion|entertainment|contact|tamper|grouped_light|device_power|zigbee_bridge_connectivity|zgp_connectivity|zigbee_connectivity|zdp_connectivity|bridge|zigbee_device_discovery|homekit|matter|matter_fabric|scene|entertainment_configuration|public_image|auth_v1|behavior_script|behavior_instance|geofence|geofence_client|geolocation)$",
    )


# ===== Error Handling =====


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


# ===== Generic Response Wrappers =====

T = TypeVar("T")


class ApiResponseDTO(BaseModel, Generic[T]):
    """Generic API response wrapper with errors and data."""

    errors: List[ApiErrorDTO] = Field(default_factory=list)
    data: List[T] = Field(default_factory=list)


class SingleResourceResponseDTO(BaseModel, Generic[T]):
    """Response containing a single resource."""

    errors: List[ApiErrorDTO] = Field(default_factory=list)
    data: List[T]  # API always returns an array, even for single resources


class ResourceListResponseDTO(BaseModel, Generic[T]):
    """Response containing a list of resources."""

    errors: List[ApiErrorDTO] = Field(default_factory=list)
    data: List[T]


# ===== Bridge Configuration =====


class BridgeConfigDTO(BaseModel):
    """Bridge configuration information."""

    name: str
    swversion: str
    apiversion: str
    mac: str
    bridgeid: str
    factorynew: bool
    replacesbridgeid: Optional[str] = None
    modelid: str
    datastoreversion: str
    starterkit_id: str


class BridgeResponseDTO(BaseModel):
    """Bridge resource response."""

    id: str
    bridge_id: str
    time_zone: Dict[str, str]
    type: str = Field(default="bridge")

    class Config:
        extra = "allow"


# ===== Event Streaming =====


class EventDTO(BaseModel):
    """Server-Sent Event from the Hue bridge."""

    creationtime: str = Field(description="ISO 8601 timestamp")
    id: str = Field(description="Event ID (UUID)")
    type: str = Field(description="Event type (update, add, delete)")
    data: List[Dict[str, Any]] = Field(description="Changed resource data")


# ===== Entertainment =====


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


# ===== Button/Switch Events =====


class ButtonEventDTO(BaseModel):
    """Button press event data."""

    id: str
    id_v1: Optional[str] = None
    owner: ResourceIdentifierDTO
    metadata: Dict[str, str]
    button: Dict[str, Any]
    type: str = Field(default="button")


# ===== Sensor Data =====


class MotionSensorDTO(BaseModel):
    """Motion sensor data."""

    id: str
    id_v1: Optional[str] = None
    owner: ResourceIdentifierDTO
    enabled: bool
    motion: Dict[str, Any]
    type: str = Field(default="motion")


class TemperatureSensorDTO(BaseModel):
    """Temperature sensor data."""

    id: str
    id_v1: Optional[str] = None
    owner: ResourceIdentifierDTO
    enabled: bool
    temperature: Dict[str, float]
    type: str = Field(default="temperature")


class LightLevelSensorDTO(BaseModel):
    """Light level sensor data."""

    id: str
    id_v1: Optional[str] = None
    owner: ResourceIdentifierDTO
    enabled: bool
    light: Dict[str, Any]
    type: str = Field(default="light_level")


# ===== ZigBee Connectivity =====


class ZigbeeConnectivityDTO(BaseModel):
    """ZigBee connectivity status."""

    id: str
    id_v1: Optional[str] = None
    owner: ResourceIdentifierDTO
    status: str = Field(
        pattern="^(connected|disconnected|connectivity_issue|unidirectional_incoming)$"
    )
    mac_address: str
    type: str = Field(default="zigbee_connectivity")


# ===== Device Power =====


class DevicePowerDTO(BaseModel):
    """Device power status."""

    id: str
    id_v1: Optional[str] = None
    owner: ResourceIdentifierDTO
    power_state: Dict[str, Any]
    type: str = Field(default="device_power")


# ===== Homekit =====


class HomekitDTO(BaseModel):
    """HomeKit configuration."""

    id: str
    status: str = Field(pattern="^(paired|pairing|unpaired)$")
    type: str = Field(default="homekit")


# ===== Resource Discovery =====


class ResourceDTO(BaseModel):
    """Generic resource representation."""

    id: str
    type: str
    data: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"


class ResourceCollectionDTO(BaseModel):
    """Collection of all resources."""

    errors: List[ApiErrorDTO] = Field(default_factory=list)
    data: List[ResourceDTO]
