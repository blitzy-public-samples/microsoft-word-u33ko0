"""Build the router for the two current-user profile routes.

`GET /me` returns the authenticated user and `PUT /me` updates it. Both are
declared with a plain `def` rather than `async def`, unlike every other
handler in this package.

`app.services.user_service` does not exist, and this module imports it at
module level, so neither route is registered. Both routes read the caller's
own identity from the dependency and take no user identifier from the
request. See ./README.md for the path collision with the document routes.
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
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        That same `User`, unchanged.
    """
    return current_user

@router.put('/me')
def update_user(user_update: UserUpdate, current_user: User = Depends(get_current_user)) -> User:
    """Update the authenticated caller's own profile.

    The update is scoped to `current_user.id`, so the route takes no user
    identifier from the request. The absent service makes its sync/async
    contract unknowable, and this plain handler calls it synchronously. See
    the HUMAN ASSISTANCE NEEDED marker below.

    Args:
        user_update: Validated request body, declared `UserUpdate`, whose
            four fields are all optional.
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        The updated `User`, as the return annotation declares.

    Raises:
        HTTPException: 400 with the detail `"Failed to update user"` when
            the update yields a falsy value.
    """
    # HUMAN ASSISTANCE NEEDED
    # The following code assumes the existence of a UserService class with an update_user method.
    # Please verify if this implementation aligns with your actual UserService implementation.
    user_service = UserService()
    updated_user = user_service.update_user(current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=400, detail="Failed to update user")
    return updated_user