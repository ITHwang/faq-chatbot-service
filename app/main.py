import logging
import sys

from fastapi import FastAPI
import uvicorn

from app.api import api_router
from app.core import settings
from app.data.etl import extract_transform_load

logger = logging.getLogger(__name__)


def __setup_logging(log_level: str):
    log_level = getattr(logging, log_level.upper())
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    root_logger.addHandler(stream_handler)
    logger.info(f"Set up logging with log level {log_level}")


def __setup_db(pkl_path: str, db_path: str, collection_name: str):
    extract_transform_load(pkl_path, db_path, collection_name)


app = FastAPI()

app.include_router(api_router, prefix=settings.API_PREFIX)


def start():
    """Launched with `poetry run start` at root level."""

    print("Running in AppEnvironment: " + settings.ENVIRONMENT.value)

    __setup_logging(settings.LOG_LEVEL)
    __setup_db(settings.PKL_PATH, settings.DB_PATH, settings.COLLECTION_NAME)

    live_reload = not settings.RENDER

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=live_reload,
        workers=settings.UVICORN_WORKER_COUNT,
    )
