"""
Data Transfer Objects (DTOs) for Hue API v2.
This package contains Pydantic models for all API requests and responses.
"""


from .common_dto import (
    ApiErrorDTO,
    ApiResponseDTO,
    ErrorResponseDTO,
    ResourceCollectionDTO,
    ResourceDTO,
    ResourceIdentifierDTO,
    ResourceListResponseDTO,
    SingleResourceResponseDTO,
)


from .bridge_dto import (
    BridgeConfigDTO,
    BridgeResponseDTO,
)


from .device_dto import (
    ButtonEventDTO,
    DeviceDeleteResponseDTO,
    DeviceIdentifyDTO,
    DeviceListResponseDTO,
    DevicePowerDTO,
    DeviceResponseDTO,
    DeviceUpdateDTO,
    DeviceUpdateResponseDTO,
    HomekitDTO,
    LightLevelSensorDTO,
    MotionSensorDTO,
    TemperatureSensorDTO,
    UserTestDTO,
    ZigbeeConnectivityDTO,
)


from .entertainment_dto import (
    EntertainmentChannelDTO,
    EntertainmentConfigurationDTO,
)


from .event_dto import (
    EventDataDTO,
    EventDTO,
    EventFilterDTO,
    EventStreamMessageDTO,
    EventSubscriptionDTO,
    EventType,
    InternalEventDTO,
    ResourceType,
)


from .grouped_light_dto import (
    GroupedLightIdentifyDTO,
    GroupedLightListResponseDTO,
    GroupedLightResponseDTO,
    GroupedLightUpdateDTO,
    GroupedLightUpdateResponseDTO,
)


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


from .room_dto import (
    RoomCreateDTO,
    RoomCreateResponseDTO,
    RoomDeleteResponseDTO,
    RoomListResponseDTO,
    RoomResponseDTO,
    RoomUpdateDTO,
    RoomUpdateResponseDTO,
)


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
    
    "ApiErrorDTO",
    "ApiResponseDTO",
    "ErrorResponseDTO",
    "ResourceCollectionDTO",
    "ResourceDTO",
    "ResourceIdentifierDTO",
    "ResourceListResponseDTO",
    "SingleResourceResponseDTO",
    
    "BridgeConfigDTO",
    "BridgeResponseDTO",
    
    "ButtonEventDTO",
    "DeviceIdentifyDTO",
    "DeviceListResponseDTO",
    "DeviceDeleteResponseDTO",
    "DevicePowerDTO",
    "DeviceResponseDTO",
    "DeviceUpdateDTO",
    "DeviceUpdateResponseDTO",
    "HomekitDTO",
    "LightLevelSensorDTO",
    "MotionSensorDTO",
    "TemperatureSensorDTO",
    "UserTestDTO",
    "ZigbeeConnectivityDTO",
    
    "EntertainmentChannelDTO",
    "EntertainmentConfigurationDTO",
  
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
    
    "RoomCreateDTO",
    "RoomCreateResponseDTO",
    "RoomDeleteResponseDTO",
    "RoomListResponseDTO",
    "RoomResponseDTO",
    "RoomUpdateDTO",
    "RoomUpdateResponseDTO",
    
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
    
    "DeviceIdentifyDTO",
    "DeviceListResponseDTO",
    "DeviceDeleteResponseDTO",
    "DeviceResponseDTO",
    "DeviceUpdateDTO",
    "DeviceUpdateResponseDTO",
    "UserTestDTO",
    
    "GroupedLightIdentifyDTO",
    "GroupedLightListResponseDTO",
    "GroupedLightResponseDTO",
    "GroupedLightUpdateDTO",
    "GroupedLightUpdateResponseDTO",
]
