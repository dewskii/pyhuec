"""
Event producer for consuming the Hue Bridge SSE stream.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import AsyncIterator, Optional

from pyhuec.models.dto.event_dto import EventStreamMessageDTO
from pyhuec.models.protocols import EventClientProtocol, EventProducerProtocol

logger = logging.getLogger(__name__)


class EventProducer(EventProducerProtocol):
    """
    Produces events from the Hue Bridge SSE endpoint.

    This producer connects to the bridge's event stream and yields
    parsed event messages for downstream processing.
    """

    def __init__(
        self,
        event_client: EventClientProtocol,
        endpoint: str = "/eventstream/clip/v2",
    ):
        """
        Initialize the event producer.

        Args:
            event_client: SSE client for connection
            endpoint: SSE endpoint path
        """
        self._client = event_client
        self._endpoint = endpoint
        self._is_running = False

    async def start(self) -> None:
        """
        Start producing events from the bridge.

        Raises:
            ConnectionError: If unable to connect to event stream
        """
        if self._is_running:
            logger.warning("Event producer already running")
            return

        logger.info(f"Connecting to event stream: {self._endpoint}")
        try:
            await self._client.connect(self._endpoint)
            self._is_running = True
            logger.info("Event producer started successfully")
        except Exception as e:
            logger.error(f"Failed to start event producer: {e}")
            raise ConnectionError(f"Could not connect to event stream: {e}") from e

    async def stop(self) -> None:
        """Stop producing events and cleanup resources."""
        if not self._is_running:
            return

        logger.info("Stopping event producer")
        try:
            await self._client.disconnect()
        except Exception as e:
            logger.error(f"Error disconnecting client: {e}")
        finally:
            self._is_running = False
            logger.info("Event producer stopped")

    def is_running(self) -> bool:
        """Check if the producer is currently running."""
        return self._is_running and self._client.is_connected()

    async def get_event_stream(self) -> AsyncIterator[EventStreamMessageDTO]:
        """
        Get an async iterator of raw event stream messages.

        Yields:
            EventStreamMessageDTO: Raw SSE messages from the bridge

        Raises:
            RuntimeError: If producer is not running
        """
        if not self._is_running:
            raise RuntimeError("Event producer not running. Call start() first.")

        logger.info("Starting event stream iteration")

        try:
            async for raw_event in self._client.listen():
                try:
                    message = self._parse_sse_message(raw_event)
                    if message:
                        yield message
                except Exception as e:
                    logger.error(f"Error parsing event message: {e}", exc_info=True)
                    continue

        except asyncio.CancelledError:
            logger.info("Event stream iteration cancelled")
            raise
        except Exception as e:
            logger.error(f"Error in event stream: {e}", exc_info=True)
            raise

    def _parse_sse_message(self, raw_data: str) -> Optional[EventStreamMessageDTO]:
        """
        Parse raw SSE data into EventStreamMessageDTO.

        Args:
            raw_data: Raw SSE message string

        Returns:
            Parsed message or None if invalid
        """
        try:
            lines = raw_data.strip().split("\n")
            message_id = None
            data_json = None

            for line in lines:
                if line.startswith("id:"):
                    message_id = line[3:].strip()
                elif line.startswith("data:"):
                    data_json = line[5:].strip()

            if not data_json:
                return None

            data = json.loads(data_json)

            return EventStreamMessageDTO(
                id=message_id,
                data=data,
                timestamp=datetime.utcnow(),
            )

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in SSE message: {e}")
            return None
        except Exception as e:
            logger.error(f"Error parsing SSE message: {e}", exc_info=True)
            return None
