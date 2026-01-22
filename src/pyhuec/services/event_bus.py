"""
Event bus for coordinating event distribution to subscribers.
"""

import asyncio
import logging
from typing import Callable, Dict, List, Optional
from uuid import uuid4

from pyhuec.models.dto.event_dto import (
    EventFilterDTO,
    EventSubscriptionDTO,
    InternalEventDTO,
)
from pyhuec.models.protocols.event_protocols import EventBusProtocol

logger = logging.getLogger(__name__)


class EventBus(EventBusProtocol):
    """
    Event bus for distributing events to registered subscribers.

    Manages subscriptions with optional filtering and dispatches events
    to matching handlers asynchronously.
    """

    def __init__(self):
        """Initialize the event bus."""
        self._subscriptions: Dict[str, tuple[Callable, Optional[EventFilterDTO]]] = {}
        self._is_running = False
        self._event_queue: asyncio.Queue[InternalEventDTO] = asyncio.Queue()
        self._dispatch_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start the event bus and begin event processing."""
        if self._is_running:
            raise RuntimeError("Event bus already running")

        logger.info("Starting event bus")
        self._is_running = True
        self._dispatch_task = asyncio.create_task(self._dispatch_loop())

    async def stop(self) -> None:
        """Stop the event bus and cleanup all resources."""
        if not self._is_running:
            return

        logger.info("Stopping event bus")
        self._is_running = False

        await self._event_queue.put(None)

        if self._dispatch_task:
            try:
                await asyncio.wait_for(self._dispatch_task, timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("Dispatch task did not stop gracefully, cancelling")
                self._dispatch_task.cancel()
                try:
                    await self._dispatch_task
                except asyncio.CancelledError:
                    pass

        self._subscriptions.clear()

    def is_running(self) -> bool:
        """Check if event bus is running."""
        return self._is_running

    async def publish(self, event: InternalEventDTO) -> None:
        """
        Manually publish an event to all subscribers.

        Args:
            event: Event to publish
        """
        if not self._is_running:
            raise RuntimeError("Event bus not running")

        await self._event_queue.put(event)

    async def subscribe(
        self,
        handler: Callable[[InternalEventDTO], None],
        event_filter: Optional[EventFilterDTO] = None,
    ) -> EventSubscriptionDTO:
        """
        Subscribe a handler to the event bus.

        Args:
            handler: Callback for events (can be sync or async)
            event_filter: Optional filter

        Returns:
            Subscription details
        """
        if not callable(handler):
            raise ValueError("Handler must be callable")

        subscription_id = str(uuid4())
        self._subscriptions[subscription_id] = (handler, event_filter)

        logger.debug(
            f"Registered subscription {subscription_id} with filter: {event_filter}"
        )

        return EventSubscriptionDTO(
            subscription_id=subscription_id,
            filter=event_filter,
            active=True,
        )

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Remove a subscription.

        Args:
            subscription_id: Subscription to remove

        Returns:
            True if removed successfully
        """
        if subscription_id in self._subscriptions:
            del self._subscriptions[subscription_id]
            logger.debug(f"Removed subscription: {subscription_id}")
            return True
        return False

    async def _dispatch_loop(self) -> None:
        """Background task that dispatches events to subscribers."""
        logger.info("Event dispatch loop started")

        try:
            while self._is_running:
                event = await self._event_queue.get()

                if event is None:
                    break

                await self._dispatch_event(event)

        except Exception as e:
            logger.error(f"Error in dispatch loop: {e}", exc_info=True)
        finally:
            logger.info("Event dispatch loop stopped")

    async def _dispatch_event(self, event: InternalEventDTO) -> None:
        """
        Dispatch an event to all matching subscribers.

        Args:
            event: Event to dispatch
        """
        tasks = []

        for subscription_id, (handler, event_filter) in self._subscriptions.items():
            if not self._matches_filter(event, event_filter):
                continue

            task = asyncio.create_task(
                self._invoke_handler(subscription_id, handler, event)
            )
            tasks.append(task)

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def _matches_filter(
        self, event: InternalEventDTO, event_filter: Optional[EventFilterDTO]
    ) -> bool:
        """
        Check if an event matches the filter criteria.

        Args:
            event: Event to check
            event_filter: Filter criteria (None means match all)

        Returns:
            True if event matches filter
        """
        if event_filter is None:
            return True

        if (
            event_filter.event_types
            and event.event_type not in event_filter.event_types
        ):
            return False

        if (
            event_filter.resource_types
            and event.resource_type not in event_filter.resource_types
        ):
            return False

        if (
            event_filter.resource_ids
            and event.resource_id not in event_filter.resource_ids
        ):
            return False

        return True

    async def _invoke_handler(
        self, subscription_id: str, handler: Callable, event: InternalEventDTO
    ) -> None:
        """
        Invoke a handler with an event, handling both sync and async handlers.

        Args:
            subscription_id: ID of the subscription
            handler: Handler function to invoke
            event: Event to pass to handler
        """
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)
        except Exception as e:
            logger.error(
                f"Error in handler for subscription {subscription_id}: {e}",
                exc_info=True,
            )
