from io import BytesIO

from aiohttp import ClientSession
from PIL import Image
from settings import logger


class ImageDownloader:

    async def download_images(self, links: list[str]) -> list[Image]:
        logger.debug("Downloading images")
        images = []
        if not list:
            return images
        async with ClientSession() as session:
            for url in links:
                if isinstance(url, list):
                    images.append(await self.download_images(url))
                    continue
                elif not isinstance(url, str):
                    continue
                async with session.get(url) as request:
                    img_bytes = await request.content.read()
                    image = Image.open(BytesIO(img_bytes), formats=["JPEG", "PNG", "TIFF"])
                    images.append(image)
        return images
