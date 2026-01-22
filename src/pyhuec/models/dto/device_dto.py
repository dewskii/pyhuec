"""
Device DTOs for Hue API v2 requests and responses.
Based on: https://developers.meethue.com/develop/hue-api-v2/api-reference/
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ResourceIdentifierDTO(BaseModel):
    """Reference to another resource by ID and type."""

    rid: str
    rtype: str


class MetadataDTO(BaseModel):
    """Metadata information for a device."""

    name: str
    archetype: Optional[str] = Field(
        None,
        description="Device archetype",
        pattern="^(bridge_v2|unknown_archetype|classic_bulb|sultan_bulb|flood_bulb|spot_bulb|candle_bulb|luster_bulb|pendant_round|pendant_long|ceiling_round|ceiling_square|floor_shade|floor_lantern|table_shade|recessed_ceiling|recessed_floor|single_spot|double_spot|table_wash|wall_lantern|wall_shade|flexible_lamp|ground_spot|wall_spot|plug|hue_go|hue_lightstrip|hue_iris|hue_bloom|bollard|wall_washer|hue_play|vintage_bulb|vintage_candle_bulb|ellipse_bulb|triangle_bulb|small_globe_bulb|large_globe_bulb|edison_bulb|christmas_tree|string_light|hue_centris|hue_lightstrip_tv|hue_lightstrip_pc|hue_tube|hue_signe|pendant_spot|ceiling_horizontal|ceiling_tube|hue_tap|hue_dimmer_switch|hue_motion_sensor|hue_smart_button)$",
    )


class ProductDataDTO(BaseModel):
    """Product information for a device."""

    model_id: str
    manufacturer_name: str
    product_name: str
    product_archetype: str
    certified: bool
    software_version: str
    hardware_platform_type: Optional[str] = None


class UserTestDTO(BaseModel):
    """User test mode status."""

    status: str = Field(pattern="^(set|changing)$")
    usertest: bool


class DeviceUpdateDTO(BaseModel):
    """DTO for updating a device (PUT request)."""

    metadata: Optional[MetadataDTO] = None
    usertest: Optional[UserTestDTO] = Field(
        None, description="Enable/disable user test mode for device identification"
    )

    model_config = ConfigDict(extra="forbid")


class DeviceIdentifyDTO(BaseModel):
    """DTO for identifying a device."""

    action: str = Field(
        pattern="^(identify)$", description="Set to 'identify' to identify the device"
    )


class DeviceResponseDTO(BaseModel):
    """DTO for device resource response (GET)."""

    id: str
    id_v1: Optional[str] = None
    product_data: ProductDataDTO
    metadata: MetadataDTO
    identify: Optional[Dict[str, Any]] = None
    services: List[ResourceIdentifierDTO] = Field(
        description="Services provided by this device (light, button, motion, etc.)"
    )
    usertest: Optional[UserTestDTO] = None
    type: str = Field(default="device")

    model_config = ConfigDict(extra="allow")


class DeviceListResponseDTO(BaseModel):
    """DTO for list of devices response."""

    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[DeviceResponseDTO]


class DeviceUpdateResponseDTO(BaseModel):
    """DTO for device update response."""

    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[ResourceIdentifierDTO]


class DeviceDeleteResponseDTO(BaseModel):
    """DTO for device deletion response."""

    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[ResourceIdentifierDTO]


class ButtonEventDTO(BaseModel):
    """Button press event data."""

    id: str
    id_v1: Optional[str] = None
    owner: ResourceIdentifierDTO
    metadata: Dict[str, str]
    button: Dict[str, Any]
    type: str = Field(default="button")


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


class DevicePowerDTO(BaseModel):
    """Device power status."""

    id: str
    id_v1: Optional[str] = None
    owner: ResourceIdentifierDTO
    power_state: Dict[str, Any]
    type: str = Field(default="device_power")


class HomekitDTO(BaseModel):
    """HomeKit configuration."""

    id: str
    status: str = Field(pattern="^(paired|pairing|unpaired)$")
    type: str = Field(default="homekit")
