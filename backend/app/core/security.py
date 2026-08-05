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

Dependency limitation. The repository commits no backend dependency manifest,
so nothing pins `python-jose` or `passlib` and nothing excludes a vulnerable
release. Reviewed secure floor: `python-jose` 3.4.0 or later. Releases below it
carry GHSA-6c5p-j8vq-pqhj (CVE-2024-33663), a critical algorithm-confusion flaw
that bears directly on the `jwt.encode` at L19 and the `jwt.decode` at L35, and
GHSA-cjwg-qfpm-7377 (CVE-2024-33664), a denial-of-service flaw. `passlib` 1.7.4
with a `bcrypt` backend is what the `CryptContext` at L8 requires, and neither
package name appears in any tracked file. Pinning a version is a dependency
change and stays outside this documentation pass.

L6 imports the `get_settings` factory, which `app/core/config.py:L19` defines.
Eight other modules import a `settings` singleton from that same module, and
`app/core/config.py` never defines the name.

No module in this repository imports `app.core.security`, so the four functions
below have no callers. The twelve protected routes import `get_current_user`
from `app/api/auth.py:L14` instead.

Line locators: every `Lnn` reference below numbers the tree at commit
06be74c7c88aa6bca652d465eaa00ad480a9e5c5, the frozen revision that precedes this
documentation pass. A bare `Lnn` points into this file, and a `path:Lnn` points into
the named file. Current HEAD numbers each documented file higher.
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
    unchanged. L18 sets the `exp` claim, and L19 signs the payload with
    `settings.SECRET_KEY` and `settings.ALGORITHM`.

    The L14 branch tests `expires_delta` for truthiness rather than for `None`,
    so two inputs behave in ways the parameter default does not suggest:

    - `timedelta(0)` is falsy. A caller who asks for a zero lifetime takes the
      L17 fallback instead and receives the configured lifetime.
    - A negative `timedelta` is truthy. L15 adds it to `datetime.utcnow()`, so
      L18 writes an `exp` claim already in the past and L19 signs a token that
      every verifier rejects at once.

    Configuration limitation. All three settings this function reads arrive
    unvalidated. `app/core/config.py:L7-L9` declares `SECRET_KEY` and `ALGORITHM`
    as bare `str` and `ACCESS_TOKEN_EXPIRE_MINUTES` as bare `int`, with no
    length bound, no allowed-value list and no positivity check. L19 therefore
    signs with an empty or low-entropy key when the environment supplies one, and
    with whatever algorithm string the environment names. L17 accepts a zero,
    negative or unbounded configured lifetime by the same route.

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

    Configuration limitation. L35 verifies the signature with
    `settings.SECRET_KEY` and restricts the accepted algorithms to
    `[settings.ALGORITHM]`. Both values arrive unvalidated from
    `app/core/config.py:L7` and `:L9`, which declare each as a bare `str`. An
    empty or low-entropy key leaves the signature check ineffective against a
    forged token, and the single-entry algorithm list inherits whatever string
    the environment names rather than an approved algorithm.

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
            `None`. None of the three passes a `headers` argument, so none of the
            three responses carries a `WWW-Authenticate: Bearer` header. The
            bearer scheme expects that header on a 401, so a client cannot read
            the scheme or realm from the rejection and a standards-conforming
            client library cannot start its re-authentication flow from the
            response alone. Adding the header would change the responses, so this
            pass records the gap only.

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