"""Declare the application settings model and the factory that builds it.

Both imports resolve. `BaseSettings` ships in the main Pydantic package only
in Pydantic 1.x, so importing the name here pins the backend to that major
version. `Optional` annotates the `GOOGLE_CLOUD_PROJECT` and
`GOOGLE_APPLICATION_CREDENTIALS` fields below.

Dependency limitation. The repository commits no backend dependency manifest.
No `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `Pipfile`,
`tox.ini` or `.python-version` is tracked, so nothing records which Pydantic
release the L1 import resolves against and nothing excludes a vulnerable one.
The `BaseSettings` import at L1 requires Pydantic 1.x, while Pydantic 2.x is
the current major release, so a resolver that takes the newest version breaks
this module. Reviewed secure floor for the pinned major: Pydantic 1.10.13 or
later, because releases below it carry the regular-expression denial-of-service
advisory GHSA-mr82-8j83-vxmv (CVE-2024-3772). Selecting a version and adding a
manifest are code changes and stay outside this documentation pass.

The module never defines a module-level `settings` instance. Eight modules
import that name from here, so each import raises ImportError:
`app/api/auth.py:L6`, `app/db/firestore.py:L3`, `app/db/sql.py:L3`,
`app/main.py:L7`, `app/services/collaboration_service.py:L4`,
`app/services/document_service.py:L5`, `app/services/export_service.py:L3`
and `app/tasks/background_tasks.py:L3`. Seven of the eight dereference the
name; `app/services/document_service.py` imports it and never uses it.
`app/core/security.py:L6` imports the `get_settings` factory below instead,
and that factory does exist.

Line locators: every `Lnn` reference below numbers the tree at commit
06be74c7c88aa6bca652d465eaa00ad480a9e5c5, the frozen revision that precedes this
documentation pass. A bare `Lnn` points into this file, and a `path:Lnn` points into
the named file. Current HEAD numbers each documented file higher.
"""
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Declare the nine configuration fields this model can load from the environment.

    Pydantic populates each key from the process environment or from the file
    named in the nested `Config` class. No field carries an explicit default,
    so the seven keys typed `str` or `int` are strictly required. The two
    `Optional[str]` fields receive an implicit `None` under Pydantic 1.x and
    stay optional.

    Required is not the same as validated. Every field carries a bare `str` or
    `int` annotation. No field uses `Field(...)` with a bound, no regular
    expression constrains a value, and the class declares no `@validator`, so
    Pydantic checks the type and nothing else. Verified consequences, each
    confirmed by constructing the model directly:

    - `SECRET_KEY` accepts the empty string and any short or low-entropy value.
      A caller who signs with a guessable key produces JSON Web Tokens that an
      attacker can forge, and `app/core/security.py:L19` and
      `app/api/auth.py:L37` both sign with whatever this field holds.
    - `ALGORITHM` accepts any string, including `none`. Nothing restricts the
      value to a signing algorithm the deployment intends.
    - `ACCESS_TOKEN_EXPIRE_MINUTES` accepts `0` and negative integers, and
      carries no upper bound. A zero or negative value yields a token whose
      `exp` claim is already in the past, and a large value yields a token that
      effectively never expires.
    - `DATABASE_URL` and `REDIS_URL` accept any string. Neither is parsed as a
      Uniform Resource Locator (URL) at this layer, so a malformed value passes
      settings validation and fails later, at `app/db/sql.py:L5` for the
      database and at `app/tasks/background_tasks.py:L9` for the broker.

    Adding constraints or validators would change the settings model, so this
    pass records the gap and leaves the model as committed.

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
        GOOGLE_APPLICATION_CREDENTIALS: Path to a Google credential
            configuration file that Application Default Credentials accepts,
            including a workload or workforce identity federation
            configuration or a service-account key. No code reads the field
            from `Settings`. The Google authentication library reads the
            operating-system environment variable of the same name through
            Application Default Credentials at `app/db/firestore.py:L6`.
            `scripts/deploy.sh:L4` guards on that same variable.
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
    The function has two callers, at `app/core/security.py:L12` and
    `app/core/security.py:L33`.

    Returns:
        A Settings instance populated from the environment.

    Raises:
        pydantic.ValidationError: If any of the seven required fields is
            absent from both the process environment and the uncommitted
            `.env` file.
    """
    return Settings()