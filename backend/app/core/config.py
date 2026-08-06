"""Declare the application settings model and the factory that builds it.

Nine modules import a module-level `settings` object from here, and this module defines
none. Importing any of those modules therefore raises `ImportError`, which is the first
failure a backend run hits.

Dependency limitation. The repository commits no backend dependency manifest.
No `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `Pipfile`,
`tox.ini` or `.python-version` is tracked, so nothing records which Pydantic
release the L1 import resolves against and nothing excludes a vulnerable one.
The `BaseSettings` import at L1 requires Pydantic 1.x, while Pydantic 2.x is
the current major release, so a resolver that takes the newest version breaks
this module. Reviewed secure floor for the pinned major: Pydantic 1.10.13 or
later, because releases below it carry the regular-expression denial-of-service
advisory GHSA-mr82-8j83-vxmv (CVE-2024-3772). No committed file names a version,
so nothing in the repository selects one.

Deployment coverage. `infrastructure/docker/docker-compose.yml:L23-L24` supplies
exactly one environment key to the `backend` service, `DATABASE_URL`. Seven of
the nine fields below carry no default and are therefore required:
`PROJECT_NAME`, `API_V1_STR`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`,
`ALGORITHM`, `DATABASE_URL` and `REDIS_URL`. Compose covers one of the seven, so
constructing `Settings()` inside that container still fails validation on the
six remaining required keys: `PROJECT_NAME`, `API_V1_STR`, `SECRET_KEY`,
`ACCESS_TOKEN_EXPIRE_MINUTES`, `ALGORITHM` and `REDIS_URL`. Pydantic reports
every missing required field at once, so the container reports all six together.
Restoring the module-level `settings` instance therefore does not make the
committed Compose deployment start.

Six further settings are read at runtime and declared by no field below, so each
raises `AttributeError` at the point of the read even on a fully supplied
environment. The six are `ALLOWED_ORIGINS` at `app/main.py:L118`, `PROJECT_ID` at
`app/services/collaboration_service.py:L120`, `:L21`, `:L50` and `:L60`,
`STORAGE_BUCKET_NAME` at `app/services/export_service.py:L154` and `:L35`,
`SIGNED_URL_EXPIRATION` at `app/services/export_service.py:L162` and `:L43`,
`EXPORT_BUCKET_NAME` at `app/tasks/background_tasks.py:L141`, and
`DOCUMENT_BUCKET_NAME` at `app/tasks/background_tasks.py:L278`. Fifteen settings
are therefore in play: nine declared here and six read but never declared.

`REDIS_URL` has no target in the committed topology even when supplied.
`infrastructure/docker/docker-compose.yml:L3-L39` defines three services,
`frontend`, `backend` and `db`, and names no Redis service, while
`app/tasks/background_tasks.py:L98` builds a Celery broker from that value.

`BaseSettings` lives in the `pydantic` package itself, so this module requires Pydantic
1.x. Pydantic 2 moved the class to `pydantic-settings`.
"""
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Collect the environment-supplied configuration for the backend.

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

    - `SECRET_KEY` accepts the empty string and any short or low-entropy value,
      and `app/core/security.py:L81` and `app/api/auth.py:L240` both sign with
      whatever the field holds. The consequence depends on which algorithm
      `ALGORITHM` names. Under a symmetric algorithm such as HS256, this one
      value both signs and verifies, so a guessable key lets an attacker forge
      a JSON Web Token that `app/core/security.py:L181` and
      `app/api/auth.py:L158` accept. Under an asymmetric algorithm such as
      RS256, the two signing sites need a private key here while the two
      verifying sites need a public key, so a short value forges nothing and
      the operation fails instead. One field serves both roles, and nothing
      pairs it with the algorithm the deployment names.
    - `ALGORITHM` accepts any string, including `none`. Nothing restricts the
      value to a signing algorithm the deployment intends.
    - `ACCESS_TOKEN_EXPIRE_MINUTES` accepts `0` and negative integers, and
      carries no upper bound. A zero or negative value yields a token whose
      `exp` claim is already in the past, and a large value yields a token that
      effectively never expires.
    - `DATABASE_URL` and `REDIS_URL` accept any string. Neither is parsed as a
      Uniform Resource Locator (URL) at this layer, so a malformed value passes
      settings validation and fails later, at `app/db/sql.py:L16` for the
      database and at `app/tasks/background_tasks.py:L98` for the broker.

    The model as committed accepts every value listed above, so each consequence
    surfaces at the reading site rather than at settings construction.

    Attributes:
        PROJECT_NAME: Display name for the application. Required.
        API_V1_STR: Version prefix for the API. Required, and read by no module.
        SECRET_KEY: Signing key for JSON Web Tokens. Required, with no length bound and
            no default.
        ACCESS_TOKEN_EXPIRE_MINUTES: Token lifetime in minutes. Required.
        ALGORITHM: Signing algorithm name. Required, with no allowed-value check.
        GOOGLE_CLOUD_PROJECT: Google Cloud project identifier. Optional, and passed to
            the Firestore client.
        GOOGLE_APPLICATION_CREDENTIALS: Path to a service-account key file. Optional.
        DATABASE_URL: SQLAlchemy connection string. Required.
        REDIS_URL: Celery broker and backend URL. Required, and no Redis service is
            declared in Compose or in the Terraform.

    Note:
        Seven of the nine fields are required and carry no default, so constructing
        `Settings()` without a complete environment raises `ValidationError`. No field
        declares a validator, so any non-empty string satisfies `SECRET_KEY` and
        `ALGORITHM`.
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
        """Point Pydantic at the `.env` file and its encoding."""
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    """Build a fresh `Settings` instance from the current environment.

    Returns:
        A new `Settings`, constructed on every call.

    Raises:
        ValidationError: When any of the seven required fields is absent from both the
            environment and the `.env` file.

    Note:
        Carries no caching decorator, so each call re-reads the environment and rebuilds
        the model. `app/core/security.py` calls it once per function invocation.
    """
    return Settings()