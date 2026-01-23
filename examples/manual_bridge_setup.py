import asyncio
import logging

from pyhuec.hue_client_factory import HueClientFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    client = await HueClientFactory.create_client(
        bridge_ip="your-ipv4-bridge-address",
        api_key="your-api-key-here",
        enable_events=False,
        enable_cache=False,
        auto_sync=False,
        http_timeout=15.0,
    )

    logger.info("Connected")

    lights = await client.get_lights()
    logger.info(f"Found {len(lights.data)} lights")

    for light in lights.data:
        name = light.metadata.name if light.metadata else light.id
        is_on = light.on.get("on", False)
        logger.info(f"  {name}: {'ON' if is_on else 'OFF'}")


if __name__ == "__main__":
    asyncio.run(main())
