"""Build the router for the two current-user profile routes.

Two handlers serve `GET /me` and `PUT /me`, both behind `get_current_user`. The module
exports `router`.

`app/main.py` imports the name `users_router` from this module, and this module defines
`router`. The module cannot import. L3 requests `UserService` from
`app.services.user_service`, a module that does not exist, so L3 raises before L4 is
reached. L4 requests `get_current_user` from `app.api.auth`, the definition at
`auth.py:L14`, and that module would fail in turn at `auth.py:L6` on the absent
`settings` name.

Both handlers are plain synchronous `def`, at L9 and L13. The other twelve
committed handlers are `async def`, so FastAPI runs these two in its thread pool.

Each handler below splits its docstring at a form-feed marker, spelled as the
Unicode named escape for that character. FastAPI publishes the text above that
marker as the route description in the generated OpenAPI document and drops
everything below it. Each lower section is labelled "Internal notes" and carries
dependency names, locators and failure analysis.

Line references point at the pre-documentation layout of commit `06be74c`, so
they exclude docstrings added by this pass.
"""
from fastapi import APIRouter, Depends, HTTPException
from app.schema.user import User, UserUpdate
from app.services.user_service import UserService
from app.api.auth import get_current_user

router = APIRouter()

@router.get('/me')
def get_current_user_info(current_user: User = Depends(get_current_user)) -> User:
    """Return the authenticated caller's own profile.

    Args:
        current_user: The caller, injected through `Depends(get_current_user)`.

    Returns:
        The `User` given in the return annotation.
    \N{FORM FEED}
    Internal notes.

    The decorator sits at L8, and L10 returns the injected `current_user` object.
    The handler is a synchronous `def`, and FastAPI resolves its `async def`
    dependency at `auth.py:L14` before calling it.

    The route is shadowed. `app/main.py:L50` mounts the document router first, so
    `GET /{document_id}` claims `GET /me` and this handler never runs.
    """
    return current_user

@router.put('/me')
def update_user(user_update: UserUpdate, current_user: User = Depends(get_current_user)) -> User:
    """Apply a profile update for the authenticated caller.

    Args:
        user_update: Request body declared `UserUpdate`, carrying optional `email`,
            `username`, `full_name` and `password`.
        current_user: The caller, injected through `Depends(get_current_user)`.

    Returns:
        The updated `User` the service returns.

    Raises:
        HTTPException: HTTP 400, detail `"Failed to update user"`, when the
            update yields a falsy result.
    \N{FORM FEED}
    Internal notes.

    Note:
        The service call is not awaited, so a coroutine result would be truthy and pass
        the check unexecuted. See the assistance marker below, which records that the
        `UserService.update_user` contract is unverified.
    """
    # HUMAN ASSISTANCE NEEDED
    # The following code assumes the existence of a UserService class with an update_user method.
    # Please verify if this implementation aligns with your actual UserService implementation.
    user_service = UserService()
    updated_user = user_service.update_user(current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=400, detail="Failed to update user")
    return updated_user