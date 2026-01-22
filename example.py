import asyncio
import logging
from asyncio import CancelledError
from pyhuec.hue_client_factory import HueClientFactory


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    try:
        logger.info("Connecting to Hue Bridge...")
        client = await HueClientFactory.create_client()
        
        logger.info("Fetching lights...")
        lights = await client.get_lights()
        logger.info(f"Found {len(lights.data)} lights")
        
        if lights.data:
            light = lights.data[0]
            logger.info(f"Turning on: {light.metadata.name if light.metadata else light.id}")
            await client.turn_on_light(light.id, brightness=100)
        
        logger.info("Starting event stream (Press Ctrl-C to stop)...")
        await client.start_event_stream()
        
        await client.subscribe_to_light_events(
            lambda event: logger.info(f"Event: {event.event_type} - {event.resource_id}")
        )
        
        while True:
            await asyncio.sleep(1)
        

    except (KeyboardInterrupt, CancelledError):
        logger.info("Shutting down...")
        await client.stop_event_stream()
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()



if __name__ == '__main__':
    asyncio.run(main())