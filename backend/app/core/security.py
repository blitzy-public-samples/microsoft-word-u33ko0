"""Hold the token and password primitives: signing, hashing and verification.

Three names are used and never imported, and they fail in a fixed order.
`Optional` in the `create_access_token` signature stops that definition
while the module loads. `User` in the `get_current_user` return annotation
stops the later definition once the first is repaired. Only `UserService`,
used inside that function's body, would fail when the body runs.

`jwt.JWTError` in the `except` clause below is sound: `python-jose` exposes
`JWTError` on its `jwt` module, so that line is not a defect.

`app/api/auth.py` carries its own `get_current_user` and its own inline
signing, so both live in two places with different status codes and
different details. No module imports anything from this file.
See ./README.md for the comparison.
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
    """Sign a JSON Web Token carrying the supplied claims and an expiry.

    The expiry is added to a copy of `data`, so the caller's dict is left
    unchanged. `Optional` in the signature is never imported, so the module
    raises `NameError` here while loading and never creates this function.

    Args:
        data: Claims to encode. Callers put the subject identifier in
            `"sub"`.
        expires_delta: Optional lifetime. When omitted, the lifetime comes
            from `settings.ACCESS_TOKEN_EXPIRE_MINUTES`.

    Returns:
        The encoded token as a string.

    Example:
        >>> token = create_access_token({"sub": "user-123"})
        >>> token = create_access_token(
        ...     {"sub": "user-123"}, expires_delta=timedelta(minutes=15)
        ... )
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
    """Check a plaintext password against a stored bcrypt hash.

    The call goes through passlib's `CryptContext` rather than `bcrypt`
    directly, so the resolved pair of distributions decides the contract, and
    no manifest pins either one. See `docs/troubleshooting.md` for the
    version-specific evidence.

    Args:
        plain_password: The password as submitted.
        hashed_password: The stored hash to compare against.

    Returns:
        True when the password matches the hash, False when it does not.

    Raises:
        ValueError: If the resolved password-hashing backend rejects the
            input. The message names a 72-byte limit even where the length of
            the input is not the cause.
        TypeError: If `hashed_password` is None, which the absent
            `app.services.user_service` would otherwise have to rule out.
        UnknownHashError: If `hashed_password` holds a value no configured
            scheme recognises, such as a plaintext column from a partially
            migrated store.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password with the bcrypt scheme configured on `pwd_context`.

    No schema bounds the input, and the call reaches bcrypt through passlib,
    so the resolved distributions decide the outcome. bcrypt reads at most 72
    bytes, and releases differ on whether a longer password is truncated or
    rejected. See `docs/troubleshooting.md` for the version-specific evidence.

    Args:
        password: The password to hash, unbounded by any schema rule.

    Returns:
        The bcrypt hash, including its salt and cost parameter.

    Raises:
        ValueError: If the resolved password-hashing backend rejects the
            password. The repository pins neither passlib nor bcrypt.
    """
    return pwd_context.hash(password)

# HUMAN ASSISTANCE NEEDED
# This function needs to be reviewed and potentially modified to ensure it correctly
# integrates with the User model and UserService. The exact implementation may vary
# depending on how these are set up in your project.
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Resolve a bearer token to the user its `sub` claim names.

    This function is the second `get_current_user` in the tree. The routers
    depend on the one in `app/api/auth.py`, and nothing imports this one. The
    two differ in their answers: a missing user is 401 here and 404 there, and
    the credential detail reads
    `"Could not validate credentials"` here against
    `"Invalid authentication credentials"` there.

    `User` and `UserService` are imported nowhere. `User` sits in the return
    annotation, so the module raises `NameError` here while loading and never
    creates this function. `UserService` sits in the body and would raise only
    when the body runs. See the HUMAN ASSISTANCE NEEDED marker above.

    Args:
        token: Bearer token, taken from the `Authorization` header by
            `oauth2_scheme`.

    Returns:
        The `User` the `sub` claim identifies.

    Raises:
        HTTPException: 401 when the claim is absent, when verification
            fails, or when no user matches. None of the three carries a
            `WWW-Authenticate` header.

    Example:
        >>> @router.get('/profile')
        ... async def profile(user: User = Depends(get_current_user)):
        ...     return user
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