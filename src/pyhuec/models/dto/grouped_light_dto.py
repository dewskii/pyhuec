"""
Grouped Light DTOs for Hue API v2 requests and responses.
Based on: https://developers.meethue.com/develop/hue-api-v2/api-reference/
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ResourceIdentifierDTO(BaseModel):
    """Reference to another resource by ID and type."""

    rid: str
    rtype: str


class XyDTO(BaseModel):
    """CIE XY color coordinates."""

    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)


class ColorDTO(BaseModel):
    """CIE XY color."""

    xy: XyDTO


class MirekSchemaDTO(BaseModel):
    """Mired color temperature range."""

    mirek_minimum: int = Field(ge=153)
    mirek_maximum: int = Field(le=500)


class ColorTemperatureDTO(BaseModel):
    """Color temperature in mirek."""

    mirek: Optional[int] = Field(None, ge=153, le=500)
    mirek_valid: Optional[bool] = None
    mirek_schema: Optional[MirekSchemaDTO] = None


class DimmingDTO(BaseModel):
    """Dimming/brightness control."""

    brightness: float = Field(ge=0.0, le=100.0)


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


class DynamicsDTO(BaseModel):
    """Dynamic effects configuration."""

    duration: Optional[int] = Field(None, ge=0)
    speed: Optional[float] = Field(None, ge=0.0, le=1.0)


class GroupedLightUpdateDTO(BaseModel):
    """DTO for updating a grouped light (PUT request)."""

    on: Optional[Dict[str, bool]] = Field(None, description="{'on': true/false}")
    dimming: Optional[DimmingDTO] = None
    color_temperature: Optional[ColorTemperatureDTO] = None
    color: Optional[ColorDTO] = None
    alert: Optional[AlertDTO] = None
    signaling: Optional[SignalingDTO] = None
    dynamics: Optional[DynamicsDTO] = None

    model_config = ConfigDict(extra="forbid")


class GroupedLightIdentifyDTO(BaseModel):
    """DTO for identifying all lights in a group."""

    action: str = Field(
        pattern="^(identify)$",
        description="Set to 'identify' to flash all lights in the group",
    )


class GroupedLightResponseDTO(BaseModel):
    """DTO for grouped light resource response (GET)."""

    id: str
    id_v1: Optional[str] = None
    owner: ResourceIdentifierDTO = Field(
        description="Room or zone that owns this grouped light"
    )
    on: Optional[Dict[str, bool]] = Field(
        None, description="Aggregated on/off state of all lights in the group"
    )
    dimming: Optional[DimmingDTO] = Field(
        None, description="Aggregated brightness of all lights in the group"
    )
    dimming_delta: Optional[Dict[str, Any]] = None
    color_temperature: Optional[ColorTemperatureDTO] = Field(
        None, description="Aggregated color temperature (if all lights support it)"
    )
    color: Optional[ColorDTO] = Field(
        None, description="Aggregated color (if all lights support it)"
    )
    alert: Optional[AlertDTO] = None
    signaling: Optional[SignalingDTO] = None
    dynamics: Optional[DynamicsDTO] = None
    type: str = Field(default="grouped_light")

    model_config = ConfigDict(extra="allow")


class GroupedLightListResponseDTO(BaseModel):
    """DTO for list of grouped lights response."""

    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[GroupedLightResponseDTO]


class GroupedLightUpdateResponseDTO(BaseModel):
    """DTO for grouped light update response."""

    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[ResourceIdentifierDTO]
