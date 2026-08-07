"""Build the authentication router and the token-to-user dependency.

Two public routes: `POST /token` issues a bearer token, and `POST /register` creates a
user. Both are unauthenticated. The module exports `router`, `get_current_user`,
`oauth2_scheme` and `pwd_context`.

The module cannot import. `settings` is requested from `app.core.config`, which defines
only the `Settings` class and a `get_settings()` factory, so that import raises first.
`app.services.user_service` does not exist, so `UserService` would raise next.

- L81 requests `settings` from `app.core.config`. `app.core.config` defines
  only the `Settings` class and a `get_settings()` factory, never a
  module-level `settings` object. L81 therefore raises first, with
  `ImportError: cannot import name 'settings' from 'app.core.config'`.
- L83 requests `UserService` from `app.services.user_service`. No such module
  exists, so L83 raises next once L81 resolves.

`app/main.py:L16` imports `auth_router` from this module, and `app/api/auth.py:L87`
defines `router` instead. `app/core/security.py:L117` defines a second
`get_current_user`. `app/api/documents.py:L48`, `app/api/templates.py:L72` and
`app/api/users.py:L25` import `app/api/auth.py:L89` instead.

Neither public route applies a request limit. No line in this module and no
committed middleware applies a rate limit, a delay, a lockout, a challenge or a
per-caller quota. The credential check behind L167 and the address lookup behind
L242 therefore answer requests as fast as the server can, so password guessing
against `POST /token` and bulk account creation against `POST /register` are
bounded only by server capacity.

No request field carries an upper bound. `app/schema/user.py:L71-L94` declares the
four `UserCreate` fields as bare `str` with no `max_length`, the
`OAuth2PasswordRequestForm` at L168 bounds neither `username` nor `password`, and
no committed middleware caps the request body size. A caller can therefore submit
an arbitrarily large value in any field on either public route.

Dependency limitation. The repository commits no backend dependency manifest, so
nothing pins the four third-party packages this module needs and nothing excludes
a vulnerable release. Required packages and their reviewed floors:

- `python-jose`, imported at L78 for `jwt.decode` at L155 and `jwt.encode` at L235.
  Floor 3.4.0 or later. Below it, GHSA-6c5p-j8vq-pqhj (CVE-2024-33663) allows
  algorithm confusion and GHSA-cjwg-qfpm-7377 (CVE-2024-33664) allows resource
  exhaustion through a compressed JSON Web Encryption payload. Both advisories
  are driven by the token an attacker submits, so the `jwt.decode` at L155 is the
  remotely reachable call. The `jwt.encode` at L235 signs claims this module
  builds at L236 and reads no caller-supplied token.
- `python-multipart`, which FastAPI requires before it can populate the
  `OAuth2PasswordRequestForm` at L168 from a form body. Conservative floor 0.0.31
  or later, which clears both published advisories. The two differ in reach.
  GHSA-5rvq-cxj2-64vf (CVE-2026-53539), fixed in 0.0.30, is the one this route
  exposes. The flaw is quadratic-time field-separator scanning in
  `QuerystringParser`, the parser Starlette drives for the
  `application/x-www-form-urlencoded` body that an unauthenticated post to L167
  sends, and it is scored 7.5 High for availability. 0.0.30 is therefore the
  floor for this code path. GHSA-v9pg-7xvm-68hf (CVE-2026-53540),
  fixed in 0.0.31, is package-wide hardening rather than exposure here. The
  unvalidated negative `Content-Length` read sits in the library's own
  `parse_form()` entry point, and its text records Starlette and FastAPI as
  unaffected. No line in this repository calls `parse_form()`.
- `passlib` with a `bcrypt` backend, for the `CryptContext` at L86 and the hash
  at L323. Floor `passlib` 1.7.4.
- `fastapi` with a Pydantic 1.x-compatible release, because `app/schema/user.py`
  and `app/core/config.py` both depend on Pydantic 1.x behavior. Pydantic floor
  1.10.13, below which GHSA-mr82-8j83-vxmv (CVE-2024-3772) applies.

No manifest names any of these packages, so an environment build resolves each
one to whatever release the package index offers on the day it runs.

Both route docstrings below close with a paragraph labelled "Internal notes",
carrying dependency names, locators and failure analysis. The `get_current_user`
dependency carries no such paragraph, because its own notes sit inline.

Every `Lnn` reference below points at the current layout of the file it names. A
bare `Lnn` points into this file, and a `path:Lnn` points into the named file.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core.config import settings
from app.schema.user import User, UserCreate
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
router = APIRouter()

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Resolve the bearer token to the user it names.

    L162 calls `UserService.get_user_by_id` on the class rather than on an
    instance.

    The dependency authenticates a token and stops there. L155 verifies the
    signature, L156 reads the `sub` claim, L162 fetches the user by that
    identifier, and L165 returns whatever came back. No line tests
    `user.is_active`, which `app/schema/user.py:L172` declares on the `User`
    contract and which no code path in the repository reads. Wherever this
    dependency is invoked it therefore accepts a valid token issued to an account
    that was later deactivated, and reports no difference between an active and a
    deactivated account, so deactivating an account revokes nothing until the
    token expires. The function performs no per-object authorization either; each
    router body owns that check.

    Which routes that acceptance actually reaches is a separate question. Twelve
    handlers declare this dependency: five in `app/api/documents.py`, two in
    `app/api/users.py` and five in `app/api/templates.py`. None of the twelve is
    served as committed, because `import app.main` fails at `app/main.py:L16` and
    then at L81 here. On a repaired import, `app/main.py:L125-L128` mounts every
    router with no prefix, so `GET /{document_id}` at
    `app/api/documents.py:L145` and `PUT /{document_id}` at `:L188` shadow
    `GET /me` and `PUT /me` at `app/api/users.py:L29` and `:L50`, and all five
    template routes repeat paths the documents router claimed first at
    `app/main.py:L126`. Starlette matches in registration order, so seven of the
    twelve protected handlers stay unreachable and the five document routes are
    the ones an accepted token would reach.

    Configuration limitation. L155 verifies with `settings.SECRET_KEY` and limits
    the accepted algorithms to `[settings.ALGORITHM]`. `app/core/config.py:L113`
    and `:L115` declare both as bare `str` with no length bound and no allowed-value
    list, and the consequence depends on which algorithm the environment names.
    Under a symmetric algorithm such as HS256, this field carries the shared
    secret that both signs and verifies, so an empty or guessable value lets an
    attacker mint a token that L155 accepts. Under an asymmetric algorithm such as
    RS256, L155 expects a public key in the same field, so a short or low-entropy
    value forges nothing and verification fails instead of succeeding. The
    algorithm list carries whatever string the environment names either way.

    `app/core/security.py:L117` defines a second `get_current_user`. The
    missing-user branch at `app/core/security.py:L189` raises 401, where L98
    raises 404, and both send the detail `"User not found"`. The
    credential-failure detail differs too. L158 and L160 send
    `"Invalid authentication credentials"`, while `app/core/security.py:L182`
    and `app/core/security.py:L184` send `"Could not validate credentials"`.

    Args:
        token: Bearer token, extracted from the `Authorization` header by
            `oauth2_scheme`.

    Returns:
        The `User` the token's `sub` claim identifies.

    Raises:
        HTTPException: 401 when the `sub` claim is absent or the signature fails to
            verify, and 404 when no user matches the identifier.

        Neither 401 passes a `headers` argument, so neither response carries a
        `WWW-Authenticate: Bearer` header. The bearer scheme expects that header
        on a 401, so a client cannot read the scheme or realm from the rejection
        and a standards-conforming client library cannot begin re-authentication
        from the response alone.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await UserService.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Issue a bearer token for submitted form credentials.

    The route is public and takes an OAuth2 password-grant form body carrying a
    username and a password. A success returns hypertext transfer protocol (HTTP)
    status 200 carrying a bearer token, because the decorator sets no
    `status_code`.

    Args:
        form_data: The submitted credentials, declared
            `OAuth2PasswordRequestForm`. FastAPI populates it from an OAuth2
            password-grant form body, which carries `username` and `password`.

    Returns:
        A dict holding `access_token` and `token_type`, where `token_type` is
        the literal string `"bearer"`. The handler declares no return
        annotation.

    Raises:
        HTTPException: HTTP 401 with the detail
            `"Incorrect username or password"`. The one detail covers both an
            unknown username and a wrong password, so the response discloses no
            account existence.

    Internal notes.

    L230 calls `UserService.authenticate_user` on the class rather than on an
    instance, against a module that does not exist. The inline JSON Web Token
    (JWT) encoding at L235-L239 duplicates `create_access_token` at
    `app/core/security.py:L48-L80`. L180 builds the payload
    `{"sub": str(user.id), "exp": datetime.utcnow() + access_token_expires}`,
    and L237 and L238 sign it with `settings.SECRET_KEY` and
    `settings.ALGORITHM`. L234 reads the lifetime from
    `settings.ACCESS_TOKEN_EXPIRE_MINUTES`.

    The decorator sits at L167, the 401 at L232 and the return at L240. L168
    declares no return annotation.

    Configuration limitation. L234, L237 and L238 read
    `settings.ACCESS_TOKEN_EXPIRE_MINUTES`, `settings.SECRET_KEY` and
    `settings.ALGORITHM`. `app/core/config.py:L113-L115` declares all three with bare
    `str` and `int` annotations and no constraint. L237 therefore signs with an
    empty or low-entropy key when the environment supplies one, L238 uses whatever
    algorithm string the environment names, and L234 accepts a zero, negative or
    unbounded lifetime. A zero or negative value produces a token whose `exp`
    claim at L236 is already in the past. Under a symmetric algorithm such as
    HS256, the key L237 signs with is the same secret that verification needs, so
    a guessable value lets an attacker mint tokens that the dependency at L89
    accepts. Under an asymmetric algorithm such as RS256, L237 needs a private key
    in that field and signing fails when it holds anything else.

    L230 reads `form_data.username` and `form_data.password`. The 401 at L232
    fires when authentication yields a falsy user, and the call passes no
    `headers` argument, so the response carries no `WWW-Authenticate: Bearer`
    header, which the bearer scheme expects on a 401 from a token endpoint.

    The route applies no request limit. No line here and no committed middleware
    applies a rate limit, a delay, a lockout, a challenge or a per-caller quota,
    so password guessing against L167 is bounded only by how fast the server
    answers. `OAuth2PasswordRequestForm` bounds neither submitted field, and no
    line caps the request body size.
    """
    user = await UserService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": str(user.id), "exp": datetime.utcnow() + access_token_expires},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/register')
async def register_user(user: UserCreate):
    """Register a new account from submitted credentials.

    The route is public and takes a body carrying an email address, a username,
    an optional full name and a password. A success returns HTTP status 200,
    because the decorator sets no `status_code`. The handler computes a bcrypt
    hash of the submitted password before it creates the account.

    Args:
        user: The submitted account details, declared `UserCreate`. The
            validated body carries `email`, `username`, `full_name` and
            `password`.

    Returns:
        The value the user service produced for the new account. The handler
        declares no return annotation and the decorator sets no `response_model`,
        so FastAPI applies no output contract.

    Raises:
        HTTPException: HTTP 400 with the detail `"Email already registered"`,
            when an account already exists for the submitted address.

    Internal notes.

    The decorator at L242 declares no authentication dependency, so the route
    is public. `POST /token` at L167 is the only other public route. L242 sets
    no `status_code`, so a success returns HTTP 200, and the 400 sits at L321
    behind the lookup at L319.

    No password policy runs on this public route. `app/schema/user.py:L94`
    declares `UserCreate.password` as a bare `str` with no `min_length`, no
    regular expression and no non-empty check, and the model declares no
    `@validator`. The empty string, a single character and any common password
    all validate, and L323 hashes whatever arrives. Any caller can therefore
    create an account with a trivial password.
    `frontend/src/utils/validation.ts:L44-L51` declares a length and character
    policy, and no module calls it, so nothing on the client protects this route.

    No submitted field carries an upper bound either. `app/schema/user.py:L71-L94`
    declares `email`, `username`, `full_name` and `password` as bare `str` fields
    with no `max_length`, and neither this route nor any committed middleware caps
    the request body size. A caller can therefore submit an arbitrarily large
    value in any of the four fields, including the `password` that L323 hashes.

    The route applies no request limit. No line here and no committed middleware
    applies a rate limit, a delay, a lockout, a challenge or a per-caller quota,
    so bulk account creation against L242 is bounded only by how fast the server
    answers.

    As a side effect, L323 computes a bcrypt hash of the submitted password
    through `pwd_context`. `app/schema/user.py:L94` declares
    `UserCreate.password`. The read model `User` at `app/schema/user.py:L114-L173`
    declares `id`, `created_at`, `updated_at`, `is_active` and `is_superuser`,
    with no field able to retain a password hash.

    The response fields cannot be established from this repository. L243 declares
    no return annotation and the decorator at L242 sets no `response_model`, so
    FastAPI applies no output contract and L325 returns the value from
    `UserService.create_user` unchanged. `app/services/user_service.py` does not
    exist, so nothing here records what that value contains. L324 hands the hash
    computed at L323 to that call, so a service that echoes its input would put
    the hash in the response body. Hash exposure on this route cannot be ruled
    out until the service and a response model exist.

    L324 passes only `user.email` and `hashed_password` to
    `UserService.create_user`, so the validated `username` and `full_name`
    never reach the service. `app/schema/user.py:L71-L94` declares the four
    request fields, and L325 returns whatever L324 produced.

    The 400 sits at L321 and the lookup that triggers it at L319. The route is
    public, so any caller can submit an address and read that response. The 400
    and its detail appear only when an account exists for the address, and a free
    address returns a different status, so the pair of responses reports account
    existence to an unauthenticated caller. Repeating the request across a list of
    addresses enumerates which ones hold accounts.
    """
    existing_user = await UserService.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = await UserService.create_user(user.email, hashed_password)
    return new_user