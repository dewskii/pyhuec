import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from zeroconf import IPVersion, ServiceStateChange
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf

from pyhuec import MdnsClientProtocol

logger = logging.getLogger(__name__)
load_dotenv()


class MdnsClient(MdnsClientProtocol):
    """Protocol for mDNS (multicast DNS) service discovery."""

    def __init__(
        self,
    ) -> None:
        self.aiobrowser: AsyncServiceBrowser | None = None
        self.aiozc: AsyncZeroconf | None = None
        self.services: Dict[str, AsyncServiceInfo] = {}
        self.service_type = os.environ["TARGET_MDNS"]

    def _handler(
        self,
        zeroconf,
        service_type: str,
        name: str,
        state_change: ServiceStateChange,
    ) -> None:
        """
        Handle mDNS service events and async eventloop

        Args:
            zeroconf: Asynczeroconf
            service_type: String
            name: String
            state_change: ServiceStateChange
        Returns:
            None
        """
        logger.debug(f"EVENT {state_change} {name}")
        if state_change not in (
            ServiceStateChange.Added,
            ServiceStateChange.Updated,
        ):
            return
        asyncio.create_task(self._resolve_services(zeroconf, service_type, name))

    async def discover_services(
        self,
        service_type: str = "_hue._tcp.local.",
        timeout: float = 5.0,
    ) -> list[Dict[str, Any]]:
        """
        Discover services using mDNS.

        Args:
            service_type: mDNS service type to discover
            timeout: Discovery timeout in seconds

        Returns:
            List of discovered services with addresses and ports
        """
        service_type = os.environ["TARGET_MDNS"]
        async with AsyncZeroconf(ip_version=IPVersion.All) as aiozc:
            self.aiozc = aiozc
            self.aiobrowser = AsyncServiceBrowser(
                self.aiozc.zeroconf, service_type, handlers=[self._handler]
            )
            try:
                await asyncio.sleep(timeout)
            finally:
                await self.aiobrowser.async_cancel()
                await self.aiozc.async_close()

        # Return service IPv4 addresses
        ips: List[str] = []
        for info in self.services.values():
            ips.extend(info.parsed_addresses(version=IPVersion.V4Only))
        return sorted(set(ips))
        ...

    async def resolve_hostname(self, zeroconf, service_type: str, name: str) -> None:
        """
        Resolve hostname to IP address using mDNS, adding to the service store.

        Args:
            zeroconf: AsyncZeroconf configuration for service resolution
            service_type: String representation of the mDNS address to search for
            name: String representation of the service name
        Returns:
            None
        """
        info = AsyncServiceInfo(service_type, name)
        await info.async_request(zeroconf, 3000)
        logger.debug(f"RESOLVED {name} {info}")
        if info:
            self.services[name] = info
