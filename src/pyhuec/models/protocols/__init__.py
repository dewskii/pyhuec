"""
Protocols definitions for pyhuec models layer.
These protocols define interface contracts for repositories, services, and controllers.
"""

from .bridge_protocols import (
    BridgeControllerProtocol,
    BridgeEventStreamProtocol,
    BridgeRepositoryProtocol,
    BridgeServiceProtocol,
)
from .device_protocols import (
    DeviceControllerProtocol,
    DeviceRepositoryProtocol,
    DeviceServiceProtocol,
)
from .event_protocols import (
    EventBusProtocol,
    EventConsumerProtocol,
    EventHandlerProtocol,
    EventProducerProtocol,
    EventServiceProtocol,
    EventTransformerProtocol,
)
from .grouped_light_protocols import (
    GroupedLightControllerProtocol,
    GroupedLightRepositoryProtocol,
    GroupedLightServiceProtocol,
)
from .light_protocols import (
    LightControllerProtocol,
    LightRepositoryProtocol,
    LightServiceProtocol,
)
from .room_protocols import (
    RoomControllerProtocol,
    RoomRepositoryProtocol,
    RoomServiceProtocol,
)
from .scene_protocols import (
    SceneControllerProtocol,
    SceneRepositoryProtocol,
    SceneServiceProtocol,
)
from .transport_protocols import (
    ApiClientProtocol,
    CacheProtocol,
    EventClientProtocol,
    HttpClientProtocol,
    MdnsClientProtocol,
    RateLimiterProtocol,
)

__all__ = [
    "LightControllerProtocol",
    "LightRepositoryProtocol",
    "LightServiceProtocol",
    "RoomControllerProtocol",
    "RoomRepositoryProtocol",
    "RoomServiceProtocol",
    "SceneControllerProtocol",
    "SceneRepositoryProtocol",
    "SceneServiceProtocol",
    "DeviceControllerProtocol",
    "DeviceRepositoryProtocol",
    "DeviceServiceProtocol",
    "GroupedLightControllerProtocol",
    "GroupedLightRepositoryProtocol",
    "GroupedLightServiceProtocol",
    "BridgeControllerProtocol",
    "BridgeEventStreamProtocol",
    "BridgeRepositoryProtocol",
    "BridgeServiceProtocol",
    "ApiClientProtocol",
    "CacheProtocol",
    "EventClientProtocol",
    "HttpClientProtocol",
    "MdnsClientProtocol",
    "RateLimiterProtocol",
    "EventBusProtocol",
    "EventConsumerProtocol",
    "EventHandlerProtocol",
    "EventProducerProtocol",
    "EventServiceProtocol",
    "EventTransformerProtocol",
]
