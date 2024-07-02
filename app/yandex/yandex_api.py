import asyncio
from json import dumps, JSONDecodeError

from aiohttp import ClientSession

from settings import logger
from misc import InvalidDiskLink, Folder


class YandexDiskImagesParser:
    API_GET_URL = f"https://cloud-api.yandex.net/v1/disk/public/resources"

    async def get_folder_content(
            self,
            params: dict,
            names_list: list[str],
            counter: int = 0,
            max_depth: int = 3,
    ) -> list[str] | list[list]:
        if counter >= max_depth:
            return []
        counter += 1
        async with ClientSession() as session:
            async with session.get(self.API_GET_URL, params=params) as request:
                if request.status != 200:
                    if counter == 1:
                        raise InvalidDiskLink(f"Invalid Disk link! {params['public_key']}")
                    else:
                        return []
                images = []
                folders = []
                try:
                    folder_json = await request.json()
                    items = folder_json.get("_embedded").get("items")
                    if not items:
                        if counter == 1:
                            raise InvalidDiskLink("Empty folder")
                    for item in items:
                        if item.get("media_type") == "image":
                            images.append(item.get("file"))
                            continue
                        elif item.get("type") == "dir":
                            name = item.get("name")
                            if names_list and (name not in names_list):
                                logger.debug(f"Name {name} not in folder names list. Skipping.")
                                continue
                            elif names_list:
                                names_list.remove(name)
                            path = item.get("path")
                            public_key = item.get("public_key")
                            params = {"public_key": public_key, "path": path}
                            folders.append(await self.get_folder_content(params, names_list, counter, max_depth))
                except JSONDecodeError:
                    logger.error("Site responded with invalid json")
                    if counter == 1:
                        raise
                images.extend(folders)
                return images

    async def get_image_urls(
            self,
            main_public_key: str,
            searched_folders: list[str] | None = None,
            max_depth: int = 3,
    ):
        params = {"public_key": main_public_key}
        logger.warning(f"{params}")
        images = await self.get_folder_content(params, searched_folders, max_depth=max_depth)
        return images
