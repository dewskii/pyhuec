"""
Data Transfer Objects (DTOs) for Hue API v2.
This package contains Pydantic models for all API requests and responses.
"""

# Common DTOs
from .common_dto import (
    ApiErrorDTO,
    ApiResponseDTO,
    BridgeConfigDTO,
    BridgeResponseDTO,
    ButtonEventDTO,
    DevicePowerDTO,
    EntertainmentChannelDTO,
    EntertainmentConfigurationDTO,
    ErrorResponseDTO,
    EventDTO,
    HomekitDTO,
    LightLevelSensorDTO,
    MotionSensorDTO,
    ResourceCollectionDTO,
    ResourceDTO,
    ResourceIdentifierDTO,
    ResourceListResponseDTO,
    SingleResourceResponseDTO,
    TemperatureSensorDTO,
    ZigbeeConnectivityDTO,
)

# Device DTOs
from .device_dto import (
    DeviceDeleteResponseDTO,
    DeviceIdentifyDTO,
    DeviceListResponseDTO,
    DeviceResponseDTO,
    DeviceUpdateDTO,
    DeviceUpdateResponseDTO,
    UserTestDTO,
)

# Event DTOs
from .event_dto import (
    EventDataDTO,
    EventFilterDTO,
    EventStreamMessageDTO,
    EventSubscriptionDTO,
    EventType,
    InternalEventDTO,
    ResourceType,
)

# Grouped Light DTOs
from .grouped_light_dto import (
    GroupedLightIdentifyDTO,
    GroupedLightListResponseDTO,
    GroupedLightResponseDTO,
    GroupedLightUpdateDTO,
    GroupedLightUpdateResponseDTO,
)

# Light DTOs
from .light_dto import (
    AlertDTO as LightAlertDTO,
)
from .light_dto import (
    ColorDTO as LightColorDTO,
)
from .light_dto import (
    ColorTemperatureDeltaDTO,
    ContentConfigurationDTO,
    DimmingDeltaDTO,
    EffectActionDTO,
    EffectStatusDTO,
    EffectsV2DTO,
    GamutDTO,
    LightIdentifyDTO,
    LightListResponseDTO,
    LightResponseDTO,
    LightUpdateDTO,
    LightUpdateResponseDTO,
    MirekSchemaDTO,
    OrderDTO,
    OrientationDTO,
    PowerupColorDTO,
    PowerupDimmingDTO,
    PowerupDTO,
    PowerupOnDTO,
    ProductDataDTO,
    TimedEffectsDTO,
    XyDTO,
)
from .light_dto import (
    ColorTemperatureDTO as LightColorTemperatureDTO,
)
from .light_dto import (
    DimmingDTO as LightDimmingDTO,
)
from .light_dto import (
    DynamicsDTO as LightDynamicsDTO,
)
from .light_dto import (
    EffectsDTO as LightEffectsDTO,
)
from .light_dto import (
    GradientDTO as LightGradientDTO,
)
from .light_dto import (
    GradientPointDTO as LightGradientPointDTO,
)
from .light_dto import (
    MetadataDTO as LightMetadataDTO,
)
from .light_dto import (
    SignalingDTO as LightSignalingDTO,
)

# Room DTOs
from .room_dto import (
    RoomCreateDTO,
    RoomCreateResponseDTO,
    RoomDeleteResponseDTO,
    RoomListResponseDTO,
    RoomResponseDTO,
    RoomUpdateDTO,
    RoomUpdateResponseDTO,
)

# Scene DTOs
from .scene_dto import (
    ActionDTO as SceneActionDTO,
)
from .scene_dto import (
    DimmingDTO as SceneDimmingDTO,
)
from .scene_dto import (
    PaletteColorDTO,
    PaletteColorTemperatureDTO,
    PaletteDTO,
    SceneCreateDTO,
    SceneCreateResponseDTO,
    SceneDeleteResponseDTO,
    SceneListResponseDTO,
    SceneRecallDTO,
    SceneResponseDTO,
    SceneStatusDTO,
    SceneUpdateDTO,
    SceneUpdateResponseDTO,
)

__all__ = [
    # Common
    "ApiErrorDTO",
    "ApiResponseDTO",
    "ButtonEventDTO",
    "BridgeConfigDTO",
    "BridgeResponseDTO",
    "DevicePowerDTO",
    "EntertainmentChannelDTO",
    "EntertainmentConfigurationDTO",
    "ErrorResponseDTO",
    "EventDTO",
    "HomekitDTO",
    "LightLevelSensorDTO",
    "MotionSensorDTO",
    "ResourceCollectionDTO",
    "ResourceDTO",
    "ResourceIdentifierDTO",
    "ResourceListResponseDTO",
    "SingleResourceResponseDTO",
    "TemperatureSensorDTO",
    "ZigbeeConnectivityDTO",
    # Events
    "EventDataDTO",
    "EventFilterDTO",
    "EventStreamMessageDTO",
    "EventSubscriptionDTO",
    "EventType",
    "InternalEventDTO",
    "ResourceType",
    # Light
    "LightAlertDTO",
    "LightColorDTO",
    "LightColorTemperatureDTO",
    "ColorTemperatureDeltaDTO",
    "ContentConfigurationDTO",
    "LightDimmingDTO",
    "DimmingDeltaDTO",
    "LightDynamicsDTO",
    "EffectActionDTO",
    "LightEffectsDTO",
    "EffectStatusDTO",
    "EffectsV2DTO",
    "GamutDTO",
    "LightGradientDTO",
    "LightGradientPointDTO",
    "LightIdentifyDTO",
    "LightListResponseDTO",
    "LightResponseDTO",
    "LightUpdateDTO",
    "LightUpdateResponseDTO",
    "LightMetadataDTO",
    "MirekSchemaDTO",
    "OrderDTO",
    "OrientationDTO",
    "PowerupColorDTO",
    "PowerupDimmingDTO",
    "PowerupDTO",
    "PowerupOnDTO",
    "ProductDataDTO",
    "LightSignalingDTO",
    "TimedEffectsDTO",
    "XyDTO",
    # Room
    "RoomCreateDTO",
    "RoomCreateResponseDTO",
    "RoomDeleteResponseDTO",
    "RoomListResponseDTO",
    "RoomResponseDTO",
    "RoomUpdateDTO",
    "RoomUpdateResponseDTO",
    # Scene
    "SceneActionDTO",
    "SceneDimmingDTO",
    "PaletteColorDTO",
    "PaletteColorTemperatureDTO",
    "PaletteDTO",
    "SceneCreateDTO",
    "SceneCreateResponseDTO",
    "SceneDeleteResponseDTO",
    "SceneListResponseDTO",
    "SceneRecallDTO",
    "SceneResponseDTO",
    "SceneStatusDTO",
    "SceneUpdateDTO",
    "SceneUpdateResponseDTO",
    # Device
    "DeviceIdentifyDTO",
    "DeviceListResponseDTO",
    "DeviceDeleteResponseDTO",
    "DeviceResponseDTO",
    "DeviceUpdateDTO",
    "DeviceUpdateResponseDTO",
    "UserTestDTO",
    # Grouped Light
    "GroupedLightIdentifyDTO",
    "GroupedLightListResponseDTO",
    "GroupedLightResponseDTO",
    "GroupedLightUpdateDTO",
    "GroupedLightUpdateResponseDTO",
]
