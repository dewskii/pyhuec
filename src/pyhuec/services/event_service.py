"""
Event service for managing event consumption and production.
"""

import asyncio
import logging
from typing import Callable, Optional
from uuid import uuid4

from pyhuec.models.dto.event_dto import (
    EventFilterDTO,
    EventSubscriptionDTO,
    InternalEventDTO,
)
from pyhuec.models.protocols.event_protocols import (
    EventBusProtocol,
    EventProducerProtocol,
    EventServiceProtocol,
    EventTransformerProtocol,
)

logger = logging.getLogger(__name__)


class EventService(EventServiceProtocol):
    """
    High-level service for event stream management.

    This service coordinates event production, transformation, and distribution
    to subscribers through the event bus.
    """

    def __init__(
        self,
        event_producer: EventProducerProtocol,
        event_transformer: EventTransformerProtocol,
        event_bus: EventBusProtocol,
    ):
        """
        Initialize the event service.

        Args:
            event_producer: Producer for raw event stream
            event_transformer: Transformer for raw to internal events
            event_bus: Bus for event distribution
        """
        self._producer = event_producer
        self._transformer = event_transformer
        self._bus = event_bus
        self._processing_task: Optional[asyncio.Task] = None
        self._shutdown_event = asyncio.Event()

    async def start_event_stream(self) -> None:
        """Start listening to the Hue bridge event stream."""
        if self.is_streaming():
            logger.warning("Event stream already running")
            return

        logger.info("Starting event stream")
        await self._producer.start()
        await self._bus.start()

        
        self._shutdown_event.clear()
        self._processing_task = asyncio.create_task(self._process_events())

    async def stop_event_stream(self) -> None:
        """Stop the event stream and cleanup resources."""
        if not self.is_streaming():
            logger.warning("Event stream not running")
            return

        logger.info("Stopping event stream")
        self._shutdown_event.set()

        if self._processing_task:
            self._processing_task.cancel()
            try:
                await self._processing_task
            except asyncio.CancelledError:
                pass
            self._processing_task = None

        await self._producer.stop()
        await self._bus.stop()

    def is_streaming(self) -> bool:
        """Check if currently streaming events."""
        return (
            self._processing_task is not None
            and not self._processing_task.done()
            and self._producer.is_running()
        )

    async def subscribe_to_events(
        self,
        handler: Callable[[InternalEventDTO], None],
        event_filter: Optional[EventFilterDTO] = None,
    ) -> str:
        """
        Subscribe to events with a handler.

        Args:
            handler: Event handler callback
            event_filter: Optional filter criteria

        Returns:
            Subscription ID for later unsubscription
        """
        subscription = await self._bus.subscribe(handler, event_filter)
        logger.info(f"Created event subscription: {subscription.subscription_id}")
        return subscription.subscription_id

    async def unsubscribe_from_events(self, subscription_id: str) -> bool:
        """
        Remove an event subscription.

        Args:
            subscription_id: ID from subscribe_to_events

        Returns:
            True if unsubscribed successfully
        """
        result = await self._bus.unsubscribe(subscription_id)
        if result:
            logger.info(f"Removed event subscription: {subscription_id}")
        return result

    async def _process_events(self) -> None:
        """
        Background task to consume raw events, transform them, and publish.
        """
        logger.info("Event processing task started")
        try:
            async for raw_message in self._producer.get_event_stream():
                if self._shutdown_event.is_set():
                    break

                try:
                    
                    internal_events = await self._transformer.transform(raw_message)

                    
                    for event in internal_events:
                        await self._bus.publish(event)

                except Exception as e:
                    logger.error(f"Error processing event: {e}", exc_info=True)

        except asyncio.CancelledError:
            logger.info("Event processing task cancelled")
            raise
        except Exception as e:
            logger.error(f"Fatal error in event processing: {e}", exc_info=True)
        finally:
            logger.info("Event processing task stopped")
