from enum import Enum
import os

from pydantic_settings import BaseSettings


class AppEnvironment(str, Enum):
    """Enum for app environments."""

    LOCAL = "local"
    PREVIEW = "preview"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application settings."""

    OPENAPI_URL: str | None = None
    AWS_KEY: str | None = None
    AWS_SECRET: str | None = None
    API_PREFIX: str = "/api"
    LOG_LEVEL: str = "DEBUG"
    RENDER: bool = False
    IS_PULL_REQUEST: bool = False

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


settings = Settings()
