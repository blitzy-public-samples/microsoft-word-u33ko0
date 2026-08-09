# backend/app/core

## Purpose

`core/` holds two modules: application configuration and the authentication primitives. `config.py` declares a
Pydantic `BaseSettings` model with nine configuration keys at `config.py:L20-L48`, plus a `get_settings()` factory at
`config.py:L63`. `security.py` declares a password-hashing context at `security.py:L24`, a bearer-token scheme at
`security.py:L25`, and four functions covering JSON Web Token (JWT) issuance, password verification, password hashing,
and request-time user resolution.

Nothing in the repository imports `app.core.security`. A search for `core.security` across every committed source and
configuration file returns no result, so all four functions in that module have zero callers. The twelve protected
routes take their `get_current_user` dependency from `app.api.auth` instead, at `api/documents.py:L19`,
`api/templates.py:L19` and `api/users.py:L15`. `config.py` is consumed; `security.py` is not.

## Key Components

| Component | Type | Location | Description |
| --- | --- | --- | --- |
| `Settings` | Pydantic `BaseSettings` model | `config.py:L20` | Declares nine configuration keys at `L40-L48`. Seven are strictly required and two default to `None`. |
| `Settings.Config` | Nested Pydantic configuration class | `config.py:L50` | Sets `env_file = ".env"` at `L60` and `env_file_encoding = "utf-8"` at `L61`. The named `.env` file is not committed. |
| `get_settings` | Factory function | `config.py:L63` | Returns a fresh `Settings` instance at `L76`. Performs no caching. |
| `pwd_context` | Module-level `CryptContext` | `security.py:L24` | Configured with `schemes=['bcrypt']` and `deprecated='auto'`. Backs both password functions. |
| `oauth2_scheme` | Module-level `OAuth2PasswordBearer` | `security.py:L25` | Configured with `tokenUrl='token'`, which matches the `POST /token` route at `api/auth.py:L66`. |
| `create_access_token` | Function | `security.py:L27` | Signs a JWT. Reads `ACCESS_TOKEN_EXPIRE_MINUTES` at `L54` and calls `jwt.encode` with `SECRET_KEY` and `ALGORITHM` at `L56`. |
| `verify_password` | Function | `security.py:L59` | Delegates to `pwd_context.verify` at `L84` and returns `bool`, except where the resolved passlib and bcrypt releases make it raise. |
| `get_password_hash` | Function | `security.py:L86` | Delegates to `pwd_context.hash` at `L104` and returns `str`. |
| `get_current_user` | Async FastAPI dependency | `security.py:L110` | Decodes the bearer token at `L144` and resolves a user through `UserService` at `L151-L152`. Carries the package's only marker directly above, at `L106-L109`. |

## Architecture Fit

`core/` is the shared foundation layer of the backend. Both the Application Programming Interface (API) routers and
the persistence adapters depend on it, and it depends on nothing inside the application. `config.py` sits at the
bottom of every import chain: eight modules request a `settings` object from it, and `security.py:L22` requests the
`get_settings` factory. Package composition and the wider import graph are documented in [../README.md](../README.md),
and the system-wide view sits in [../../../docs/architecture-overview.md](../../../docs/architecture-overview.md).

The in-repository specification is a comparison point here, not ground truth. The relevant heading is `SECURITY
CONSIDERATIONS > AUTHENTICATION AND AUTHORIZATION`, which opens at `documentation/Technical Specifications.md:L622`.
That section names Google Cloud Identity Platform and Cloud Identity and Access Management (IAM) at
`documentation/Technical Specifications.md:L624`. The same section names Multi-Factor Authentication (MFA) at
`documentation/Technical Specifications.md:L628-L630`, Single Sign-On (SSO) at `documentation/Technical
Specifications.md:L632`, and Role-Based Access Control (RBAC) with the roles Reader, Editor and Admin at
`documentation/Technical Specifications.md:L646-L647`. Its `Implementation` subsection at `documentation/Technical
Specifications.md:L662` carries a sequence diagram at `documentation/Technical Specifications.md:L664-L680` whose
participants are User, Frontend, AuthService, GoogleCloudIdentity and Backend.

The divergence is one of model, not of mechanism. The specification does name JSON Web Tokens, at
`documentation/Technical Specifications.md:L655` under API access control, and the committed code does issue them.
What the code omits is everything the specification wraps around them. `security.py:L24` and `security.py:L86` hash
passwords locally with bcrypt, `security.py:L56` signs tokens locally with `python-jose`, and no module references an
Identity Platform, an MFA challenge or an SSO provider. The committed code therefore implements a local credential
model where the specification describes a federated one.

Role handling needs one qualification. Two role-adjacent artifacts exist outside this package: `schema/user.py:L72`
declares an `is_superuser: bool` that no code path reads, and `tasks/background_tasks.py:L112` names a
`document_permissions` Firestore collection. Neither is a role model. The authorization the backend actually performs
is a single owner-equality check in the service tier, under the three `# Check user permissions` comments at
`services/document_service.py:L107`, `:L147` and `:L183`.

## Dependencies

### Internal

| Dependency | Direction | Location | State |
| --- | --- | --- | --- |
| `app.core.config.get_settings` | `security.py` imports from `config.py` | Defined at `config.py:L63`, imported at `security.py:L22` | Resolves. Called at `security.py:L49` and `security.py:L142`. |
| `app.core.config.settings` | Eight modules import from `config.py` | `api/auth.py:L20`, `db/firestore.py:L16`, `db/sql.py:L14`, `main.py:L20`, `services/collaboration_service.py:L18`, `services/document_service.py:L17`, `services/export_service.py:L16`, `tasks/background_tasks.py:L16` | Does not resolve. `config.py` never creates a module-level `settings` instance. |
| `Optional` | Used by `security.py` | `security.py:L27`, inside `Optional[timedelta]` | Undefined. `security.py` imports nothing from `typing`. |
| `User` | Used by `security.py` | `security.py:L110`, the return annotation | Undefined. Declared in `schema/user.py:L56` and never imported here. |
| `UserService` | Used by `security.py` | `security.py:L151` | Undefined. No `app.services.user_service` module exists. |

Seven of the eight modules above dereference the `settings` object; `services/document_service.py:L17` imports it and
never uses it. `config.py` itself has no unresolved import: `pydantic` at `L17` and `typing.Optional` at `L18` both
resolve, and `Optional` is genuinely used at `L45` and `L46`. Contract definitions are documented in
[../../../docs/data-model.md](../../../docs/data-model.md).

### External

Only the four distributions these two modules import are listed. Package-wide version floors across the whole backend
live in [../README.md](../README.md), and the external services the backend reaches sit in
[../../../docs/integration-guide.md](../../../docs/integration-guide.md).

| Distribution | Constraint | Evidence in this package |
| --- | --- | --- |
| `pydantic` | 1.x only | `config.py:L17` imports `BaseSettings` from the main package. Version 2 moved that class to the separate `pydantic-settings` distribution. |
| `python-jose` | Unestablished | `security.py:L18` imports `jwt` from `jose`, `security.py:L56` calls `jwt.encode`, `security.py:L144` calls `jwt.decode`, and `security.py:L148` catches `jwt.JWTError`. |
| `passlib` with a bcrypt backend | Unestablished | `security.py:L19` imports `CryptContext`, and `security.py:L24` configures it with `schemes=['bcrypt']`. |
| `fastapi` | Unestablished | `security.py:L20` imports `Depends`, `HTTPException` and `status`; `security.py:L21` imports `OAuth2PasswordBearer`. |

No manifest and no lock file is committed anywhere in `backend/`, so each row records what the code requires.
"Unestablished" means nothing pins the distribution, not that any release is safe.

## Configuration

Fifteen configuration keys reach the backend through the `Settings` model. Nine are declared at `config.py:L40-L48`.
Six more are read from a `settings` object by other modules and are declared nowhere, so each one raises
`AttributeError` even after the absent singleton is restored. The Status column below classifies all fifteen.

| Key | Status | Declared at | Read at |
| --- | --- | --- | --- |
| `PROJECT_NAME` | DECLARED | `config.py:L40` | No consumer. `main.py:L90` sets `app.title` from the string literal `"Microsoft Word Backend"`. |
| `API_V1_STR` | DECLARED | `config.py:L41` | No consumer anywhere in the repository. The name appears exactly once, at its own declaration. |
| `SECRET_KEY` | DECLARED | `config.py:L42` | `security.py:L56`, `:L144`; `api/auth.py:L54`, `:L98` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | DECLARED | `config.py:L43` | `security.py:L54`; `api/auth.py:L95` |
| `ALGORITHM` | DECLARED | `config.py:L44` | `security.py:L56`, `:L144`; `api/auth.py:L54`, `:L99` |
| `GOOGLE_CLOUD_PROJECT` | DECLARED | `config.py:L45` | `db/firestore.py:L20`, at import time |
| `GOOGLE_APPLICATION_CREDENTIALS` | DECLARED | `config.py:L46` | Never dereferenced through `settings`. See the note below. |
| `DATABASE_URL` | DECLARED | `config.py:L47` | `db/sql.py:L16`, at import time |
| `REDIS_URL` | DECLARED | `config.py:L48` | `tasks/background_tasks.py:L22`, as the Celery broker argument |
| `ALLOWED_ORIGINS` | READ-BUT-NEVER-DECLARED | Nowhere | `main.py:L77`, as the Cross-Origin Resource Sharing (CORS) allow-list |
| `PROJECT_ID` | READ-BUT-NEVER-DECLARED | Nowhere | `services/collaboration_service.py:L69`, `:L70`, `:L128`, `:L153` |
| `STORAGE_BUCKET_NAME` | READ-BUT-NEVER-DECLARED | Nowhere | `services/export_service.py:L60`, `:L92` |
| `SIGNED_URL_EXPIRATION` | READ-BUT-NEVER-DECLARED | Nowhere | `services/export_service.py:L68`, `:L100` |
| `EXPORT_BUCKET_NAME` | READ-BUT-NEVER-DECLARED | Nowhere | `tasks/background_tasks.py:L62` |
| `DOCUMENT_BUCKET_NAME` | READ-BUT-NEVER-DECLARED | Nowhere | `tasks/background_tasks.py:L107` |

Four details qualify the table.

**Seven of the nine declared keys are strictly required, not nine.** No field carries an explicit default. Under
Pydantic 1.x, however, an `Optional[X]` field without a default is not required and receives an implicit `None`. That
covers `GOOGLE_CLOUD_PROJECT` at `config.py:L45` and `GOOGLE_APPLICATION_CREDENTIALS` at `config.py:L46`, both
annotated `Optional[str]`. The remaining seven raise `ValidationError` when absent.

**`GOOGLE_APPLICATION_CREDENTIALS` is unread through `settings` yet still load-bearing.** The settings field is never
dereferenced. The like-named operating-system environment variable is one of several sources Application Default
Credentials (ADC) consults, and `db/firestore.py:L19` holds the repository's only explicit ADC call, where
`credentials, project = default()` runs at import time. `scripts/deploy.sh:L4` aborts the deploy when that variable is
unset.

Removing the settings field would change nothing. Unsetting the environment variable stops the deploy script outright,
and leaves each Google client to whatever other ADC source the host offers. Examples are a `gcloud` user credential in
the well-known configuration file or the metadata server on a Google Cloud instance. This repository commits none of
those, so the outcome depends on the host rather than on anything tracked here.

**No `.env` file is committed.** `config.py:L60` points `env_file` at `.env`, and no such file exists in the
repository, so every required key must arrive from the process environment.

**`SIGNED_URL_EXPIRATION` has no declared type, no default and no bound.** The key sets the lifetime of a bearer
credential. A signed URL needs no authentication: whoever holds the link downloads the object until the link expires.
The key is absent from `Settings` entirely, so `config.py:L40-L48` constrains nothing about it. `Settings` declares no
`int`, `timedelta` or `datetime` annotation for it.

`Settings` declares no `Field` with `le` or `ge`, and no validator, so nothing here caps the value the process environment
supplies. A unit mistake therefore passes silently, because the Google client reads a bare integer as seconds while a
`timedelta` or a `datetime` means something else. The only ceiling lives in the client library rather than here.
`Blob.generate_signed_url` raises `ValueError` for a version 4 expiry above seven days, so a value above that limit
fails outright rather than minting a long-lived link. Any value at or below it is accepted with no project policy
behind it.

No signed URL is generated today, so this is a latent gap rather than a live exposure. Four barriers sit in front of
it, in the order execution meets them. `services/export_service.py` imports the absent `settings` singleton, so the
module fails at import. `export_service.py:L60` then reads the undeclared `STORAGE_BUCKET_NAME`.
`export_service.py:L68` then reads the undeclared `SIGNED_URL_EXPIRATION`.

Version 4 signing then needs a credential that can sign, and two routes qualify. A service-account private key signs
locally. A principal holding `iam.serviceAccounts.signBlob` signs through the Identity and Access Management (IAM) API
instead, which the Google Cloud Storage client uses when the call supplies `service_account_email` and `access_token`.
`export_service.py:L66-L70` supplies neither, and passes no `credentials`.

Signing therefore uses whatever the Cloud Storage client resolved for itself at `export_service.py:L36`, which builds
`Client()` with no arguments and runs its own ADC lookup. That lookup is independent of the Firestore lookup at
`db/firestore.py:L19`, and neither client shares a credential with the other. A key-file credential carries a private
key and signs. A metadata-server credential carries only a token, so local signing raises and the IAM route is
unavailable because the call names no service account.

Which credential each client resolves is a property of the host, and this repository supplies none, so the signing
outcome is unestablished here. The [services README](../services/README.md) and the [integration
guide](../../../docs/integration-guide.md) carry the same gap from the call-site and integration views.

## Data Flows

Two flows pass through this package. Configuration flows outward: a caller invokes `get_settings()` at `config.py:L63`,
and a fresh `Settings` instance returns at `config.py:L76`. Pydantic reads the process environment and the absent
`.env` file named at `config.py:L60`.

Token validation is the longer flow, and it stops before it finishes. FastAPI extracts the bearer token through
`Depends(oauth2_scheme)` at `security.py:L110`, against the scheme declared at `security.py:L25`. `get_settings()` runs
at `security.py:L142`. `jwt.decode` verifies the signature at `security.py:L144` using `SECRET_KEY` and `ALGORITHM`. The
`sub` claim is read at `security.py:L145`.

A missing subject raises 401 at `security.py:L147`, and a `jwt.JWTError` raises 401 at `security.py:L149`.
`UserService()` is then instantiated at `security.py:L151` and `get_user_by_id` is awaited at `security.py:L152`. A
`None` result raises 401 at `security.py:L154`, and the user returns at `security.py:L155`.

The flow reaches `security.py:L151` and stops. `UserService` is undefined, so the lookup raises `NameError` instead of
returning a user.

```mermaid
sequenceDiagram
    accTitle: The dependency chain from the bearer scheme to the absent UserService
    accDescr: A request carries a bearer token into get_current_user, which reads settings, decodes the token and then constructs UserService. UserService is undefined, so the chain raises NameError before it can return a user or reach its 401.
    participant C as Client
    participant GCU as get_current_user<br/>security.py:L110
    participant US as UserService<br/>ABSENT

    C->>GCU: bearer token, L25
    GCU->>GCU: get_settings(), L142
    GCU->>GCU: jwt.decode, L144
    Note over GCU: FastAPI resolves the dependency, and oauth2_scheme<br/>extracts the header at security.py:L25<br/>get_settings() resolves at config.py:L63<br/>jose.jwt.decode reads SECRET_KEY and ALGORITHM at L144<br/>sub claim read at L145<br/>401 at L147 if sub is None, 401 at L149 on jwt.JWTError
    GCU--xUS: UserService(), L151
    Note over GCU,US: BROKEN EDGE, drawn dashed with a cross:<br/>UserService is undefined, so L151 raises NameError,<br/>await get_user_by_id at L152 never runs,<br/>and the 401 at L154 is never reached
```

## Design Patterns

`core/` applies five patterns. Configuration uses a settings object: one Pydantic `BaseSettings` model at
`config.py:L20` gathers every key, so no module reads the environment directly. Access to that model runs through a
factory, `get_settings()` at `config.py:L63`, rather than an exported instance.

Two primitives are module-level singletons constructed at import: `pwd_context` at `security.py:L24` and
`oauth2_scheme` at `security.py:L25`. Authentication arrives by dependency injection, through `Depends(oauth2_scheme)`
in the `get_current_user` signature at `security.py:L110`. Token validation is stateless: `jwt.decode` at
`security.py:L144` verifies a signature and reads a claim, with no session store and no revocation list.

One absence shapes runtime behavior. `get_settings()` performs no caching. The module declares no
`functools.lru_cache` decorator and holds no module-level memo, so every call constructs a new `Settings` instance and
re-reads the environment. `security.py` calls it twice, at `security.py:L49` and `security.py:L142`, which means one
construction per token issued and one per request validated.

## Known Limitations

The largest limitation comes first. Nothing imports `app.core.security`, so every defect below sits in code that no
request path reaches. Repository-wide defect evidence sits in
[../../../docs/troubleshooting.md](../../../docs/troubleshooting.md), and judgement calls made while writing this
documentation are recorded in [../../../docs/decision-log.md](../../../docs/decision-log.md).

### Token security contract

Two `get_current_user` definitions exist and only one is reached. The table below states what the token contract does
**not** constrain, for both the issuing path here and the validating dependency that the twelve protected routes
actually import from `app.api.auth`. Every row is an absent control rather than a misconfiguration.

| Control | State | Evidence |
| --- | --- | --- |
| Secret strength or rotation | Absent | `config.py:L42` declares `SECRET_KEY: str` with no validator, minimum length or rotation hook. `security.py:L56` and `api/auth.py:L96-L100` sign with whatever value loads |
| Algorithm allow-list | Absent | `config.py:L44` declares `ALGORITHM: str` with no allowed-value check. Both `security.py:L56` and the decode at `api/auth.py:L54` pass the value straight through, so configuration alone selects the algorithm |
| Bounded token lifetime | Absent | `config.py:L43` declares `ACCESS_TOKEN_EXPIRE_MINUTES` with no ceiling. `security.py:L51-L54` computes `expire` from it, so an arbitrarily long lifetime is accepted |
| Issuer (`iss`) and audience (`aud`) claims | Absent | `api/auth.py:L96-L100` encodes exactly `sub` and `exp`. The decode at `:L54` reads `sub` only, and `security.py:L144` does the same, so a token cannot be scoped to one service or audience |
| Token identifier (`jti`) and revocation | Absent | No claim identifies a token and no store records issued or withdrawn tokens, so an issued token stays valid until `exp` |
| Inactive-account rejection | Absent in the dependency routes use | `api/auth.py:L61` loads the user and `:L64` returns it with no check, while `app/schema/user.py:L71` declares `is_active`. `security.py:L151-L154` behaves the same way, so a deactivated account keeps access |
| `WWW-Authenticate: Bearer` on an explicitly raised 401 | Absent | Six explicitly raised 401 responses set no `headers`: `api/auth.py:L56-L57`, `:L59`, `:L92-L93`, and `security.py:L147`, `:L149`, `:L154` |
| `WWW-Authenticate: Bearer` on a missing-header 401 | Present, from the framework | `security.py:L25` and `api/auth.py:L24` construct `OAuth2PasswordBearer` without `auto_error=False`, so FastAPI answers a missing or non-bearer `Authorization` header itself, with 401 `Not authenticated` and the challenge attached. Only the raises inside the dependency bodies omit it |
| Reviewed cryptography dependency floor | Absent | Nothing pins `python-jose`, because no backend manifest or lock file is committed, and the [dated register](../../../docs/troubleshooting.md#the-dated-dependency-and-advisory-register) carries the full advisory set. Releases through 3.3.0 carry [CVE-2024-33663](https://github.com/advisories/GHSA-6c5p-j8vq-pqhj), an algorithm confusion weakness with OpenSSH ECDSA and other key formats, fixed in 3.4.0. The advisory concerns verification, so the calls it would reach are `jwt.decode` at `security.py:L144` and `api/auth.py:L54`. Exposure here is conditional and unestablished, needing an installed release at or below 3.3.0, a verification key in an affected format, and an algorithm list admitting the confused algorithm. Both decode calls pass `algorithms=[settings.ALGORITHM]` while `config.py:L42` and `:L44` declare neither value, so no precondition can be checked here |

A safe floor cannot be asserted from this repository, because no committed file names a version. Establishing one
belongs to the reviewed manifest and lock recorded as future work in
[../../../docs/onboarding.md](../../../docs/onboarding.md).

- **The whole `security.py` module is unconsumed.** No tracked source file imports `core.security`, and the name appears
  only in documentation, including this file. `create_access_token` (`security.py:L27`), `verify_password` (`:L59`) and
  `get_password_hash` (`:L86`) appear only at their own definitions and have zero callers. The twelve protected routes import
  `get_current_user` from `app.api.auth` at `api/documents.py:L19`, `api/templates.py:L19` and `api/users.py:L15`.
- **No module-level `settings` instance exists.** `config.py` declares the `Settings` class at `L20` and the
  `get_settings` factory at `L63`, and never creates a `settings` object. Eight modules import one by name, listed
  under Dependencies above. That single absent line is the root cause of the backend's import failure; the full chain is
  documented in [../README.md](../README.md).
- **Three undefined names in `security.py` fail at three different moments.** Python evaluates annotations when the
  `def` statement runs, and no module here uses `from __future__ import annotations`.
  - `Optional` at `security.py:L27`, inside `Optional[timedelta]`, raises `NameError: name 'Optional' is not
    defined` **at module import time**.
  - `User` at `security.py:L110`, the return annotation, is also an import-time failure, but execution never reaches
    it because `L27` raises first.
  - `UserService` at `security.py:L151` sits inside a function body and raises at **first call**, not at import.
- **`except jwt.JWTError` at `security.py:L148` is correct and is not a defect.** The attribute resolves against
  `python-jose`, which exposes `JWTError` on the `jwt` module imported at `security.py:L18`. `api/auth.py:L17`
  imports the same exception by bare name and catches it at `api/auth.py:L58`. Both forms work.
- **The package's only marker is a four-line `HUMAN ASSISTANCE NEEDED` block at `security.py:L106-L109`**, directly
  above `get_current_user`. The block reads: "This function needs to be reviewed and potentially modified to ensure it
  correctly integrates with the User model and UserService. The exact implementation may vary depending on how these are
  set up in your project." `backend/app/core` contains zero `TODO` comments.
- **Token issuance and user resolution each exist twice, and the copy outside this package is the one in use.**
  `create_access_token` at `security.py:L27-L57` is duplicated by the inlined `jwt.encode` call at
  `api/auth.py:L96-L100`. `get_current_user` at `security.py:L110` is duplicated at `api/auth.py:L28`.
- **The two copies of `get_current_user` disagree on status code and on message.** For a user that cannot be found,
  `security.py:L154` raises 401 with detail "User not found" while `api/auth.py:L63` raises 404. On the
  invalid-credentials path, `security.py:L147` and `:L149` use "Could not validate credentials" while `api/auth.py:L57`
  and `:L59` use "Invalid authentication credentials".
- **The absent `UserService` is called two incompatible ways.** `security.py:L151-L152` instantiates the class and
  awaits an instance method, while `api/auth.py:L61`, `:L91`, `:L130` and `:L135` call methods on the class unbound.
  Any future implementation must satisfy one form or the other.
- **Two configuration access paths exist and one works.** `security.py:L22` imports the `get_settings` factory, which
  `config.py:L63` defines. Eight other modules import the `settings` singleton, which `config.py` does not define.
- **Three declared keys have no consumer.** `PROJECT_NAME` at `config.py:L40` is unread because `main.py:L90` uses a
  string literal. `API_V1_STR` at `config.py:L41` appears once, at its own declaration.
  `GOOGLE_APPLICATION_CREDENTIALS` at `config.py:L46` is never dereferenced through `settings`, though the like-named
  environment variable is read by ADC at `db/firestore.py:L19` and guarded at `scripts/deploy.sh:L4`.
- **401 is the only status code in this package**, raised at `security.py:L147`, `:L149` and `:L154`. No 403, 404 or 400
  appears in either module, so ownership checks and duplicate-registration handling live elsewhere.

Deployment consequences of the absent `.env` file and the unset credential variable are documented in
[../../../docs/deployment-guide.md](../../../docs/deployment-guide.md).

## Usage Examples

Both examples below fail at the import statement. Importing `app.core.security` raises
`NameError: name 'Optional' is not defined` at `security.py:L27`, before any function in the module becomes callable.
Each example shows the declared contract, taken from the signature at its cited line.

`create_access_token` at `security.py:L27` takes a payload dictionary and an optional lifetime, and returns the encoded
token as `str`.

```python
from datetime import timedelta

from app.core.security import create_access_token

# Default lifetime, taken from settings.ACCESS_TOKEN_EXPIRE_MINUTES at security.py:L54
token = create_access_token({"sub": "user-123"})

# Explicit lifetime, which skips the settings read at security.py:L54
short_lived = create_access_token({"sub": "user-123"}, timedelta(minutes=5))
```

The call above cannot execute: the import raises `NameError` at `security.py:L27`. Both forms also require `SECRET_KEY`
and `ALGORITHM` in the environment, because `jwt.encode` at `security.py:L56` reads them from a freshly constructed
`Settings`.

`get_current_user` at `security.py:L110` is a FastAPI dependency, not a function to call directly. Its only parameter is
the bearer token, supplied by `Depends(oauth2_scheme)`, so a route declares it as a dependency instead.

```python
from fastapi import APIRouter, Depends

from app.core.security import get_current_user

router = APIRouter()


@router.get("/profile")
async def read_profile(current_user=Depends(get_current_user)):
    return current_user
```

The route above cannot execute either: the import raises `NameError` at `security.py:L27`, and reaching
`security.py:L151` would raise a second `NameError` for the undefined `UserService`. No route in this repository depends
on this function, so the example shows intended use with no in-repository call site. The twelve routes that do guard
access use the copy at `api/auth.py:L28`.

`get_settings()` at `config.py:L63` is the one construct in this package that runs today. The import
`from app.core.config import get_settings` resolves, and the call returns a `Settings` instance whenever the seven
required keys are in the environment. `verify_password` at `security.py:L59` and `get_password_hash` at
`security.py:L86` are single-line wrappers over `pwd_context` and carry no example here. For environment setup and a
first run, see [../../../docs/onboarding.md](../../../docs/onboarding.md).
