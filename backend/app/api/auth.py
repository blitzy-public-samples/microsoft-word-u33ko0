"""Expose authentication routes and the bearer-token dependency.

settings, UserService, and the router name imported by app.main are unresolved.
No backend manifest pins python-jose, python-multipart, passlib, or the
FastAPI/Pydantic compatibility set. Reviewed floors are python-jose 3.4.0,
python-multipart 0.0.31, passlib 1.7.4, and Pydantic 1.10.13.
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
    """Resolve a bearer token to the user it identifies.

    Every protected route in this application depends on this function.
    UserService is unresolved, so the lookup method's binding contract cannot
    be verified.

    The dependency never checks `is_active`, so a valid token for an inactive
    user reaches all twelve protected handlers. SECRET_KEY and ALGORITHM are
    also unconstrained environment values.

    app.core.security defines a second helper with the same name. The helper
    here returns 404 for a missing user, while the other helper returns 401.

    Args:
        token: Bearer token, declared `str`. FastAPI supplies the value
            through `Depends(oauth2_scheme)`.

    Returns:
        The authenticated user, declared `User`.

    Raises:
        HTTPException: 401 when the token carries no `sub` claim or when
            `jwt.decode` raises `JWTError`. 404 when the lookup returns
            `None`.

        Neither custom 401 includes `WWW-Authenticate: Bearer`.
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
    """Issue a bearer token for a valid username and password.

    \N{FORM FEED}

    The route is public. The handler signs the token inline rather than
    calling the helper in app.core.security.

    SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES carry no validation.

    Args:
        form_data: An OAuth2 password form carrying `username` and `password`.

    Returns:
        A dictionary holding `access_token` and `token_type`. The handler
        declares no return annotation.

    Raises:
        HTTPException: 401 when authentication fails. The response includes no
            `WWW-Authenticate: Bearer` header.
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
    """Register a user and return the created record.

    \N{FORM FEED}

    The route is public. The User schema has no password-hash field, and
    persistence and response filtering cannot be verified because UserService
    is absent and the route binds no response model.

    UserCreate accepts any string password, including an empty value. The
    duplicate-email response also reveals whether an unauthenticated address
    already has an account.

    Args:
        user: A UserCreate carrying the email, username and plaintext
            password.

    Returns:
        The record UserService creates. The handler declares no return
        annotation.

    Raises:
        HTTPException: 400 when the email is already registered.

    Side effects:
        Hashes the submitted password with bcrypt before the create call.
        The call forwards only email and the hash, dropping username and
        full_name.
    """
    existing_user = await UserService.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = await UserService.create_user(user.email, hashed_password)
    return new_user