"""Build the authentication router and the shared bearer-token dependency.

Exposes two routes of the application programming interface (API) and the
`get_current_user` dependency that guards handlers in the other routers.
Routes are `POST /token` at L28 and `POST /register` at L42. Module exports
are `oauth2_scheme`, `pwd_context`, `router`, `get_current_user`,
`login_for_access_token` and `register_user`.

The module cannot import. Two of its imports do not resolve, in this order:

- L6 requests `settings` from `app.core.config`. `app.core.config` defines
  only the `Settings` class and a `get_settings()` factory, never a
  module-level `settings` object. L6 therefore raises first, with
  `ImportError: cannot import name 'settings' from 'app.core.config'`.
- L8 requests `UserService` from `app.services.user_service`. No such module
  exists, so L8 raises next once L6 resolves.

`app/main.py:L3` imports the name `auth_router` from this module. L12 defines
`router` instead. `app/core/security.py:L32` defines a second
`get_current_user`. `app/api/documents.py:L5`, `app/api/templates.py:L5` and
`app/api/users.py:L4` import the one defined here at L14.

Dependency limitation. The repository commits no backend dependency manifest, so
nothing pins the four third-party packages this module needs and nothing excludes
a vulnerable release. Required packages and their reviewed floors:

- `python-jose`, imported at L3 for `jwt.encode` at L35 and `jwt.decode` at L16.
  Floor 3.4.0 or later. Below it, GHSA-6c5p-j8vq-pqhj (CVE-2024-33663) allows
  algorithm confusion against exactly those two calls, and
  GHSA-cjwg-qfpm-7377 (CVE-2024-33664) allows denial of service.
- `python-multipart`, which FastAPI requires before it can populate the
  `OAuth2PasswordRequestForm` at L29 from a form body. Floor 0.0.31 or later.
  Below 0.0.31, GHSA-v9pg-7xvm-68hf (CVE-2026-53540) applies, and below 0.0.30
  GHSA-5rvq-cxj2-64vf (CVE-2026-53539) adds a high-severity processor
  exhaustion reachable from an unauthenticated form post to L28.
- `passlib` with a `bcrypt` backend, for the `CryptContext` at L11 and the hash
  at L48. Floor `passlib` 1.7.4.
- `fastapi` with a Pydantic 1.x-compatible release, because `app/schema/user.py`
  and `app/core/config.py` both depend on Pydantic 1.x behavior. Pydantic floor
  1.10.13, below which GHSA-mr82-8j83-vxmv (CVE-2024-3772) applies.

Choosing versions and writing a manifest are dependency changes and stay outside
this documentation pass.

Line references point at the pre-documentation layout of commit `06be74c`, so
they exclude docstrings added by this pass.
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
    """Resolve the bearer token into the authenticated user.

    L23 calls `UserService.get_user_by_id` on the class rather than on an
    instance.

    The dependency authenticates a token and stops there. L16 verifies the
    signature, L17 reads the `sub` claim, L23 fetches the user by that
    identifier, and L26 returns whatever came back. No line tests
    `user.is_active`, which `app/schema/user.py:L23` declares on the `User`
    contract and which no code path in the repository reads. A valid token issued
    to an account that was later deactivated therefore passes this dependency and
    reaches all twelve protected routes, so deactivating an account revokes
    nothing until the token expires. The function performs no per-object
    authorization either; each router body owns that check.

    Configuration limitation. L16 verifies with `settings.SECRET_KEY` and limits
    the accepted algorithms to `[settings.ALGORITHM]`. `app/core/config.py:L7`
    and `:L9` declare both as bare `str` with no length bound and no allowed-value
    list, so an empty or low-entropy key leaves the signature check ineffective
    against a forged token and the algorithm list carries whatever string the
    environment names.

    `app/core/security.py:L32` defines a second `get_current_user`. The
    missing-user branch at `app/core/security.py:L45` raises 401, where L25
    raises 404, and both send the detail `"User not found"`. The
    credential-failure detail differs too. L19 and L21 send
    `"Invalid authentication credentials"`, while `app/core/security.py:L38`
    and `app/core/security.py:L40` send `"Could not validate credentials"`.

    Args:
        token: The bearer credential, declared `str`. FastAPI injects it
            through `Depends(oauth2_scheme)`.

    Returns:
        The `User` given in the return annotation. L23 cannot execute, so no
        `User` is ever produced.

    Raises:
        HTTPException: Hypertext transfer protocol (HTTP) status 401 at L19,
            when the decoded JSON Web Token (JWT) payload carries no `sub`
            claim.
        HTTPException: HTTP 401 at L21, when decoding raises `JWTError`.
        HTTPException: HTTP 404 at L25, when the lookup returns `None`.

        Neither 401 passes a `headers` argument, so neither response carries a
        `WWW-Authenticate: Bearer` header. The bearer scheme expects that header
        on a 401, so a client cannot read the scheme or realm from the rejection
        and a standards-conforming client library cannot begin re-authentication
        from the response alone. Adding the header would change the responses, so
        this pass records the gap only.
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

    L30 calls `UserService.authenticate_user` on the class rather than on an
    instance, against a module that does not exist. The inline JWT encoding
    at L35-L39 duplicates `create_access_token` at
    `app/core/security.py:L11-L20`. L36 builds the payload
    `{"sub": str(user.id), "exp": datetime.utcnow() + access_token_expires}`,
    and L37 and L38 sign it with `settings.SECRET_KEY` and
    `settings.ALGORITHM`. L34 reads the lifetime from
    `settings.ACCESS_TOKEN_EXPIRE_MINUTES`.

    The decorator at L28 sets no `status_code`, so a success returns HTTP 200.

    Configuration limitation. L34, L37 and L38 read
    `settings.ACCESS_TOKEN_EXPIRE_MINUTES`, `settings.SECRET_KEY` and
    `settings.ALGORITHM`. `app/core/config.py:L7-L9` declares all three with bare
    `str` and `int` annotations and no constraint, so L37 signs with an empty or
    low-entropy key when the environment supplies one, L38 uses whatever
    algorithm string the environment names, and L34 accepts a zero, negative or
    unbounded lifetime. A zero or negative value produces a token whose `exp`
    claim at L36 is already in the past.

    Args:
        form_data: The submitted credentials, declared
            `OAuth2PasswordRequestForm`. FastAPI populates it from an OAuth2
            password-grant form body. L30 reads `form_data.username` and
            `form_data.password`.

    Returns:
        L29 declares no return annotation. L40 returns a dict holding
        `access_token` and `token_type`, where `token_type` is the literal
        string `"bearer"`.

    Raises:
        HTTPException: HTTP 401 at L32, when authentication yields a falsy
            user. The call passes no `headers` argument, so the response carries
            no `WWW-Authenticate: Bearer` header, which the bearer scheme expects
            on a 401 from a token endpoint. The single detail
            `"Incorrect username or password"` covers both an unknown username
            and a wrong password, so this response discloses no account
            existence.
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

    The decorator at L42 declares no authentication dependency, so the route
    is public. `POST /token` at L28 is the only other public route. L42 sets
    no `status_code`, so a success returns HTTP 200.

    No password policy runs on this public route. `app/schema/user.py:L11`
    declares `UserCreate.password` as a bare `str` with no `min_length`, no
    regular expression and no non-empty check, and the model declares no
    `@validator`. The empty string, a single character and any common password
    all validate, and L48 hashes whatever arrives. Any caller can therefore
    create an account with a trivial password.
    `frontend/src/utils/validation.ts:L8-L15` declares a length and character
    policy, and no module calls it, so nothing on the client protects this route.

    As a side effect, L48 computes a bcrypt hash of the submitted password
    through `pwd_context`. `app/schema/user.py:L11` declares
    `UserCreate.password`. The read model `User` at `app/schema/user.py:L19-L24`
    declares `id`, `created_at`, `updated_at`, `is_active` and `is_superuser`,
    with no field able to retain a password hash.

    The response fields cannot be established from this repository. L43 declares
    no return annotation and the decorator at L42 sets no `response_model`, so
    FastAPI applies no output contract and L50 returns the value from
    `UserService.create_user` unchanged. `app/services/user_service.py` does not
    exist, so nothing here records what that value contains. L49 hands the hash
    computed at L48 to that call, so a service that echoes its input would put
    the hash in the response body. Hash exposure on this route cannot be ruled
    out until the service and a response model exist.

    L49 passes only `user.email` and `hashed_password` to
    `UserService.create_user`, so the validated `username` and `full_name`
    never reach the service.

    Args:
        user: The submitted account details, declared `UserCreate`. The
            validated body carries `email`, `username`, `full_name` and
            `password`, per `app/schema/user.py:L5-L11`.

    Returns:
        L43 declares no return annotation. L50 returns whatever
        `UserService.create_user` produced at L49.

    Raises:
        HTTPException: HTTP 400 at L46, with the detail
            `"Email already registered"`, when the lookup at L44 finds an
            existing user. The route is public, so any caller can submit an
            address and read that response. The 400 and its detail appear only
            when an account exists for the address, and a free address returns a
            different status, so the pair of responses reports account existence
            to an unauthenticated caller. Repeating the request across a list of
            addresses enumerates which ones hold accounts. Changing the status or
            the detail would change the responses, so this pass records the
            behavior only.
    """
    existing_user = await UserService.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = await UserService.create_user(user.email, hashed_password)
    return new_user