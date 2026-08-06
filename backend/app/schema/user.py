"""Declare the Pydantic contracts for user records.

Four models: `UserBase`, `UserCreate`, `UserUpdate` and `User`. The module imports
cleanly. `List` is imported and unused.

Pydantic publishes each model's own docstring as the `description` of the JSON
Schema it generates, and FastAPI copies that schema into the OpenAPI document it
serves. Every class docstring below therefore states the public contract only,
and the internal analysis for all four models sits in this module docstring,
which Pydantic never publishes.

Every import here resolves and `import app.schema.user` succeeds. Only three of
the fifteen modules under `backend/app/` import cleanly, and `app.schema.user`
is one of them. `List` on the `typing` import line is imported and never used.
`orm_mode = True` in the nested `Config` is the Pydantic 1.x spelling, so
attribute-based construction here depends on Pydantic 1.x.

Consumers. `app/api/auth.py:L7` imports `User` and `UserCreate`, and
`app/api/auth.py:L43` annotates the `register_user` parameter with `UserCreate`.
`app/api/users.py:L2` imports `User` and `UserUpdate`, and `app/api/users.py:L13`
is the only consumer of `UserUpdate`. `app/api/documents.py:L6` and
`app/api/templates.py:L6` import `User`. `UserUpdate` extends `BaseModel` rather
than `UserBase`, so it shares no field definition with the create path.

No field carries a length bound. `email`, `username` and `full_name` at L6-L8,
`password` at L11 and the four `UserUpdate` fields at L14-L17 all carry bare `str`
or `Optional[str]` annotations with no `min_length` and no `max_length`, and no
model declares a `@validator`. No route and no committed middleware caps the
request body size either, so a caller can submit an arbitrarily large value in any
field. `POST /register` is public, because `app/api/auth.py:L42` declares no
authentication dependency, so an unauthenticated caller reaches the unbounded
`UserCreate` fields directly.

No password policy applies to `UserCreate.password`. The bare `str` at L11 carries
no non-empty check and no regular expression, so the empty string, a single
character and any common password all validate, and `app/api/auth.py:L48` hashes
whatever arrives. `frontend/src/utils/validation.ts:L8-L15` declares a length and
character policy, and no module calls it, so the client validator cannot protect
this contract even if it ran.

`User` declares no field for the password hash that `app/api/auth.py:L48`
computes, so a response validated against `User` cannot carry that hash. The
guarantee stops at this contract. `app/api/auth.py:L43` declares no return
annotation and its decorator at `:L42` sets no `response_model`, so `POST
/register` returns the absent service's result unfiltered at `:L50`. Nothing
constrains that value to `User`, so hash exposure on the registration response
cannot be ruled out from this file.

The two authorization flags on `User` are declared and never read. No code path in
the repository reads `is_active` or `is_superuser`; both names appear only as
declarations across every `.py`, `.ts` and `.tsx` file. The consequence for
`is_active` is concrete. `app/api/auth.py:L14-L26` resolves a bearer token,
fetches the user at `:L23` and returns it at `:L26` without testing the flag, so a
valid token issued to a deactivated account passes the dependency. Deactivating a
user therefore revokes nothing until the token expires. The `User` docstring below
records which of the twelve protected routes such a token actually reaches.

`User` declares neither `name` nor `avatar`, and `updated_at` has no counterpart
in the client-side user contract. `docs/data-model.md` records both divergences.

`app/services/user_service.py` does not exist, though `app/api/auth.py:L8` and
`app/api/users.py:L3` both import it.

Line references point at the pre-documentation layout of commit `06be74c`, so
they exclude docstrings added by this pass.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    """Carry the fields shared by every user representation.

    Attributes:
        email: Email address. Required, and declared `str` rather than `EmailStr`, so no
            format check runs.
        username: Display name. Required.
        full_name: Full name. Optional, defaulting to `None`.
    """
    email: str
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """Carry a user registration request body.

    Extends `UserBase` and adds the required plaintext `password` that the
    registration route hashes before it creates an account.

    Attributes:
        password: Plain-text password. Required, declared `str` with no length bound and
            no pattern, so the contract accepts a single character.
    """
    password: str

class UserUpdate(BaseModel):
    """Request body for updating a user.

    Extends `BaseModel` rather than `UserBase`, so the model redeclares `email`,
    `username` and `full_name` locally. Every field is optional, so a caller may
    send any subset of the four.

    Attributes:
        email: Replacement email address. Optional.
        username: Replacement display name. Optional.
        full_name: Replacement full name. Optional.
        password: Replacement plain-text password. Optional.
    """
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    """Represent a stored user returned to the caller.

    `User` extends `UserBase`, travels outward as a response model, and carries
    the nested `Config` class below. `app/api/auth.py:L7`,
    `app/api/users.py:L2`, `app/api/documents.py:L6` and
    `app/api/templates.py:L6` import this model.

    `User` declares no field for the password hash that `app/api/auth.py:L48`
    computes, so a response validated against this contract cannot carry that
    hash. The module docstring above records why that guarantee stops at this
    contract and does not reach the `POST /register` response.

    The two authorization flags are declared and never read. No code path in the
    repository reads `is_active` or `is_superuser`; both names appear only as
    declarations across every `.py`, `.ts` and `.tsx` file.

    The consequence for `is_active` sits in the token dependency.
    `app/api/auth.py:L14-L26` resolves a bearer token, fetches the user at `:L23`
    and returns it at `:L26` without testing the flag, so wherever that
    dependency is invoked it accepts a valid token issued to an account that was
    later deactivated. The dependency reports no difference between an active and
    a deactivated account, so deactivating a user revokes nothing until the token
    expires.

    Route reachability is a separate question, and the answer is narrower.
    `import app.main` fails at `app/main.py:L3`, then at `app/api/auth.py:L6`,
    with `ImportError: cannot import name 'settings' from 'app.core.config'`, so
    no route is served at all as committed and the dependency is invoked nowhere.
    Repairing that import does not make all twelve protected routes reachable
    either. `app/main.py:L49-L52` mounts every router with no prefix, so
    `GET /{document_id}` at `app/api/documents.py:L22` and `PUT /{document_id}` at
    `:L30` shadow `GET /me` and `PUT /me` at `app/api/users.py:L8` and `:L12`, and
    all five routes in `app/api/templates.py` repeat paths the documents router
    claimed first at `app/main.py:L50`. Seven of the twelve protected handlers are
    therefore unreachable through the assembled route order, leaving the five
    document routes as the ones a deactivated account would actually reach.

    `User` declares neither `name` nor `avatar`, and `updated_at` has no
    counterpart in the client-side user contract. `docs/data-model.md` records
    both divergences.

    Attributes:
        id: User identifier. Required.
        created_at: Creation timestamp. Required.
        updated_at: Last-modification timestamp. Required.
        is_active: Whether the account is enabled. Required, and read by no code path,
            so neither current-user dependency rejects a deactivated user.
        is_superuser: Whether the account holds elevated rights. Required, and read by
            no code path, so no route grants anything on it.

    Note:
        `orm_mode` lets the model read attributes off an object rather than a
        dictionary, and no ORM model is declared anywhere in the backend for it to read.
    """
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_superuser: bool

    class Config:
        """Enable attribute-based population under Pydantic 1.x."""
        orm_mode = True