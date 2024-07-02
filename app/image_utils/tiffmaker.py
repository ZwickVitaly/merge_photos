from os import path
from uuid import uuid4

from PIL import Image
from PIL.TiffImagePlugin import AppendingTiffWriter

from settings import logger, STATIC_FILES_DIR


class TiffMaker:

    async def get_frames(
            self,
            list_of_folders: list[list[str]],
            row_len: int = 4,
            width: int = 400,
            height: int = 400,
            gap: int = 50,
            bg_color: tuple[int, int, int] = (255, 255, 255),
            max_images_per_page: int = 40,
    ):
        logger.debug("Getting frames")
        frames = []
        if not list_of_folders:
            return None
        for folder in list_of_folders:
            frame: Image = await self.self_merge_images(
                images=folder,
                row_len=row_len,
                width=width,
                height=height,
                gap=gap,
                bg_color=bg_color,
                max_images=max_images_per_page,
            )
            frames.append(frame)
        return frames

    @staticmethod
    async def self_merge_images(
            images: list[Image],
            row_len: int = 4,
            width: int = 400,
            height: int = 400,
            gap: int = 50,
            bg_color: tuple[int, int, int] = (255, 255, 255),
            max_images: int = 40,
    ):
        logger.debug("Merging frames")
        if len(images) > max_images:
            return None
        if len(images) < row_len:
            row_len = len(images)
        new_image = Image.new(
            "RGB",
            (
                row_len * (width + 2 * gap) + 2 * gap,
                ((len(images) // row_len) or 1) * (height + 2 * gap) + 2 * gap
            ),
            bg_color
        )
        for i, img in enumerate(images):
            img = img.resize((width, height))
            new_image.paste(
                img, (((i % row_len) * (width + 2 * gap)) + 2 * gap, (i // row_len * (height + 2 * gap)) + 2 * gap),
            )
        return new_image

    async def make_tiff(
            self,
            links: list[list[Image]],
            filename: str,
            row_len: int = 4,
            width: int = 400,
            height: int = 400,
            gap: int = 50,
            bg_color: tuple[int, int, int] = (255, 255, 255),
            max_images_per_page: int = 40,
    ):
        images_for_frames = await self.get_frames(
            links,
            row_len=row_len,
            width=width,
            height=height,
            gap=gap,
            bg_color=bg_color,
            max_images_per_page=max_images_per_page,
        )
        if not images_for_frames:
            return None
        if path.exists(f"{STATIC_FILES_DIR}/{filename}"):
            filename += f"_{uuid4()}"
            logger.debug(f"Making {filename}")
        with AppendingTiffWriter(f"{STATIC_FILES_DIR}/{filename}") as tr:
            for frame in images_for_frames:
                if frame:
                    frame.save(tr)
                    tr.newFrame()
