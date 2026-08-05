"""Expose the authenticated user's profile routes.

UserService and the router name imported by app.main are unresolved.
The document router is mounted first, so its parameterized GET and PUT routes
match `/me` before these handlers.
"""
from fastapi import APIRouter, Depends, HTTPException
from app.schema.user import User, UserUpdate
from app.services.user_service import UserService
from app.api.auth import get_current_user

router = APIRouter()

@router.get('/me')
def get_current_user_info(current_user: User = Depends(get_current_user)) -> User:
    """Return the authenticated caller's own profile.

    \N{FORM FEED}

    Args:
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        The caller's user record, declared `User`.
    """
    return current_user

@router.put('/me')
def update_user(user_update: UserUpdate, current_user: User = Depends(get_current_user)) -> User:
    """Apply a profile patch for the authenticated caller.

    \N{FORM FEED}

    See the assistance marker in the comment block below. UserService is
    unresolved, so update_user's return contract cannot be verified. The
    synchronous handler calls the method without await and returns the result
    unchanged. Password hashing and storage are also unknowable.

    Args:
        user_update: A UserUpdate holding the replacement fields.
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        The updated user record, declared `User`.

    Raises:
        HTTPException: 400 when the update call returns a falsy value.
    """
    # HUMAN ASSISTANCE NEEDED
    # The following code assumes the existence of a UserService class with an update_user method.
    # Please verify if this implementation aligns with your actual UserService implementation.
    user_service = UserService()
    updated_user = user_service.update_user(current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=400, detail="Failed to update user")
    return updated_user