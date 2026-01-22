"""
Factory for creating fully configured HueClient instances.

Handles dependency injection and wiring of all components.
Supports automatic bridge discovery and authentication.
"""

from email.mime import base
import logging
from pathlib import Path
from typing import Optional

from pyhuec.hue_client import HueClient
from pyhuec.repositories.grouped_light_repository import GroupedLightRepository
from pyhuec.repositories.light_repository import LightRepository
from pyhuec.repositories.room_repository import RoomRepository
from pyhuec.repositories.scene_repository import SceneRepository
from pyhuec.services.event_bus import EventBus
from pyhuec.services.event_service import EventService
from pyhuec.services.event_transformer import EventTransformer
from pyhuec.transport.bridge_authenticator import BridgeAuthenticator
from pyhuec.transport.event_client import EventClient
from pyhuec.transport.event_producer import EventProducer
from pyhuec.transport.http_client import HttpClient
from pyhuec.transport.mdns_client import MdnsClient

logger = logging.getLogger(__name__)


class HueClientFactory:
    """
    Factory for creating configured HueClient instances.

    Handles all the dependency wiring and configuration.
    Supports automatic mDNS discovery and API key generation.

    """

    @staticmethod
    async def create_client(
        bridge_ip: Optional[str] = None,
        api_key: Optional[str] = None,
        enable_events: bool = True,
        enable_cache: bool = True,
        auto_sync: bool = True,
        event_timeout: Optional[float] = None,
        http_timeout: float = 10.0,
        auto_authenticate: bool = True,
        mdns_timeout: float = 5.0,
        env_file: Optional[Path] = None,
    ) -> HueClient:
        """
        Create a fully configured HueClient with automatic discovery/auth.

        Args:
            bridge_ip: IP address of the Hue Bridge (auto-discovers if None)
            api_key: API key for authentication (loads from env or generates if None)
            enable_events: Enable event stream support
            enable_cache: Enable local state caching
            auto_sync: Auto-refresh cache after commands
            event_timeout: Timeout for event stream (None = no timeout)
            http_timeout: Timeout for HTTP requests
            auto_authenticate: If True, prompts for bridge button press to generate key
            mdns_timeout: Timeout for mDNS discovery
            env_file: Path to .env file for storing/loading API key

        Returns:
            Configured HueClient instance

        Raises:
            RuntimeError: If bridge cannot be found or authenticated
        """

        if bridge_ip is None:
            logger.info("No bridge IP provided, discovering via mDNS...")
            mdns_client = MdnsClient()
            bridges = await mdns_client.discover_bridges(timeout=mdns_timeout)

            if not bridges:
                raise RuntimeError(
                    "No Hue Bridge found on network. "
                    "Please ensure bridge is powered on and connected."
                )

            bridge_ip = bridges[0]["ip"]
            logger.info(f"✅ Discovered bridge at {bridge_ip}")
            print(f"🔍 Discovered Hue Bridge at {bridge_ip}")

        if api_key is None:
            logger.info("No API key provided, attempting to obtain one...")

            authenticator = BridgeAuthenticator(
                bridge_ip=bridge_ip,
                app_name="pyhuec",
                device_name="python-client",
            )

            try:
                api_key = await authenticator.get_or_create_api_key(
                    env_file=env_file,
                    interactive=auto_authenticate,
                )
            finally:
                await authenticator.close()

            if not api_key:
                raise RuntimeError(
                    "Failed to obtain API key. "
                    "Please provide api_key parameter or set HUE_USER environment variable."
                )

        base_url = f"https://{bridge_ip}"

        http_client = HttpClient(base_url=base_url)
        http_client.set_base_url(base_url)
        http_client.set_auth_token(api_key)
        http_client.set_timeout(http_timeout)

        light_repo = LightRepository(http_client=http_client)
        grouped_light_repo = GroupedLightRepository(http_client=http_client)
        room_repo = RoomRepository(http_client=http_client)
        scene_repo = SceneRepository(http_client=http_client)

        event_service = None
        if enable_events:
            event_client = EventClient(
                base_url=base_url,
                api_key=api_key,
                timeout=event_timeout,
            )
            event_producer = EventProducer(event_client=event_client)
            event_transformer = EventTransformer()
            event_bus = EventBus()

            event_service = EventService(
                event_producer=event_producer,
                event_transformer=event_transformer,
                event_bus=event_bus,
            )
        else:
            event_service = _DummyEventService()

        client = HueClient(
            light_repository=light_repo,
            grouped_light_repository=grouped_light_repo,
            room_repository=room_repo,
            scene_repository=scene_repo,
            event_service=event_service,
            enable_state_cache=enable_cache,
            auto_sync_on_command=auto_sync,
        )

        logger.info(
            f"Created HueClient for {bridge_ip} "
            f"(events={enable_events}, cache={enable_cache})"
        )

        return client

    @staticmethod
    async def create_from_discovery(
        api_key: Optional[str] = None,
        mdns_timeout: float = 5.0,
        auto_authenticate: bool = False,
        env_file: Optional[Path] = None,
        **kwargs,
    ) -> HueClient:
        """
        Create client by discovering bridge via mDNS.

        This is a convenience method that calls create_client() with
        bridge_ip=None to trigger auto-discovery.

        Args:
            api_key: API key for authentication (loads from env or generates if None)
            mdns_timeout: Timeout for mDNS discovery
            auto_authenticate: If True, prompts for bridge button press
            env_file: Path to .env file for storing/loading API key
            **kwargs: Additional arguments for create_client

        Returns:
            Configured HueClient instance

        Raises:
            RuntimeError: If no bridge found or authentication fails
        """
        return await HueClientFactory.create_client(
            bridge_ip=None,
            api_key=api_key,
            mdns_timeout=mdns_timeout,
            auto_authenticate=auto_authenticate,
            env_file=env_file,
            **kwargs,
        )


class _DummyEventService:
    """Dummy event service when events are disabled."""

    async def start_event_stream(self) -> None:
        """No-op start."""
        pass

    async def stop_event_stream(self) -> None:
        """No-op stop."""
        pass

    def is_streaming(self) -> bool:
        """Always false."""
        return False

    async def subscribe_to_events(self, handler, event_filter=None) -> str:
        """Return dummy subscription ID."""
        return "dummy-subscription"

    async def unsubscribe_from_events(self, subscription_id: str) -> bool:
        """Always succeeds."""
        return True
