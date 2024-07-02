from contextlib import asynccontextmanager
from settings import logger


@asynccontextmanager
async def basic_lifespan(*args, **kwargs):
    logger.warning("App started")
    yield
    logger.warning("App finished")