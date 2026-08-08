"""Declare the Pydantic contracts for user accounts.

Four models cover the shared fields, the create and update payloads and the
read model. No model declares a password-hash field, so the hash that
`app/api/auth.py` computes on registration has nowhere to live in these
contracts.

`List` is imported and never used. The read model sets `orm_mode`, which is
the Pydantic 1.x spelling. The client contract in
`frontend/src/schema/user.ts` declares neither `updated_at` nor the two
boolean flags. See ./README.md for the field comparison.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    """Carry the fields every user representation shares.

    Attributes:
        email: Account email address, required. Declared `str`, so no
            address format is enforced.
        username: Display handle, required.
        full_name: Full name, optional.
    """
    email: str
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """Model the registration request body.

    Attributes:
        password: The submitted password, required. Declared `str` with no
            length bound and no pattern, and the model declares no
            validator, so any non-null string validates.
    """
    password: str

class UserUpdate(BaseModel):
    """Model the profile update request body.

    Every field is optional, so a caller may send any subset.

    Attributes:
        email: New email address, optional.
        username: New handle, optional.
        full_name: New full name, optional.
        password: New password, optional.
    """
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    """Model a stored account as the API returns it.

    Attributes:
        id: Account identifier.
        created_at: Creation timestamp.
        updated_at: Last-modification timestamp.
        is_active: Whether the account is enabled. No code path reads it,
            so neither token dependency rejects a deactivated account.
        is_superuser: Whether the account is privileged. No code path reads
            it, so no route grants elevated access.
    """
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_superuser: bool

    class Config:
        """Let Pydantic build this model from an object with attributes.

        Attributes:
            orm_mode: True. The setting is the Pydantic 1.x spelling, and
                no ORM model exists in the tree for it to read from.
        """
        orm_mode = True