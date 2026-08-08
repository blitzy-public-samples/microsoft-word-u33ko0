"""Build the authentication router and the bearer-token dependency.

Two public routes issue and accept a JSON Web Token (JWT): `POST /token` and
`POST /register`. `get_current_user` resolves a token to a `User` and is the
dependency the document, user and template routers declare.

`app.services.user_service` does not exist, so every route body here fails
at import, and `settings` is imported from `app.core.config`, which never
creates it.

See ./README.md for the route table, the second `get_current_user` in
`app/core/security.py` and the packages this module needs.
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
    """Resolve a bearer token to the user its `sub` claim names.

    The dependency authenticates and stops there. No line reads
    `user.is_active`, so a token issued to an account deactivated later is
    still accepted, and no line performs a per-object check: each router
    body owns authorization. `app/core/security.py` defines a second
    `get_current_user` whose missing-user branch answers 401 where this one
    answers 404.

    Args:
        token: Bearer token, taken from the `Authorization` header by
            `oauth2_scheme`.

    Returns:
        The `User` the `sub` claim identifies. `UserService.get_user_by_id`
        is called on the class rather than an instance, against a module
        that does not exist.

    Raises:
        HTTPException: 401 when the `sub` claim is absent or the signature
            fails to verify, 404 when no user matches the identifier.
            Neither response carries the `WWW-Authenticate: Bearer` header
            the bearer scheme expects on a 401.
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
    """Issue a bearer token for submitted password-grant credentials.

    The route is public and answers 200 on success, because the decorator
    sets no `status_code`. The token is signed inline here rather than
    through `create_access_token` in `app/core/security.py`, so the two
    carry duplicate signing logic. `UserService.authenticate_user` is
    called on the class, against a module that does not exist.

    Args:
        form_data: Submitted credentials, declared
            `OAuth2PasswordRequestForm`. FastAPI fills it from an OAuth2
            password-grant form body carrying `username` and `password`.

    Returns:
        A dict carrying `access_token` and the literal `token_type`
        `"bearer"`. The handler declares no return annotation.

    Raises:
        HTTPException: 401 with the detail
            `"Incorrect username or password"`, which covers an unknown
            username and a wrong password alike, so the response discloses
            no account existence.
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
    """Register an account from submitted credentials.

    The route is public and answers 200 on success. The handler hashes the
    submitted password with `pwd_context`, then passes on only the email and
    that hash. The service never receives `username` or `full_name`.

    Args:
        user: Submitted account details, declared `UserCreate`, carrying
            `email`, `username`, `full_name` and `password`.

    Returns:
        Whatever `UserService.create_user` produced. The handler declares no
        return annotation and the decorator sets no `response_model`, so
        FastAPI applies no output contract. `app.services.user_service` is absent.

    Raises:
        HTTPException: 400 with the detail `"Email already registered"`
            when an account exists for the submitted address. The route is
            public, so the two different responses report to any caller
            whether an address holds an account.
        ValueError: From the hash call below, which reaches bcrypt through
            passlib's `CryptContext` rather than directly, so the resolved pair
            of distributions decides when it raises and no manifest pins
            either. With passlib 1.7.4 and bcrypt 5.0.0 every call raises,
            whatever the password length. Passlib probes its backend with a
            255-byte secret, and bcrypt 5.0.0 rejects any input over 72 bytes.
            With a bcrypt release passlib can drive, only a password over 72
            bytes raises, and only from 5.0.0 onward. Either way this public
            route answers an unhandled 500 to any caller, and registration
            cannot succeed at all on the first pairing.
    """
    existing_user = await UserService.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = await UserService.create_user(user.email, hashed_password)
    return new_user