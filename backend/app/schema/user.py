"""Define Pydantic request and response models for users.

Callers reference app.services.user_service, which is not present.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    """Describe the user fields shared by the create body and the read model.

    `UserBase` extends `BaseModel` and travels in both directions at the API
    boundary, because `UserCreate` and `User` both extend it. `UserUpdate` does
    not extend it.

    Attributes:
        email: Required `str` contact address. No email-format validation runs
            at this layer.
        username: Required `str` login name.
        full_name: Optional `str` full name, default `None`.
    """

    email: str
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """Carry a user registration request body.

    `UserCreate` extends `UserBase` and adds the required plaintext `password`
    submitted at registration. The field has no length, complexity, or
    non-empty constraint, so empty and common passwords validate.

    Attributes:
        password: Required `str` plaintext password submitted at registration.
        email: Inherited from `UserBase`. Required `str`.
        username: Inherited from `UserBase`. Required `str`.
        full_name: Inherited from `UserBase`. Optional `str`, default `None`.
    """

    password: str

class UserUpdate(BaseModel):
    """Carry a partial user update patch.

    `UserUpdate` extends `BaseModel` rather than `UserBase`, so the model shares
    no field definition with the create path and redeclares `email`, `username`
    and `full_name` locally.

    Attributes:
        email: Optional `str` replacement contact address, default `None`.
        username: Optional `str` replacement login name, default `None`.
        full_name: Optional `str` replacement full name, default `None`.
        password: Optional `str` replacement plaintext password, default `None`.
    """

    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    """Represent a stored user returned to the caller.

    `User` extends `UserBase`, travels outward as a response model, and carries
    the nested `Config` class below. The model declares no password-hash field,
    so a hash cannot appear in this response contract. Registration binds no
    response model and returns an absent service's value, so that route cannot
    guarantee the same filtering or even show where the hash is stored.

    No committed path reads `is_active` or `is_superuser`. A valid token for an
    inactive user therefore continues through the current authentication
    dependency until the token expires.

    Attributes:
        id: Required `str` identifier of the stored user.
        created_at: Required `datetime` recording when the user was created.
        updated_at: Required `datetime` recording the last modification.
        is_active: Required `bool` marking the user as active.
        is_superuser: Required `bool` marking elevated privileges.
        email: Inherited from `UserBase`. Required `str`.
        username: Inherited from `UserBase`. Required `str`.
        full_name: Inherited from `UserBase`. Optional `str`, default `None`.
    """

    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_superuser: bool

    class Config:
        """Configure the enclosing `User` model.

        `orm_mode = True` lets Pydantic build a `User` from an object's
        attributes rather than from a mapping, so a router can return a stored
        object directly as a `User`. Pydantic 2 renames the key to
        `from_attributes` and ignores `orm_mode` after emitting a warning.

        Attributes:
            orm_mode: `True`. The Pydantic 1.x spelling of the switch that
                enables attribute-based construction.
        """

        orm_mode = True