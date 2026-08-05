"""Define the Pydantic user contracts for the API boundary.

Four models cover the shared field shape, the registration request body, the
partial update patch, and the read model that the application programming
interface (API) returns to callers. `User` carries a nested `Config` class.

Every import here resolves and `import app.schema.user` succeeds. Only three of
the fifteen modules under `backend/app/` import cleanly, and `app.schema.user`
is one of them. `List` on the `typing` import line is imported and never used.
`orm_mode = True` in the nested `Config` is the Pydantic 1.x spelling, so
attribute-based construction here depends on Pydantic 1.x.

`User` declares no field for the password hash that `app/api/auth.py:L48`
computes, so a response validated against `User` cannot carry that hash. The
guarantee stops at this contract. `app/api/auth.py:L43` declares no return
annotation and its decorator at `:L42` sets no `response_model`, so `POST
/register` returns the absent service's result unfiltered at `:L50`. Nothing
constrains that value to `User`, so hash exposure on the registration response
cannot be ruled out from this file.

`app/services/user_service.py` does not exist, though `app/api/auth.py:L8` and
`app/api/users.py:L3` both import it.
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
    that `app/api/auth.py:L48` reads and hashes. `app/api/auth.py:L43`
    annotates the `register_user` parameter with this model, and
    `app/api/auth.py:L7` imports it.

    No password policy applies. `password` at L11 carries a bare `str`
    annotation with no `min_length`, no `max_length`, no regular expression and
    no non-empty check, and the class declares no `@validator`. The empty
    string, a single character and any common password all validate, and
    `app/api/auth.py:L48` hashes whatever arrives. The route that accepts this
    model is public, because `app/api/auth.py:L42` declares no authentication
    dependency, so any caller can create an account with a trivial password.
    `frontend/src/utils/validation.ts:L8-L15` declares a length and character
    policy, and no module calls it, so the client validator cannot protect this
    contract even if it ran.

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
    and `full_name` locally. `app/api/users.py:L13` is the only consumer, and
    `app/api/users.py:L2` imports it.

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
    the nested `Config` class below. `app/api/auth.py:L7`,
    `app/api/users.py:L2`, `app/api/documents.py:L6` and
    `app/api/templates.py:L6` import this model.

    `User` declares no field for the password hash that `app/api/auth.py:L48`
    computes and `app/api/auth.py:L49` passes to `UserService.create_user`, so
    a response validated against this contract cannot carry that hash.
    `POST /register` is not validated against it. `app/api/auth.py:L43` declares
    no return annotation and `:L42` sets no `response_model`, so `:L50` returns
    the absent service's value unfiltered and this contract does not bound the
    registration response.

    The two authorization flags are declared and never read. No code path in the
    repository reads `is_active` or `is_superuser`; both names appear only as
    declarations across every `.py`, `.ts` and `.tsx` file. The consequence for
    `is_active` is concrete: `app/api/auth.py:L14-L26` resolves a bearer token,
    fetches the user at `:L23` and returns it at `:L26` without testing the
    flag, so a valid token issued to a deactivated account passes the dependency
    and reaches all twelve protected routes. Deactivating a user therefore
    revokes nothing until the token expires. Adding the check would change the
    dependency, so this pass records the gap only.

    `User` declares neither `name` nor `avatar`, and `updated_at` has no
    counterpart in the client-side user contract. `docs/data-model.md` records
    both divergences.

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