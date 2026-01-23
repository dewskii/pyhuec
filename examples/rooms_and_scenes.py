import asyncio
import logging

from pyhuec.hue_client_factory import HueClientFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    client = await HueClientFactory.create_client()

    logger.info("Fetching rooms...")
    rooms = await client.get_rooms()
    logger.info(f"Found {len(rooms.data)} rooms:")

    for room in rooms.data:
        name = room.metadata.name if room.metadata else room.id
        logger.info(f"  - {name}")

    logger.info("\nFetching scenes...")
    scenes = await client.get_scenes()
    logger.info(f"Found {len(scenes.data)} scenes:")

    for scene in scenes.data:
        name = scene.metadata.name if scene.metadata else scene.id
        logger.info(f"  - {name}")

    if scenes.data:
        first_scene = scenes.data[0]
        scene_name = (
            first_scene.metadata.name if first_scene.metadata else first_scene.id
        )

        logger.info(f"\nActivating scene: {scene_name}...")
        await client.recall_scene(first_scene.id)
        logger.info("Scene activated!")


if __name__ == "__main__":
    asyncio.run(main())
