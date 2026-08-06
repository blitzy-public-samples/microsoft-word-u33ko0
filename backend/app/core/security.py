"""Provide the token, password-hashing and current-user security primitives.

Exports `create_access_token`, `verify_password`, `get_password_hash`,
`get_current_user`, plus the `pwd_context` and `oauth2_scheme` singletons.

Three names are used and never imported: `Optional` in the `create_access_token`
signature, and `User` and `UserService` in `get_current_user`. The first raises
`NameError` at module evaluation; the other two raise when the function runs.

`app/api/auth.py` defines a second `get_current_user` with the same purpose and
different status codes, and every router imports that one rather than this one.

Dependency limitation. The repository commits no backend dependency manifest,
so nothing pins `python-jose` or `passlib` and nothing excludes a vulnerable
release. Reviewed secure floor: `python-jose` 3.4.0 or later. Releases below it
carry GHSA-6c5p-j8vq-pqhj (CVE-2024-33663), a critical algorithm-confusion flaw,
and GHSA-cjwg-qfpm-7377 (CVE-2024-33664), which allows resource exhaustion
through a compressed JSON Web Encryption payload. Both advisories turn on the
token an attacker submits, so the `jwt.decode` at L35 is the remotely reachable
call. The `jwt.encode` at L19 signs the payload that L13 copies from its `data`
argument and L18 stamps with an `exp` claim, never a token that arrived with a
request, so a remote caller cannot steer it. `passlib` 1.7.4 with a
`bcrypt` backend is what the `CryptContext` at L8 requires, and neither package
name appears in any tracked file. An environment build therefore resolves both
imports to whatever release the package index offers on the day it runs.

L6 imports the `get_settings` factory, which `app/core/config.py:L126` defines.
Eight other modules import a `settings` singleton from that same module, and
`app/core/config.py` never defines the name.

No module in this repository imports `app.core.security`, so the four functions
below have no callers. The twelve protected routes import `get_current_user`
from `app/api/auth.py:L92` instead.

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
    """Sign a JSON Web Token carrying the given claims and an expiry.

    Args:
        data: Claims to embed. Copied before use, so the caller's dictionary is left
            unchanged.
        expires_delta: Lifetime for this token. When omitted, the lifetime comes from
            `settings.ACCESS_TOKEN_EXPIRE_MINUTES`.

    Returns:
        The encoded token as a string.

    Raises:
        NameError: At import time, because `Optional` is used in the signature and never
            imported.

    Example:
        token = create_access_token({"sub": user_id}, timedelta(minutes=30))

    Note:
        Adds only the `exp` claim, so no issuer, audience or issued-at claim is set, and
        no token identifier is recorded that would allow revocation. Expiry is computed
        from `datetime.utcnow()`, a naive timestamp.
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
    """Check a plain-text password against a stored bcrypt hash.

    Args:
        plain_password: Password as submitted by the caller.
        hashed_password: Stored hash to compare against.

    Returns:
        True when the password matches the hash, false otherwise.

    Note:
        No caller in the committed tree uses this helper; `app/api/auth.py` delegates
        authentication to the absent user service instead.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password with bcrypt.

    Args:
        password: Plain-text password to hash.

    Returns:
        The bcrypt hash, carrying its own salt and cost factor.

    Note:
        bcrypt truncates input at 72 bytes, so a longer password contributes nothing
        beyond that length.
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
    `app/core/config.py:L113` and `:L9`, which declare each as a bare `str`, and
    the consequence depends on which algorithm the environment names. Under a
    symmetric algorithm such as HS256, this field carries the shared secret that
    both signs at L19 and verifies at L35, so an empty or guessable value lets an
    attacker forge a token that L35 accepts. Under an asymmetric algorithm such
    as RS256, L35 expects a public key in the same field, so a short or
    low-entropy value forges nothing and verification fails instead of
    succeeding. The single-entry algorithm list inherits whatever string the
    environment names rather than an approved algorithm either way.

    `app/api/auth.py:L92` defines a second copy of this function, and the twelve
    protected routes depend on that copy rather than the one here. The two
    diverge on the missing-user path: L45 raises status 401, while
    `app/api/auth.py:L167` raises 404.

    Args:
        token: Bearer token, extracted from the `Authorization` header by
            `oauth2_scheme`.

    Returns:
        The `User` the token's `sub` claim identifies.

    Raises:
        HTTPException: Status 401 at L38 when the `sub` claim read at L36 is
            `None`. Status 401 at L40 when `jwt.decode` at L35 raises
            `jwt.JWTError`. Status 401 at L45 when the lookup at L43 returns
            `None`. None of the three passes a `headers` argument, so none of the
            three responses carries a `WWW-Authenticate: Bearer` header. The
            bearer scheme expects that header on a 401, so a client cannot read
            the scheme or realm from the rejection and a standards-conforming
            client library cannot start its re-authentication flow from the
            response alone.

    Example:
        @router.get("/me")
        async def read_me(user: User = Depends(get_current_user)):
            return user

    Note:
        Answers 401 for a missing user, where the duplicate in `app/api/auth.py` answers
        404, and sends "Could not validate credentials" where that one sends "Invalid
        authentication credentials". Reads no `is_active` flag, so a deactivated user
        passes. The assistance marker directly above records the unverified integration
        with the user model and service.
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