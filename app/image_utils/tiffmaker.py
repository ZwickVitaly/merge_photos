from os import path
from uuid import uuid4
from math import ceil

from PIL import Image
from PIL.TiffImagePlugin import AppendingTiffWriter

from settings import logger, STATIC_FILES_DIR


class TiffMaker:

    async def get_frames(
            self,
            list_of_folders: list[list[str]],
            row_len: int = 0,
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
            new_frames: list[Image] = await self.self_merge_images(
                images=folder,
                row_len=row_len,
                width=width,
                height=height,
                gap=gap,
                bg_color=bg_color,
                max_images=max_images_per_page,
            )
            frames.extend(new_frames)
        return frames

    @staticmethod
    async def self_merge_images(
            images: list[Image],
            row_len: int = 0,
            width: int = 400,
            height: int = 400,
            gap: int = 50,
            bg_color: tuple[int, int, int] = (255, 255, 255),
            max_images: int = 40,
    ):
        logger.debug("Merging frames")
        if len(images) > max_images:
            images = [images[chunk_i: chunk_i + max_images] for chunk_i in range(0, len(images), max_images)]
        else:
            images = [images]
        if len(images[0]) < row_len:
            row_len = len(images[0])
        if row_len <= 0:
            row_len = ceil(len(images[0]) ** 0.5)
        if row_len > max_images:
            row_len = max_images

        merged_frames = []
        for image_seq in images:
            if not image_seq:
                continue
            new_image = Image.new(
                "RGB",
                (
                    row_len * (width + 2 * gap) + 2 * gap,
                    ((len(image_seq) // row_len) or 1) * (height + 2 * gap) + 2 * gap
                ),
                bg_color
            )
            for i, img in enumerate(image_seq):
                img = img.resize((width, height))
                new_image.paste(
                    img, (((i % row_len) * (width + 2 * gap)) + 2 * gap, (i // row_len * (height + 2 * gap)) + 2 * gap),
                )
            merged_frames.append(new_image)
        return merged_frames

    async def make_tiff(
            self,
            links: list[list[Image]],
            filename: str,
            row_len: int = 0,
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
