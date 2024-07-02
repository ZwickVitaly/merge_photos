from uuid import uuid4
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse

from api.lifespan import basic_lifespan
from yandex import YandexDiskImagesParser, ImageDownloader
from image_utils import TiffMaker
from settings import logger
from misc import SearchParams, FinalLink, ErrorResponse

app = FastAPI(lifespan=basic_lifespan)
parser = YandexDiskImagesParser()
image_downloader = ImageDownloader()
tiff_maker = TiffMaker()


@app.post("/make-tiff", responses={200: {"model": FinalLink}, 403: {"model": ErrorResponse}})
async def browse_ya_disk(search_params: SearchParams, request: Request, bg_task: BackgroundTasks):
    """
    Кидай ссылку на яндекс-диск, получи картинки, сшитые в разные tiff-файлы по папкам
    Обрати внимание на доп. параметры
    Диск должен быть публичным
    """
    logger.debug(f"User request url: {search_params.disk_url}")
    filename = f"{str(uuid4())}.tiff"
    try:
        links = await parser.get_image_urls(search_params.disk_url, search_params.searched_dirs)
        images = await image_downloader.download_images(links=links)
        await tiff_maker.make_tiff(
            images,
            filename,
            row_len=search_params.row_len,
            width=search_params.width,
            height=search_params.height,
            gap=search_params.gap,
            bg_color=search_params.bg_color,
            max_images_per_page=search_params.max_images_per_page,
        )
        logger.info(f"Successfully made {filename} file")
        return FinalLink(link=f"{request.url.netloc}/media/{filename}")
    except Exception as e:
        logger.error(f"{e}")
        return JSONResponse(status_code=403, content={"error": str(e.args[0])})

