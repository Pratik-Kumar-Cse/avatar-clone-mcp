import logging
from avatar_clone.services.heygen import HeygenService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

heygen_service = HeygenService()


async def clone_avatar(name, image_url, platform):
    logger.info(
        f"Starting avatar cloning for name: {name}, image_url: {image_url}, platform: {platform}"
    )
    try:
        # Your cloning logic here
        pass
    except Exception as e:
        logger.error(f"Error occurred while cloning avatar: {e}")
        raise
    logger.info("Avatar cloning completed successfully")
