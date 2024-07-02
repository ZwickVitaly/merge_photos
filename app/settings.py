from os import getenv
from pathlib import Path
from sys import stdout
from loguru import logger


DEBUG = getenv("DEBUG", "0") == "1"

BASE_DIR = Path(__file__).parent

STATIC_FILES_DIR = BASE_DIR.parent / "media"
STATIC_FILES_DIR.mkdir(exist_ok=True)

logger.remove()
logger.add(stdout, level="DEBUG" if DEBUG else "INFO")