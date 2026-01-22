"""
SSE (Server-Sent Events) client for Hue Bridge event stream.
"""

import asyncio
import logging
from typing import AsyncIterator, Optional

import httpx

from pyhuec.models.protocols import EventClientProtocol

logger = logging.getLogger(__name__)


class EventClient(EventClientProtocol):
    """
    Server-Sent Events (SSE) client for Hue Bridge event stream.

    This client connects to the Hue Bridge SSE endpoint and yields
    raw event data for processing by the EventProducer.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        client: Optional[httpx.AsyncClient] = None,
    ):
        """
        Initialize the SSE client.

        Args:
            base_url: Base URL of the Hue Bridge (e.g., "https://192.168.1.100")
            api_key: Hue application key for authentication
            timeout: Optional timeout for connection (None = no timeout)
            max_retries: Maximum connection retry attempts
            retry_delay: Delay between retry attempts in seconds
        """
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._timeout = timeout
        self._max_retries = max_retries
        self._retry_delay = retry_delay

        self._client = (
            client
            if client
            else httpx.AsyncClient(
                timeout=httpx.Timeout(self._timeout) if self._timeout else None,
                verify=False,
            )
        )
        self._connected = False
        self._current_endpoint: Optional[str] = None

    async def connect(self, endpoint: str) -> None:
        """
        Connect to SSE endpoint.

        Args:
            endpoint: SSE endpoint path (e.g., "/eventstream/clip/v2")

        Raises:
            ConnectionError: If unable to establish connection after retries
        """
        if self._connected:
            logger.warning("Already connected to event stream")
            return

        self._current_endpoint = endpoint

        logger.info(f"SSE client initialized for endpoint: {endpoint}")
        self._connected = True

    async def disconnect(self) -> None:
        """
        Disconnect from SSE endpoint and cleanup resources.
        """
        if not self._connected:
            return

        logger.info("Disconnecting SSE client")

        if self._client:
            await self._client.aclose()
            self._client = None

        self._connected = False
        self._current_endpoint = None

        logger.info("SSE client disconnected")

    async def listen(self) -> AsyncIterator[str]:
        """
        Listen for incoming events from the SSE stream.

        Yields:
            str: Raw SSE event data

        Raises:
            RuntimeError: If not connected
            ConnectionError: If connection is lost and cannot be re-established
        """
        if not self._connected or not self._client or not self._current_endpoint:
            raise RuntimeError("Not connected to event stream. Call connect() first.")

        url = f"{self._base_url}{self._current_endpoint}"
        headers = {
            "hue-application-key": self._api_key,
            "Accept": "text/event-stream",
        }

        retry_count = 0

        while self._connected:
            try:
                logger.info(f"Connecting to SSE stream: {url}")

                async with self._client.stream(
                    "GET",
                    url,
                    headers=headers,
                ) as response:
                    if response.status_code != 200:
                        raise ConnectionError(
                            f"SSE connection failed with status {response.status_code}"
                        )

                    logger.info("Connected to SSE stream successfully")
                    retry_count = 0

                    current_message = []

                    async for line in response.aiter_lines():
                        if not self._connected:
                            logger.info("Disconnection requested, stopping stream")
                            break

                        if not line or line.strip() == "":
                            if current_message:
                                message = "\n".join(current_message)
                                current_message = []
                                yield message
                        else:
                            current_message.append(line)

                    if current_message:
                        message = "\n".join(current_message)
                        yield message

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error in SSE stream: {e}")
                retry_count += 1

                if retry_count >= self._max_retries:
                    raise ConnectionError(
                        f"Failed to connect after {self._max_retries} attempts"
                    ) from e

                logger.info(f"Retrying connection in {self._retry_delay}s...")
                await asyncio.sleep(self._retry_delay)

            except httpx.RequestError as e:
                logger.error(f"Request error in SSE stream: {e}")
                retry_count += 1

                if retry_count >= self._max_retries:
                    raise ConnectionError(
                        f"Failed to connect after {self._max_retries} attempts"
                    ) from e

                logger.info(f"Retrying connection in {self._retry_delay}s...")
                await asyncio.sleep(self._retry_delay)

            except asyncio.CancelledError:
                logger.info("SSE stream cancelled")
                break

            except Exception as e:
                logger.error(f"Unexpected error in SSE stream: {e}", exc_info=True)
                retry_count += 1

                if retry_count >= self._max_retries:
                    raise ConnectionError(
                        f"SSE stream failed after {self._max_retries} attempts"
                    ) from e

                logger.info(f"Retrying connection in {self._retry_delay}s...")
                await asyncio.sleep(self._retry_delay)

    def is_connected(self) -> bool:
        """
        Check if connected to event stream.

        Returns:
            True if connected and client is active
        """
        return self._connected and self._client is not None
