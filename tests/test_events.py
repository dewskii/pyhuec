"""
Test examples for the event system.

This demonstrates how to test event components using mocks and fixtures.
"""

import asyncio
from datetime import datetime, timezone
from typing import AsyncIterator, List
from unittest.mock import AsyncMock, Mock

import pytest

from pyhuec.models.dto.event_dto import (
    EventDataDTO,
    EventDTO,
    EventFilterDTO,
    EventStreamMessageDTO,
    EventType,
    InternalEventDTO,
    ResourceType,
)
from pyhuec.services.event_bus import EventBus
from pyhuec.services.event_service import EventService
from pyhuec.services.event_transformer import EventTransformer


class MockEventClient:
    """Mock SSE client for testing."""

    def __init__(self, events: List[str] = None):
        self.events = events or []
        self.connected = False
        self.event_index = 0

    async def connect(self, endpoint: str) -> None:
        self.connected = True

    async def disconnect(self) -> None:
        self.connected = False

    async def listen(self) -> AsyncIterator[str]:
        for event in self.events:
            if not self.connected:
                break
            yield event
            await asyncio.sleep(0.01)

    def is_connected(self) -> bool:
        return self.connected


class MockEventProducer:
    """Mock event producer for testing."""

    def __init__(self, messages: List[EventStreamMessageDTO] = None):
        self.messages = messages or []
        self._is_running = False

    async def start(self) -> None:
        self._is_running = True

    async def stop(self) -> None:
        self._is_running = False

    def is_running(self) -> bool:
        return self._is_running

    async def get_event_stream(self) -> AsyncIterator[EventStreamMessageDTO]:
        for message in self.messages:
            if not self._is_running:
                break
            yield message
            await asyncio.sleep(0.01)


@pytest.fixture
def sample_event_dto():
    """Sample EventDTO for testing."""
    return EventDTO(
        creationtime=datetime.now(timezone.utc),
        id="event-123",
        type=EventType.UPDATE,
        data=[
            EventDataDTO(
                id="light-uuid",
                type=ResourceType.LIGHT,
                data={"on": {"on": True}, "brightness": {"brightness": 75.0}},
            )
        ],
    )


@pytest.fixture
def sample_sse_message(sample_event_dto):
    """Sample SSE message for testing."""
    return EventStreamMessageDTO(
        id="message-123",
        data=[sample_event_dto],
        timestamp=datetime.now(timezone.utc),
    )


@pytest.fixture
def sample_internal_event():
    """Sample internal event for testing."""
    return InternalEventDTO(
        event_id="event-123",
        event_type=EventType.UPDATE,
        resource_type=ResourceType.LIGHT,
        resource_id="light-uuid",
        timestamp=datetime.now(timezone.utc),
        data=EventDataDTO(
            id="light-uuid",
            type=ResourceType.LIGHT,
            on={"on": True},
            dimming={"brightness": 75.0},
        ),
        metadata={"test": True},
    )


@pytest.mark.asyncio
async def test_event_bus_subscribe():
    """Test subscribing to event bus."""
    bus = EventBus()
    await bus.start()

    handler = Mock()
    subscription = await bus.subscribe(handler)

    assert subscription.subscription_id is not None
    assert subscription.active is True

    await bus.stop()


@pytest.mark.asyncio
async def test_event_bus_publish_and_receive(sample_internal_event):
    """Test publishing and receiving events."""
    bus = EventBus()
    await bus.start()

    received_events = []

    async def handler(event):
        received_events.append(event)

    await bus.subscribe(handler)
    await bus.publish(sample_internal_event)

    await asyncio.sleep(0.1)

    assert len(received_events) == 1
    assert received_events[0].event_id == sample_internal_event.event_id

    await bus.stop()


@pytest.mark.asyncio
async def test_event_bus_filtering(sample_internal_event):
    """Test event filtering."""
    bus = EventBus()
    await bus.start()

    light_events = []

    async def light_handler(event):
        light_events.append(event)

    light_filter = EventFilterDTO(resource_types=[ResourceType.LIGHT])
    await bus.subscribe(light_handler, light_filter)

    await bus.publish(sample_internal_event)

    motion_event = InternalEventDTO(
        event_id="motion-123",
        event_type=EventType.UPDATE,
        resource_type=ResourceType.MOTION,
        resource_id="motion-uuid",
        timestamp=datetime.now(timezone.utc),
        data=EventDataDTO(
            id="motion-uuid",
            type=ResourceType.MOTION,
        ),
    )
    await bus.publish(motion_event)

    await asyncio.sleep(0.1)

    assert len(light_events) == 1
    assert light_events[0].resource_type == ResourceType.LIGHT

    await bus.stop()


@pytest.mark.asyncio
async def test_event_bus_multiple_handlers(sample_internal_event):
    """Test multiple handlers receiving same event."""
    bus = EventBus()
    await bus.start()

    received_by = []

    async def handler1(event):
        received_by.append("handler1")

    async def handler2(event):
        received_by.append("handler2")

    def handler3(event):
        received_by.append("handler3")

    await bus.subscribe(handler1)
    await bus.subscribe(handler2)
    await bus.subscribe(handler3)

    await bus.publish(sample_internal_event)
    await asyncio.sleep(0.1)

    assert len(received_by) == 3
    assert "handler1" in received_by
    assert "handler2" in received_by
    assert "handler3" in received_by

    await bus.stop()


@pytest.mark.asyncio
async def test_event_bus_unsubscribe():
    """Test unsubscribing from event bus."""
    bus = EventBus()
    await bus.start()

    received = []

    async def handler(event):
        received.append(event)

    subscription = await bus.subscribe(handler)

    result = await bus.unsubscribe(subscription.subscription_id)
    assert result is True

    event = InternalEventDTO(
        event_id="test",
        event_type=EventType.UPDATE,
        resource_type=ResourceType.LIGHT,
        resource_id="light-1",
        timestamp=datetime.now(timezone.utc),
        data=EventDataDTO(
            id="light-1",
            type=ResourceType.LIGHT,
        ),
    )
    await bus.publish(event)
    await asyncio.sleep(0.1)

    assert len(received) == 0

    await bus.stop()


@pytest.mark.asyncio
async def test_event_transformer(sample_sse_message):
    """Test transforming SSE messages to internal events."""
    transformer = EventTransformer()

    internal_events = await transformer.transform(sample_sse_message)

    assert len(internal_events) == 1
    event = internal_events[0]

    assert event.event_id == "event-123"
    assert event.event_type == EventType.UPDATE
    assert event.resource_type == ResourceType.LIGHT
    assert event.resource_id == "light-uuid"
    assert event.data.id == "light-uuid"
    assert event.data.type == ResourceType.LIGHT


@pytest.mark.asyncio
async def test_event_service_start_stop(sample_sse_message):
    """Test starting and stopping event service."""
    mock_producer = MockEventProducer([sample_sse_message])
    transformer = EventTransformer()
    bus = EventBus()

    service = EventService(mock_producer, transformer, bus)

    await service.start_event_stream()
    assert service.is_streaming()

    await service.stop_event_stream()
    assert not service.is_streaming()


@pytest.mark.asyncio
async def test_event_service_end_to_end(sample_sse_message):
    """Test complete event flow from producer to handler."""
    mock_producer = MockEventProducer([sample_sse_message])
    transformer = EventTransformer()
    bus = EventBus()
    service = EventService(mock_producer, transformer, bus)

    received_events = []

    async def handler(event):
        received_events.append(event)

    await service.start_event_stream()

    await service.subscribe_to_events(handler)

    await asyncio.sleep(0.2)

    assert len(received_events) > 0
    assert received_events[0].event_type == EventType.UPDATE

    await service.stop_event_stream()


@pytest.mark.asyncio
async def test_event_service_subscription_management():
    """Test subscription lifecycle."""
    mock_producer = MockEventProducer([])
    transformer = EventTransformer()
    bus = EventBus()
    service = EventService(mock_producer, transformer, bus)

    await service.start_event_stream()

    async def handler(event):
        pass

    sub_id = await service.subscribe_to_events(handler)
    assert sub_id is not None

    result = await service.unsubscribe_from_events(sub_id)
    assert result is True

    result = await service.unsubscribe_from_events(sub_id)
    assert result is False

    await service.stop_event_stream()


@pytest.mark.asyncio
async def test_complete_event_workflow():
    """Complete integration test of event system."""

    event_dto = EventDTO(
        creationtime=datetime.now(timezone.utc),
        id="test-event",
        type=EventType.UPDATE,
        data=[
            EventDataDTO(
                id="light-1",
                type=ResourceType.LIGHT,
                data={"on": {"on": True}},
            ),
            EventDataDTO(
                id="light-2",
                type=ResourceType.LIGHT,
                data={"brightness": {"brightness": 50.0}},
            ),
        ],
    )

    sse_message = EventStreamMessageDTO(
        id="msg-1",
        data=[event_dto],
        timestamp=datetime.now(timezone.utc),
    )

    producer = MockEventProducer([sse_message])
    transformer = EventTransformer()
    bus = EventBus()
    service = EventService(producer, transformer, bus)

    light_events = []

    async def light_handler(event):
        light_events.append(event)

    await service.start_event_stream()

    light_filter = EventFilterDTO(resource_types=[ResourceType.LIGHT])
    await service.subscribe_to_events(light_handler, light_filter)

    await asyncio.sleep(0.2)

    assert len(light_events) == 2
    assert all(e.resource_type == ResourceType.LIGHT for e in light_events)
    assert light_events[0].resource_id == "light-1"
    assert light_events[1].resource_id == "light-2"

    await service.stop_event_stream()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
