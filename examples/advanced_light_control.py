import asyncio
import logging

from pyhuec.hue_client_factory import HueClientFactory
from pyhuec.models.dto.light_dto import ColorTemperatureDTO, LightUpdateDTO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    client = await HueClientFactory.create_client()

    lights = await client.get_lights()

    if not lights.data:
        logger.warning("No lights found!")
        return

    first_light = lights.data[0]
    light_name = first_light.metadata.name if first_light.metadata else first_light.id

    logger.info(f"\nGetting details for: {light_name}")
    light_detail = await client.get_light(first_light.id)

    logger.info(f"  ID: {light_detail.id}")
    logger.info(f"  On: {light_detail.on.get('on', False)}")
    if light_detail.dimming:
        logger.info(f"  Brightness: {light_detail.dimming.brightness}%")
    if light_detail.color_temperature:
        logger.info(f"  Color Temp: {light_detail.color_temperature.mirek} mirek")

    logger.info(f"\nFlashing {light_name} to identify it...")
    await client.identify_light(first_light.id)

    await asyncio.sleep(3)

    if light_detail.color_temperature:
        logger.info(f"\nSetting {light_name} to warm white...")
        update = LightUpdateDTO(
            on={"on": True}, color_temperature=ColorTemperatureDTO(mirek=400)
        )
        await client.update_light(first_light.id, update)

        await asyncio.sleep(3)

        logger.info(f"Setting {light_name} to cool white...")
        update = LightUpdateDTO(color_temperature=ColorTemperatureDTO(mirek=200))
        await client.update_light(first_light.id, update)

        await asyncio.sleep(3)

    logger.info("Done!")


if __name__ == "__main__":
    asyncio.run(main())
