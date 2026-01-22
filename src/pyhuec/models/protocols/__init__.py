"""
Protocols definitions for pyhuec models layer.
These protocols define interface contracts for repositories, services, and controllers.
"""

# Light protocols
# Bridge protocols
from .bridge_protocols import (
    BridgeControllerProtocol,
    BridgeEventStreamProtocol,
    BridgeRepositoryProtocol,
    BridgeServiceProtocol,
)

# Device protocols
from .device_protocols import (
    DeviceControllerProtocol,
    DeviceRepositoryProtocol,
    DeviceServiceProtocol,
)

# Event protocols
from .event_protocols import (
    EventBusProtocol,
    EventConsumerProtocol,
    EventHandlerProtocol,
    EventProducerProtocol,
    EventServiceProtocol,
    EventTransformerProtocol,
)

# Grouped Light protocols
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

# Room protocols
from .room_protocols import (
    RoomControllerProtocol,
    RoomRepositoryProtocol,
    RoomServiceProtocol,
)

# Scene protocols
from .scene_protocols import (
    SceneControllerProtocol,
    SceneRepositoryProtocol,
    SceneServiceProtocol,
)

# Transport protocols
from .transport_protocols import (
    ApiClientProtocol,
    CacheProtocol,
    EventClientProtocol,
    HttpClientProtocol,
    MdnsClientProtocol,
    RateLimiterProtocol,
)

__all__ = [
    # Light
    "LightControllerProtocol",
    "LightRepositoryProtocol",
    "LightServiceProtocol",
    # Room
    "RoomControllerProtocol",
    "RoomRepositoryProtocol",
    "RoomServiceProtocol",
    # Scene
    "SceneControllerProtocol",
    "SceneRepositoryProtocol",
    "SceneServiceProtocol",
    # Device
    "DeviceControllerProtocol",
    "DeviceRepositoryProtocol",
    "DeviceServiceProtocol",
    # Grouped Light
    "GroupedLightControllerProtocol",
    "GroupedLightRepositoryProtocol",
    "GroupedLightServiceProtocol",
    # Bridge
    "BridgeControllerProtocol",
    "BridgeEventStreamProtocol",
    "BridgeRepositoryProtocol",
    "BridgeServiceProtocol",
    # Transport
    "ApiClientProtocol",
    "CacheProtocol",
    "EventClientProtocol",
    "HttpClientProtocol",
    "MdnsClientProtocol",
    "RateLimiterProtocol",
    # Events
    "EventBusProtocol",
    "EventConsumerProtocol",
    "EventHandlerProtocol",
    "EventProducerProtocol",
    "EventServiceProtocol",
    "EventTransformerProtocol",
]
