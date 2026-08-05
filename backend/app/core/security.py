"""Hash passwords and issue JSON Web Tokens for the authentication flow.

Importing this module raises `NameError: name 'Optional' is not defined`, because
L11 annotates the `expires_delta` parameter with `Optional[timedelta]` and the
file imports nothing from `typing`. Python evaluates annotations while the `def`
statement runs, and no file in this repository uses
`from __future__ import annotations`.

Two further names are undefined, and each fails at a different moment. L32
annotates a return type of `User`, which raises next, but only once L11 stops
raising, because L11 runs first. L42 calls `UserService`, which raises at first
call rather than at import, because module-level execution never enters a
function body.

`except jwt.JWTError` at L39 resolves against `python-jose`, the library L2
imports. The line carries no defect.

L6 imports the `get_settings` factory, which `app/core/config.py:L19` defines.
Eight other modules import a `settings` singleton from that same module, and
`app/core/config.py` never defines the name.

No module in this repository imports `app.core.security`, so the four functions
below have no callers. The twelve protected routes import `get_current_user`
from `app/api/auth.py:L14` instead.
"""
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import get_settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Return a signed token carrying the supplied claims.

    L12 calls `get_settings()`, which builds a fresh `Settings` from the
    environment on every call. L13 copies `data`, so the caller's mapping stays
    unchanged. L17 falls back to `settings.ACCESS_TOKEN_EXPIRE_MINUTES` when the
    caller supplies no delta. L18 sets the `exp` claim, and L19 signs the payload
    with `settings.SECRET_KEY` and `settings.ALGORITHM`.

    Args:
        data: Claims to encode, declared `dict`.
        expires_delta: Token lifetime, declared `Optional[timedelta]` with a
            default of `None`. Python cannot evaluate that annotation, because
            `Optional` is undefined at L11.

    Returns:
        The encoded token, declared `str`.

    Example:
        >>> token = create_access_token({"sub": "user-123"})
        >>> token = create_access_token({"sub": "user-123"}, timedelta(hours=1))

        The example cannot run. Importing `app.core.security` raises `NameError`
        at L11.
    """
    settings = get_settings()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Report whether a plaintext password matches a stored hash.

    L23 delegates the comparison to `pwd_context.verify` against the bcrypt
    context configured at L8.

    Args:
        plain_password: Candidate password, declared `str`.
        hashed_password: Stored hash to compare against, declared `str`.

    Returns:
        `True` when the candidate matches the stored hash, declared `bool`.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Return a bcrypt hash of the supplied password.

    L26 delegates the work to `pwd_context.hash` against the bcrypt context
    configured at L8.

    Args:
        password: Plaintext password to hash, declared `str`.

    Returns:
        The bcrypt hash, declared `str`.
    """
    return pwd_context.hash(password)

# HUMAN ASSISTANCE NEEDED
# This function needs to be reviewed and potentially modified to ensure it correctly
# integrates with the User model and UserService. The exact implementation may vary
# depending on how these are set up in your project.
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Resolve a bearer token to the user it identifies.

    See the review marker in the comment block directly above this signature:
    `UserService` is referenced but no such module exists. L42 raises `NameError`
    at first call rather than at import, because module-level execution never
    enters a function body.

    L33 calls `get_settings()`, building a second fresh `Settings`. L35 decodes
    the token. L42 instantiates `UserService`, and L43 awaits an instance method
    on the result.

    `app/api/auth.py:L14` defines a second copy of this function, and the twelve
    protected routes depend on that copy rather than the one here. The two
    diverge on the missing-user path: L45 raises status 401, while
    `app/api/auth.py:L25` raises 404.

    Args:
        token: Bearer token, declared `str`. FastAPI supplies the value through
            `Depends(oauth2_scheme)` against the scheme at L9.

    Returns:
        The authenticated user, declared `User`. The module never defines or
        imports that name.

    Raises:
        HTTPException: Status 401 at L38 when the `sub` claim read at L36 is
            `None`. Status 401 at L40 when `jwt.decode` at L35 raises
            `jwt.JWTError`. Status 401 at L45 when the lookup at L43 returns
            `None`.

    Example:
        >>> async def read_me(user: User = Depends(get_current_user)):
        ...     return user

        The example cannot run. Importing `app.core.security` raises `NameError`
        at L11, and no route in this repository depends on this function.
    """
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    user_service = UserService()
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user