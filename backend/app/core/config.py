"""Declare the application settings model and its construction helper.

The module does not export the settings singleton imported elsewhere.
No backend manifest pins Pydantic. BaseSettings requires Pydantic 1.x, whose
reviewed secure floor is 1.10.13 because earlier releases include
CVE-2024-3772.
"""
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Declare nine configuration fields loaded from the environment.

    Pydantic reads each field from the process environment or from the file
    named in the nested `Config` class. No field carries an explicit default,
    so the seven fields typed `str` or `int` are required. The two
    `Optional[str]` fields default to `None`.

    No validator constrains secret-key strength, the algorithm name, token
    lifetime, or either connection URL. Required values are not necessarily
    safe values.

    Attributes:
        PROJECT_NAME: Project display name.
        API_V1_STR: Route path version prefix.
        SECRET_KEY: Signing key for JSON Web Tokens.
        ACCESS_TOKEN_EXPIRE_MINUTES: Access token lifetime in minutes.
        ALGORITHM: JSON Web Token signing algorithm.
        GOOGLE_CLOUD_PROJECT: Google Cloud project identifier.
        GOOGLE_APPLICATION_CREDENTIALS: Path to an Application Default
            Credentials configuration, including federation configuration or
            a service-account key.
        DATABASE_URL: SQLAlchemy connection string.
        REDIS_URL: Celery broker URL.
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
        """Point Pydantic at the environment file that supplies the settings.

        `env_file` names `.env`, and the repository commits no such file, so
        Pydantic resolves every field from the process environment alone.
        `env_file_encoding` decodes the named file as UTF-8.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    """Build and return a fresh Settings instance.

    The function caches nothing, so every call re-reads and re-validates the
    environment.

    Returns:
        A Settings instance populated from the environment.

    Raises:
        pydantic.ValidationError: If a required field is absent from both the
            process environment and the uncommitted `.env` file.
    """
    return Settings()