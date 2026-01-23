import asyncio
import logging

from pyhuec.hue_client_factory import HueClientFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    client = await HueClientFactory.create_client()

    lights = await client.get_lights()
    logger.info(f"Found {len(lights.data)} lights")

    for light in lights.data:
        name = light.metadata.name if light.metadata else light.id
        is_on = light.on.get("on", False)
        brightness = light.dimming.brightness if light.dimming else "N/A"
        logger.info(f"  {name}: {'ON' if is_on else 'OFF'} (brightness: {brightness}%)")

    if lights.data:
        first_light = lights.data[0]
        light_name = (
            first_light.metadata.name if first_light.metadata else first_light.id
        )

        logger.info(f"Turning on {light_name} at 50% brightness...")
        await client.turn_on_light(first_light.id, brightness=50.0)

        await asyncio.sleep(2)

        logger.info(f"Setting {light_name} to 100% brightness...")
        await client.turn_on_light(first_light.id, brightness=100.0)

        await asyncio.sleep(2)

        logger.info(f"Turning off {light_name}...")
        await client.turn_off_light(first_light.id)

        logger.info("Done!")


if __name__ == "__main__":
    asyncio.run(main())
