"""
Light DTOs for Hue API v2 requests and responses.
Based on: https://developers.meethue.com/develop/hue-api-v2/api-reference/
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator




class ResourceIdentifierDTO(BaseModel):
    """Reference to another resource by ID and type."""

    rid: str
    rtype: str


class MetadataDTO(BaseModel):
    """Metadata information for a resource."""

    name: str
    archetype: Optional[str] = None
    fixed_mired: Optional[int] = None


class XyDTO(BaseModel):
    """CIE XY color coordinates."""

    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)


class GamutDTO(BaseModel):
    """Color gamut defining the color space boundaries."""

    red: XyDTO
    green: XyDTO
    blue: XyDTO


class MirekSchemaDTO(BaseModel):
    """Mired color temperature range."""

    mirek_minimum: int = Field(ge=153)
    mirek_maximum: int = Field(le=500)


class ColorTemperatureDTO(BaseModel):
    """Color temperature in mirek."""

    mirek: Optional[int] = Field(None, ge=153, le=500)
    mirek_valid: Optional[bool] = None
    mirek_schema: Optional[MirekSchemaDTO] = None


class ColorDTO(BaseModel):
    """CIE XY color with gamut information."""

    xy: XyDTO
    gamut: Optional[GamutDTO] = None
    gamut_type: Optional[str] = None


class DimmingDTO(BaseModel):
    """Dimming/brightness control."""

    brightness: float = Field(ge=0.0, le=100.0)
    min_dim_level: Optional[float] = Field(None, ge=0.0, le=100.0)


class DimmingDeltaDTO(BaseModel):
    """Relative brightness change."""

    action: str = Field(pattern="^(up|down|stop)$")
    brightness_delta: Optional[float] = Field(None, ge=-100.0, le=100.0)


class ColorTemperatureDeltaDTO(BaseModel):
    """Relative color temperature change."""

    action: str = Field(pattern="^(up|down|stop)$")
    mirek_delta: Optional[int] = None


class DynamicsDTO(BaseModel):
    """Dynamic effects configuration."""

    status: Optional[str] = None
    status_values: Optional[List[str]] = None
    speed: Optional[float] = Field(None, ge=0.0, le=1.0)
    speed_valid: Optional[bool] = None
    duration: Optional[int] = Field(None, ge=0)


class AlertDTO(BaseModel):
    """Alert/identification flash."""

    action: Optional[str] = Field(None, pattern="^(breathe)$")
    action_values: Optional[List[str]] = None


class SignalingDTO(BaseModel):
    """Signaling configuration."""

    signal: Optional[str] = None
    signal_values: Optional[List[str]] = None
    duration: Optional[int] = Field(None, ge=0)
    colors: Optional[List[XyDTO]] = None


class GradientPointDTO(BaseModel):
    """Single color point in a gradient."""

    color: ColorDTO


class GradientDTO(BaseModel):
    """Gradient effect with multiple color points."""

    points: List[GradientPointDTO]
    mode: Optional[str] = None
    mode_values: Optional[List[str]] = None
    points_capable: Optional[int] = None
    pixel_count: Optional[int] = None


class EffectsDTO(BaseModel):
    """Effects configuration (legacy)."""

    effect: Optional[str] = None
    effect_values: Optional[List[str]] = None
    status: Optional[str] = None
    status_values: Optional[List[str]] = None


class EffectActionDTO(BaseModel):
    """Effect action configuration."""

    effect: str
    effect_values: Optional[List[str]] = None


class EffectStatusDTO(BaseModel):
    """Effect status information."""

    effect: str
    effect_values: Optional[List[str]] = None


class EffectsV2DTO(BaseModel):
    """Effects v2 with separate action and status."""

    action: Optional[EffectActionDTO] = None
    status: Optional[EffectStatusDTO] = None


class TimedEffectsDTO(BaseModel):
    """Time-based effects like sunrise/sunset."""

    effect: Optional[str] = None
    effect_values: Optional[List[str]] = None
    status: Optional[str] = None
    status_values: Optional[List[str]] = None
    duration: Optional[int] = Field(None, ge=0)


class PowerupOnDTO(BaseModel):
    """Power-up on state configuration."""

    mode: str = Field(pattern="^(on|toggle|previous)$")
    on: Optional[Dict[str, bool]] = None


class PowerupDimmingDTO(BaseModel):
    """Power-up dimming configuration."""

    mode: str = Field(pattern="^(dimming|previous)$")
    dimming: Optional[DimmingDTO] = None


class PowerupColorDTO(BaseModel):
    """Power-up color configuration."""

    mode: str = Field(pattern="^(color_temperature|color|previous)$")
    color_temperature: Optional[ColorTemperatureDTO] = None
    color: Optional[ColorDTO] = None


class PowerupDTO(BaseModel):
    """Power restoration behavior configuration."""

    preset: str = Field(pattern="^(safety|powerfail|last_on_state|custom)$")
    configured: Optional[bool] = None
    on: Optional[PowerupOnDTO] = None
    dimming: Optional[PowerupDimmingDTO] = None
    color: Optional[PowerupColorDTO] = None


class OrientationDTO(BaseModel):
    """Gradient orientation configuration."""

    configurable: Optional[bool] = None
    orientation: Optional[str] = Field(None, pattern="^(horizontal|vertical)$")


class OrderDTO(BaseModel):
    """Gradient order configuration."""

    configurable: Optional[bool] = None
    order: Optional[str] = Field(None, pattern="^(forward|reversed)$")


class ContentConfigurationDTO(BaseModel):
    """Content configuration for gradient lights."""

    orientation: Optional[OrientationDTO] = None
    order: Optional[OrderDTO] = None


class ProductDataDTO(BaseModel):
    """Product information."""

    model_id: Optional[str] = None
    manufacturer_name: Optional[str] = None
    product_name: Optional[str] = None
    product_archetype: Optional[str] = None
    certified: Optional[bool] = None
    software_version: Optional[str] = None
    hardware_platform_type: Optional[str] = None
    function: Optional[str] = Field(None, pattern="^(functional|decorative|mixed)$")





class LightUpdateDTO(BaseModel):
    """DTO for updating a light (PUT request)."""

    metadata: Optional[MetadataDTO] = None
    on: Optional[Dict[str, bool]] = Field(None, description="{'on': true/false}")
    dimming: Optional[DimmingDTO] = None
    dimming_delta: Optional[DimmingDeltaDTO] = None
    color_temperature: Optional[ColorTemperatureDTO] = None
    color_temperature_delta: Optional[ColorTemperatureDeltaDTO] = None
    color: Optional[ColorDTO] = None
    dynamics: Optional[DynamicsDTO] = None
    alert: Optional[AlertDTO] = None
    signaling: Optional[SignalingDTO] = None
    gradient: Optional[GradientDTO] = None
    effects: Optional[EffectsDTO] = None
    effects_v2: Optional[EffectsV2DTO] = None
    timed_effects: Optional[TimedEffectsDTO] = None
    powerup: Optional[PowerupDTO] = None
    content_configuration: Optional[ContentConfigurationDTO] = None

    model_config = ConfigDict(extra="forbid")


class LightIdentifyDTO(BaseModel):
    """DTO for identifying a light."""

    action: str = Field(
        pattern="^(identify)$", description="Set to 'identify' to flash the light"
    )





class LightResponseDTO(BaseModel):
    """DTO for light resource response (GET)."""

    id: str
    id_v1: Optional[str] = None
    owner: ResourceIdentifierDTO
    metadata: Optional[MetadataDTO] = None
    product_data: Optional[ProductDataDTO] = None
    identify: Optional[Dict[str, Any]] = None
    service_id: Optional[int] = None
    on: Dict[str, bool]
    dimming: Optional[DimmingDTO] = None
    dimming_delta: Optional[Dict[str, Any]] = None
    color_temperature: Optional[ColorTemperatureDTO] = None
    color_temperature_delta: Optional[Dict[str, Any]] = None
    color: Optional[ColorDTO] = None
    dynamics: Optional[DynamicsDTO] = None
    alert: Optional[AlertDTO] = None
    signaling: Optional[SignalingDTO] = None
    mode: Optional[str] = None
    gradient: Optional[GradientDTO] = None
    effects: Optional[EffectsDTO] = None
    effects_v2: Optional[EffectsV2DTO] = None
    timed_effects: Optional[TimedEffectsDTO] = None
    powerup: Optional[PowerupDTO] = None
    content_configuration: Optional[ContentConfigurationDTO] = None
    type: str = Field(default="light")

    model_config = ConfigDict(extra="allow")


class LightListResponseDTO(BaseModel):
    """DTO for list of lights response."""

    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[LightResponseDTO]


class LightUpdateResponseDTO(BaseModel):
    """DTO for light update response."""

    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[ResourceIdentifierDTO]
