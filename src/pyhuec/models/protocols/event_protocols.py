"""
Protocol definitions for event consumption and production.
These protocols define the interface contracts for event handling.
"""

from typing import AsyncIterator, Callable, Optional, Protocol

from pyhuec.models.dto.event_dto import (
    EventFilterDTO,
    EventStreamMessageDTO,
    EventSubscriptionDTO,
    InternalEventDTO,
)


class EventProducerProtocol(Protocol):
    """Protocol for producing events from the Hue Bridge event stream."""

    async def start(self) -> None:
        """
        Start producing events from the bridge.

        Raises:
            ConnectionError: If unable to connect to event stream
        """
        ...

    async def stop(self) -> None:
        """
        Stop producing events and cleanup resources.
        """
        ...

    def is_running(self) -> bool:
        """
        Check if the producer is currently running.

        Returns:
            True if actively producing events
        """
        ...

    async def get_event_stream(self) -> AsyncIterator[EventStreamMessageDTO]:
        """
        Get an async iterator of raw event stream messages.

        Yields:
            EventStreamMessageDTO: Raw SSE messages from the bridge

        Raises:
            RuntimeError: If producer is not running
        """
        ...


class EventConsumerProtocol(Protocol):
    """Protocol for consuming processed events."""

    async def consume(
        self,
        event_filter: Optional[EventFilterDTO] = None,
    ) -> AsyncIterator[InternalEventDTO]:
        """
        Consume events with optional filtering.

        Args:
            event_filter: Optional filter criteria

        Yields:
            InternalEventDTO: Processed events matching filter

        Raises:
            RuntimeError: If event system is not running
        """
        ...

    async def subscribe(
        self,
        handler: Callable[[InternalEventDTO], None],
        event_filter: Optional[EventFilterDTO] = None,
    ) -> EventSubscriptionDTO:
        """
        Subscribe a handler to events with optional filtering.

        Args:
            handler: Async or sync callback function for events
            event_filter: Optional filter criteria

        Returns:
            EventSubscriptionDTO: Subscription details with ID

        Raises:
            ValueError: If handler is invalid
        """
        ...

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe a handler by subscription ID.

        Args:
            subscription_id: ID returned from subscribe()

        Returns:
            True if successfully unsubscribed
        """
        ...


class EventHandlerProtocol(Protocol):
    """Protocol for event handler callbacks."""

    async def handle(self, event: InternalEventDTO) -> None:
        """
        Handle an incoming event.

        Args:
            event: The event to handle

        Raises:
            Exception: Handler-specific errors
        """
        ...


class EventTransformerProtocol(Protocol):
    """Protocol for transforming raw events to internal events."""

    async def transform(
        self, raw_message: EventStreamMessageDTO
    ) -> list[InternalEventDTO]:
        """
        Transform raw SSE message to internal events.

        Args:
            raw_message: Raw event stream message from bridge

        Returns:
            List of processed internal events
        """
        ...


class EventBusProtocol(Protocol):
    """Protocol for event bus that coordinates producers and consumers."""

    async def start(self) -> None:
        """
        Start the event bus and begin event processing.

        Raises:
            RuntimeError: If already running
        """
        ...

    async def stop(self) -> None:
        """
        Stop the event bus and cleanup all resources.
        """
        ...

    def is_running(self) -> bool:
        """
        Check if event bus is running.

        Returns:
            True if actively processing events
        """
        ...

    async def publish(self, event: InternalEventDTO) -> None:
        """
        Manually publish an event to all subscribers.

        Args:
            event: Event to publish
        """
        ...

    async def subscribe(
        self,
        handler: Callable[[InternalEventDTO], None],
        event_filter: Optional[EventFilterDTO] = None,
    ) -> EventSubscriptionDTO:
        """
        Subscribe a handler to the event bus.

        Args:
            handler: Callback for events
            event_filter: Optional filter

        Returns:
            Subscription details
        """
        ...

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Remove a subscription.

        Args:
            subscription_id: Subscription to remove

        Returns:
            True if removed successfully
        """
        ...


class EventServiceProtocol(Protocol):
    """Protocol for high-level event service operations."""

    async def start_event_stream(self) -> None:
        """
        Start listening to the Hue bridge event stream.

        Raises:
            ConnectionError: If unable to connect
        """
        ...

    async def stop_event_stream(self) -> None:
        """
        Stop the event stream.
        """
        ...

    def is_streaming(self) -> bool:
        """
        Check if currently streaming events.

        Returns:
            True if stream is active
        """
        ...

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
        ...

    async def unsubscribe_from_events(self, subscription_id: str) -> bool:
        """
        Remove an event subscription.

        Args:
            subscription_id: ID from subscribe_to_events

        Returns:
            True if unsubscribed successfully
        """
        ...
