"""Hash passwords and issue JSON Web Tokens.

Optional, User, and UserService are unresolved in this module.
No backend manifest pins python-jose or passlib. The reviewed python-jose
floor is 3.4.0 because earlier releases include CVE-2024-33663 and
CVE-2024-33664. Passlib also requires a bcrypt backend.
The `jwt.JWTError` exception name is valid for python-jose and is not a defect.
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

    The function copies `data` before adding the `exp` claim, so the caller's
    mapping stays unchanged. The configured token expiry applies whenever the
    caller supplies no lifetime. A zero timedelta is also falsy and takes that
    default branch. A negative timedelta creates an already-expired token.

    Settings validates neither signing-key strength nor the algorithm name.

    Args:
        data: Claims to encode, declared `dict`.
        expires_delta: Token lifetime, declared `Optional[timedelta]` with a
            default of `None`. The `Optional` annotation is unresolved.

    Returns:
        The encoded token, declared `str`.

    Example:
        >>> token = create_access_token({"sub": "user-123"})
        >>> token = create_access_token({"sub": "user-123"}, timedelta(hours=1))

        The example cannot run, because the unresolved `Optional` annotation
        raises while this module imports.
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

    Args:
        plain_password: Candidate password, declared `str`.
        hashed_password: Stored bcrypt hash, declared `str`.

    Returns:
        `True` when the candidate matches the stored hash, declared `bool`.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Return a bcrypt hash of the supplied password.

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

    See the assistance marker in the comment block directly above this
    signature: the `User` model and the `UserService` lookup it describes are
    both unresolved here.

    Args:
        token: Bearer token, declared `str`. FastAPI supplies the value
            through `Depends(oauth2_scheme)`.

    Returns:
        The authenticated user, declared `User`. The module neither defines
        nor imports that name.

    Raises:
        HTTPException: Status 401 when the token carries no `sub` claim, when
            `jwt.decode` raises `jwt.JWTError`, or when the lookup returns
            `None`.
        NameError: On the first call, because `UserService` is unresolved.

        The custom 401 responses set no `WWW-Authenticate: Bearer` header, so
        clients receive no bearer challenge.

    Example:
        >>> async def read_me(user: User = Depends(get_current_user)):
        ...     return user

        The example cannot run, because the unresolved `Optional` annotation
        raises while this module imports.
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