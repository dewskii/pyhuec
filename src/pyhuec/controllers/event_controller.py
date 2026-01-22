"""
Event controller for managing event stream operations.
This provides a higher-level interface for controlling event streaming.
"""

import logging
from typing import Callable, Optional

from pyhuec.models.dto.event_dto import EventFilterDTO, InternalEventDTO
from pyhuec.models.protocols.event_protocols import EventServiceProtocol

logger = logging.getLogger(__name__)


class EventController:
    """
    Controller for event stream operations.

    This controller provides a high-level interface for managing the event
    system, following the same controller pattern as other pyhuec controllers.
    """

    def __init__(self, event_service: EventServiceProtocol):
        """
        Initialize the event controller.

        Args:
            event_service: Event service implementation
        """
        self._service = event_service

    async def start_streaming(self) -> bool:
        """
        Start the event stream.

        Returns:
            True if successfully started

        Raises:
            ConnectionError: If unable to connect to event stream
        """
        try:
            await self._service.start_event_stream()
            logger.info("Event streaming started")
            return True
        except Exception as e:
            logger.error(f"Failed to start event streaming: {e}")
            raise

    async def stop_streaming(self) -> bool:
        """
        Stop the event stream.

        Returns:
            True if successfully stopped
        """
        try:
            await self._service.stop_event_stream()
            logger.info("Event streaming stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop event streaming: {e}")
            return False

    def is_streaming(self) -> bool:
        """
        Check if currently streaming events.

        Returns:
            True if stream is active
        """
        return self._service.is_streaming()

    async def subscribe(
        self,
        handler: Callable[[InternalEventDTO], None],
        event_filter: Optional[EventFilterDTO] = None,
    ) -> str:
        """
        Subscribe to events with a handler.

        Args:
            handler: Event handler callback (sync or async)
            event_filter: Optional filter criteria

        Returns:
            Subscription ID for later unsubscription

        Example:
            ```python
            async def my_handler(event):
                print(f"Event: {event.event_type}")

            subscription_id = await controller.subscribe(
                handler=my_handler,
                event_filter=EventFilterDTO(
                    resource_types=[ResourceType.LIGHT]
                )
            )
            ```
        """
        return await self._service.subscribe_to_events(handler, event_filter)

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Remove an event subscription.

        Args:
            subscription_id: ID returned from subscribe()

        Returns:
            True if successfully unsubscribed
        """
        return await self._service.unsubscribe_from_events(subscription_id)

    async def restart_streaming(self) -> bool:
        """
        Restart the event stream (stop then start).

        Returns:
            True if successfully restarted
        """
        logger.info("Restarting event stream")
        await self.stop_streaming()
        await self.start_streaming()
        return True
