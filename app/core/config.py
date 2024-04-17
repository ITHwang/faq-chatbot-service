from enum import Enum
import os
from pathlib import Path

from pydantic_settings import BaseSettings


class AppEnvironment(str, Enum):
    """Enum for app environments."""

    LOCAL = "local"
    PREVIEW = "preview"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application settings."""

    OPENAI_API_KEY: str
    # AWS_KEY: str | None = None
    # AWS_SECRET: str | None = None
    API_PREFIX: str = "/api"
    LOG_LEVEL: str = "DEBUG"
    RENDER: bool = False
    IS_PULL_REQUEST: bool = False

    # See https://docs.llamaindex.ai/en/stable/module_guides/loading/documents_and_nodes/usage_documents
    METADATA_SEPERATOR: str = "\n"
    METADATA_TEMPLATE: str = "{key}: {value}"
    TEXT_TEMPLATE: str = "{metadata_str}\n\n{content}"

    # See https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/sentence_splitter
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 128

    BASE_PATH: Path = Path(__file__).parent.parent
    PKL_PATH: str = str(BASE_PATH / "data" / "raw" / "final_result.pkl")
    DB_PATH: str = str(BASE_PATH / "data" / "db")
    COLLECTION_NAME: str = "qna"

    TOP_K: int = 5

    @property
    def ENVIRONMENT(self) -> AppEnvironment:
        """
        Returns the app environment.
        """
        if self.RENDER:
            if self.IS_PULL_REQUEST:
                return AppEnvironment.PREVIEW
            else:
                return AppEnvironment.PRODUCTION
        else:
            return AppEnvironment.LOCAL

    @property
    def UVICORN_WORKER_COUNT(self) -> int:
        if self.ENVIRONMENT == AppEnvironment.LOCAL:
            return 1
        # The recommended number of workers is (2 x $num_cores) + 1:
        # Source: https://docs.gunicorn.org/en/stable/design.html#how-many-workers
        # But the Render.com servers don't have enough memory to support that many workers,
        # so we instead go by the number of server instances that can be run given the memory
        return 3

    @property
    def VERBOSE(self) -> bool:
        """
        Used for setting verbose flag in LlamaIndex modules.
        """
        return self.LOG_LEVEL == "DEBUG" or self.IS_PULL_REQUEST or not self.RENDER

    class Config:
        work_dir = Path(__file__).parent.parent.parent
        env_file = str(work_dir / ".env.development")


settings = Settings()
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
