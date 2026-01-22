"""
Event transformer for converting raw server sent messages to internal events.
"""

import logging
from typing import List

from pyhuec.models.dto.event_dto import (
    EventStreamMessageDTO,
    InternalEventDTO,
)
from pyhuec.models.protocols.event_protocols import EventTransformerProtocol

logger = logging.getLogger(__name__)


class EventTransformer(EventTransformerProtocol):
    """
    Transforms raw Hue Bridge SSE messages into internal event format.

    This transformer flattens the nested structure of SSE messages and
    creates individual internal events for each resource change.
    """

    async def transform(
        self, raw_message: EventStreamMessageDTO
    ) -> List[InternalEventDTO]:
        """
        Transform raw SSE message to internal events.

        Args:
            raw_message: Raw event stream message from bridge

        Returns:
            List of processed internal events
        """
        internal_events: List[InternalEventDTO] = []

        try:
            for event in raw_message.data:
                for event_data in event.data:
                    try:
                        internal_event = InternalEventDTO.model_construct(
                            event_id=event.id,
                            event_type=event.type,
                            resource_type=event_data.type,
                            resource_id=event_data.id,
                            timestamp=event.creationtime,
                            data=event_data,
                            metadata={
                                "sse_message_id": raw_message.id,
                                "received_at": raw_message.timestamp.isoformat()
                                if raw_message.timestamp
                                else None,
                                "legacy_id": event_data.id_v1,
                                "owner": event_data.owner.model_dump()
                                if event_data.owner
                                else None,
                            },
                        )
                        internal_events.append(internal_event)

                    except Exception as e:
                        logger.error(
                            f"Error creating internal event for resource "
                            f"{event_data.id}: {e}",
                            exc_info=True,
                        )
                        continue

        except Exception as e:
            logger.error(f"Error transforming SSE message: {e}", exc_info=True)

        logger.debug(f"Transformed {len(internal_events)} internal events")
        return internal_events
