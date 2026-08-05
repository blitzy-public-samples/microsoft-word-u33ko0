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
            user.
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

    As a side effect, L48 computes a bcrypt hash of the submitted password
    through `pwd_context`. No schema field can hold that hash.
    `app/schema/user.py:L11` declares `UserCreate.password`. The read model
    `User` at `app/schema/user.py:L19-L24` declares `id`, `created_at`,
    `updated_at`, `is_active` and `is_superuser`, with no field able to retain
    a password hash.

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
        HTTPException: HTTP 400 at L46, when a user already exists for the
            submitted email.
    """
    existing_user = await UserService.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = await UserService.create_user(user.email, hashed_password)
    return new_user