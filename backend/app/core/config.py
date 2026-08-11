"""Declare the application settings model and a factory that builds it.

Nine settings are declared and none carries an explicit default. Seven are
required, because the two `Optional[str]` fields default to `None` under
Pydantic 1.x, where `BaseSettings` also still lives. The seven must arrive
from the environment or from a `.env` file the repository does not commit.

The module creates no module-level `settings` instance, and eight modules
import one by name, which is what stops the backend importing.
`core/security.py:L22` imports the `get_settings` factory instead.

Six further settings are read elsewhere and declared nowhere:
`ALLOWED_ORIGINS`, `PROJECT_ID`, `STORAGE_BUCKET_NAME`,
`SIGNED_URL_EXPIRATION`, `EXPORT_BUCKET_NAME` and `DOCUMENT_BUCKET_NAME`.
See ./README.md for the full settings table.
"""
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Hold the settings the application reads from its environment.

    Seven fields are required, the two `Optional[str]` fields default to
    `None`, and `API_V1_STR` is declared but read by no module. `SECRET_KEY`,
    `ALGORITHM` and `ACCESS_TOKEN_EXPIRE_MINUTES` carry no bound or range check.

    Attributes:
        PROJECT_NAME: Display name for the application.
        API_V1_STR: Intended version prefix. No router uses it.
        SECRET_KEY: Key material for signing and verifying tokens.
        ACCESS_TOKEN_EXPIRE_MINUTES: Token lifetime in minutes.
        ALGORITHM: Name of the JSON Web Token signing algorithm.
        GOOGLE_CLOUD_PROJECT: Optional Google Cloud project identifier,
            read by the Firestore client.
        GOOGLE_APPLICATION_CREDENTIALS: Optional path to a service-account
            key file.
        DATABASE_URL: SQLAlchemy connection string, read by `app/db/sql.py`.
        REDIS_URL: Celery broker URL, read by `app/tasks/`.
    """
    PROJECT_NAME: str
    API_V1_STR: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    GOOGLE_CLOUD_PROJECT: Optional[str]
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str]
    DATABASE_URL: str
    REDIS_URL: str

    class Config:
        """Load missing settings from the `.env` file.

        Pydantic reads this file for any value the environment does not
        supply.

        Attributes:
            env_file: `.env`, which the repository does not commit.
            env_file_encoding: `utf-8`.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    """Build a fresh `Settings` instance from the environment.

    The factory is uncached, so each call re-reads the environment and the
    `.env` file. `app/core/security.py` calls it once per function call.

    Returns:
        A new `Settings`.

    Raises:
        ValidationError: When any of the seven required fields is absent
            from both the environment and the `.env` file.
    """
    return Settings()