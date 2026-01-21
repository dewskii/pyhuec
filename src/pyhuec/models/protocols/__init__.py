"""
Protocol definitions for pyhuec models layer.
These protocols define interface contracts for repositories, services, and controllers.
"""

# Light protocols
from .light_protocol import (
    LightControllerProtocol,
    LightRepositoryProtocol,
    LightServiceProtocol,
)

# Room protocols
from .room_protocol import (
    RoomControllerProtocol,
    RoomRepositoryProtocol,
    RoomServiceProtocol,
)

# Scene protocols
from .scene_protocol import (
    SceneControllerProtocol,
    SceneRepositoryProtocol,
    SceneServiceProtocol,
)

# Device protocols
from .device_protocol import (
    DeviceControllerProtocol,
    DeviceRepositoryProtocol,
    DeviceServiceProtocol,
)

# Grouped Light protocols
from .grouped_light_protocol import (
    GroupedLightControllerProtocol,
    GroupedLightRepositoryProtocol,
    GroupedLightServiceProtocol,
)

# Bridge protocols
from .bridge_protocol import (
    BridgeControllerProtocol,
    BridgeDiscoveryProtocol,
    BridgeEventStreamProtocol,
    BridgeRepositoryProtocol,
    BridgeServiceProtocol,
)

# Transport protocols
from .transport_protocol import (
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
    "BridgeDiscoveryProtocol",
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
]
