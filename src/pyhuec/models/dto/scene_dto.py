"""
Scene DTOs for Hue API v2 requests and responses.
Based on: https://developers.meethue.com/develop/hue-api-v2/api-reference/
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ResourceIdentifierDTO(BaseModel):
    """Reference to another resource by ID and type."""

    rid: str
    rtype: str


class MetadataDTO(BaseModel):
    """Metadata information for a scene."""

    name: str
    image: Optional[ResourceIdentifierDTO] = None
    appdata: Optional[str] = Field(None, max_length=16)


class XyDTO(BaseModel):
    """CIE XY color coordinates."""

    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)


class ColorDTO(BaseModel):
    """CIE XY color."""

    xy: XyDTO


class ColorTemperatureDTO(BaseModel):
    """Color temperature in mirek."""

    mirek: int = Field(ge=153, le=500)


class DimmingDTO(BaseModel):
    """Dimming/brightness control."""

    brightness: float = Field(ge=0.0, le=100.0)


class GradientPointDTO(BaseModel):
    """Single color point in a gradient."""

    color: ColorDTO


class GradientDTO(BaseModel):
    """Gradient effect with multiple color points."""

    points: List[GradientPointDTO]


class EffectsDTO(BaseModel):
    """Effects configuration."""

    effect: str = Field(
        pattern="^(prism|opal|glisten|sparkle|fire|candle|underwater|cosmos|sunbeam|enchant|no_effect)$"
    )


class DynamicsDTO(BaseModel):
    """Dynamic effects configuration."""

    duration: int = Field(ge=0, description="Transition duration in milliseconds")


class ActionDTO(BaseModel):
    """Action to perform on a light in a scene."""

    target: ResourceIdentifierDTO = Field(description="Target light or grouped_light")
    on: Optional[Dict[str, bool]] = Field(None, description="{'on': true/false}")
    dimming: Optional[DimmingDTO] = None
    color: Optional[ColorDTO] = None
    color_temperature: Optional[ColorTemperatureDTO] = None
    gradient: Optional[GradientDTO] = None
    effects: Optional[EffectsDTO] = None
    dynamics: Optional[DynamicsDTO] = None

    class Config:
        extra = "forbid"


class PaletteColorDTO(BaseModel):
    """Color in a scene palette."""

    color: ColorDTO
    dimming: DimmingDTO


class PaletteColorTemperatureDTO(BaseModel):
    """Color temperature in a scene palette."""

    color_temperature: ColorTemperatureDTO
    dimming: DimmingDTO


class PaletteDTO(BaseModel):
    """Color palette for a scene."""

    color: Optional[List[PaletteColorDTO]] = None
    color_temperature: Optional[List[PaletteColorTemperatureDTO]] = None
    dimming: Optional[List[DimmingDTO]] = None


# ===== Request DTOs =====


class SceneCreateDTO(BaseModel):
    """DTO for creating a new scene (POST request)."""

    metadata: MetadataDTO
    group: ResourceIdentifierDTO = Field(
        description="Room or zone this scene belongs to"
    )
    actions: List[ActionDTO] = Field(
        description="Actions to perform when activating the scene"
    )
    palette: Optional[PaletteDTO] = None
    speed: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Speed of dynamic effects"
    )
    auto_dynamic: Optional[bool] = Field(
        None, description="Enable automatic dynamic palette"
    )
    type: str = Field(default="scene")

    class Config:
        extra = "forbid"


class SceneUpdateDTO(BaseModel):
    """DTO for updating a scene (PUT request)."""

    metadata: Optional[MetadataDTO] = None
    actions: Optional[List[ActionDTO]] = Field(None, description="Update scene actions")
    palette: Optional[PaletteDTO] = None
    speed: Optional[float] = Field(None, ge=0.0, le=1.0)
    auto_dynamic: Optional[bool] = None

    class Config:
        extra = "forbid"


class SceneRecallDTO(BaseModel):
    """DTO for recalling/activating a scene (PUT request to recall endpoint)."""

    action: str = Field(default="active", pattern="^(active|dynamic_palette|static)$")
    duration: Optional[int] = Field(
        None, ge=0, description="Transition duration in milliseconds"
    )
    dimming: Optional[DimmingDTO] = Field(None, description="Override scene brightness")

    class Config:
        extra = "forbid"


# ===== Response DTOs =====


class SceneStatusDTO(BaseModel):
    """Scene status information."""

    active: Optional[str] = Field(None, pattern="^(inactive|static|dynamic_palette)$")


class SceneResponseDTO(BaseModel):
    """DTO for scene resource response (GET)."""

    id: str
    id_v1: Optional[str] = None
    metadata: MetadataDTO
    group: ResourceIdentifierDTO
    actions: List[ActionDTO]
    palette: Optional[PaletteDTO] = None
    speed: Optional[float] = Field(None, ge=0.0, le=1.0)
    auto_dynamic: Optional[bool] = None
    status: Optional[SceneStatusDTO] = None
    type: str = Field(default="scene")

    class Config:
        extra = "allow"


class SceneListResponseDTO(BaseModel):
    """DTO for list of scenes response."""

    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[SceneResponseDTO]


class SceneCreateResponseDTO(BaseModel):
    """DTO for scene creation response."""

    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[ResourceIdentifierDTO]


class SceneUpdateResponseDTO(BaseModel):
    """DTO for scene update response."""

    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[ResourceIdentifierDTO]


class SceneDeleteResponseDTO(BaseModel):
    """DTO for scene deletion response."""

    errors: List[Dict[str, Any]] = Field(default_factory=list)
    data: List[ResourceIdentifierDTO]
