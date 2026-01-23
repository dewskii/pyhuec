import asyncio
import logging

from pyhuec.hue_client_factory import HueClientFactory
from pyhuec.models.dto.event_dto import EventFilterDTO, ResourceType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    client = await HueClientFactory.create_client(enable_events=True)

    try:
        logger.info("Starting event stream...")
        await client.start_event_stream()

        await client.subscribe_to_light_events(
            lambda event: logger.info(
                f"Light event: {event.event_type.value} - {event.resource_id}"
            )
        )

        def log_all_events(event):
            logger.info(
                f"Event: [{event.resource_type.value}] "
                f"{event.event_type.value} - {event.resource_id}"
            )

        await client.subscribe_to_events(log_all_events)

        motion_filter = EventFilterDTO(resource_types=[ResourceType.MOTION])
        await client.subscribe_to_events(
            lambda event: logger.info(f"Motion detected: {event.resource_id}"),
            event_filter=motion_filter,
        )

        logger.info("Listening for events (Press Ctrl-C to stop)...")

        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        await client.stop_event_stream()
        logger.info("Done!")


if __name__ == "__main__":
    asyncio.run(main())
