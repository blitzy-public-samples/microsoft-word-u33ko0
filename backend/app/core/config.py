"""Declare the application settings model and the factory that builds it.

Both imports resolve. `BaseSettings` ships in the main Pydantic package only
in Pydantic 1.x, so importing the name here pins the backend to that major
version. `Optional` annotates the `GOOGLE_CLOUD_PROJECT` and
`GOOGLE_APPLICATION_CREDENTIALS` fields below.

The module never defines a module-level `settings` instance. Eight modules
import that name from here, so each import raises ImportError:
`app/api/auth.py:L6`, `app/db/firestore.py:L3`, `app/db/sql.py:L3`,
`app/main.py:L7`, `app/services/collaboration_service.py:L4`,
`app/services/document_service.py:L5`, `app/services/export_service.py:L3`
and `app/tasks/background_tasks.py:L3`. Seven of the eight dereference the
name; `app/services/document_service.py` imports it and never uses it.
`app/core/security.py:L6` imports the `get_settings` factory below instead,
and that factory does exist.
"""
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Declare the nine configuration keys the backend reads from its environment.

    Pydantic populates each key from the process environment or from the file
    named in the nested `Config` class. No field carries an explicit default,
    so the seven keys typed `str` or `int` are strictly required. The two
    `Optional[str]` fields receive an implicit `None` under Pydantic 1.x and
    stay optional.

    Attributes:
        PROJECT_NAME: Project display name. No code reads the field;
            `app/main.py:L55` assigns `app.title` a string literal instead.
        API_V1_STR: Route path version prefix. The name appears once in the
            repository, at its own declaration, so no code reads the field.
        SECRET_KEY: Signing key for JSON Web Tokens, read at
            `app/core/security.py:L19` and `:L35` and at
            `app/api/auth.py:L16` and `:L37`.
        ACCESS_TOKEN_EXPIRE_MINUTES: Access token lifetime in minutes, read
            at `app/core/security.py:L17` and `app/api/auth.py:L34`.
        ALGORITHM: JSON Web Token signing algorithm, read at
            `app/core/security.py:L19` and `:L35` and at
            `app/api/auth.py:L16` and `:L38`.
        GOOGLE_CLOUD_PROJECT: Google Cloud project identifier, read at
            `app/db/firestore.py:L7` to construct the Firestore client.
        GOOGLE_APPLICATION_CREDENTIALS: Path to a service account key file.
            No code reads the field from `Settings`. The Google authentication
            library reads the operating-system environment variable of the
            same name through Application Default Credentials at
            `app/db/firestore.py:L6`. `scripts/deploy.sh:L4` guards on that
            same variable.
        DATABASE_URL: SQLAlchemy connection string, read at
            `app/db/sql.py:L5`.
        REDIS_URL: Celery broker URL, read at
            `app/tasks/background_tasks.py:L9`.
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

    The function caches nothing. No `functools.lru_cache` decorates it and no
    module-level memo holds the result, so every call constructs a new
    `Settings` and re-runs the environment read and validation.
    `app/core/security.py` calls the function twice, at L12 and L33.

    Returns:
        A Settings instance populated from the environment.

    Raises:
        pydantic.ValidationError: If any of the seven required fields is
            absent from both the process environment and the uncommitted
            `.env` file.
    """
    return Settings()