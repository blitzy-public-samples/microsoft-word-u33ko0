"""Build the router for the create, read, update and delete (CRUD) template routes.

Five handlers serve `POST /`, `GET /`, `GET /{template_id}`,
`PUT /{template_id}` and `DELETE /{template_id}` of the application programming
interface (API). L8 exports `router`. Every handler declares
`current_user: User = Depends(get_current_user)`, so all five routes require a
bearer token. L5 imports that dependency from `app.api.auth`, which defines it
at `app/api/auth.py:L14`.

Access control. Bearer authentication is the only control this module implements,
and it is the only one any committed file can verify. The dependency at
`app/api/auth.py:L14-L26` decodes a token and returns the matching user, so it
answers who is calling. The dependency does not establish what that caller may reach.

Object-level authorization is unimplemented here and unverifiable anywhere. No
handler below compares a template's owner against `current_user`, reads a role,
consults an access-control list or inspects a share list. Each handler forwards
`current_user` to the service and returns whatever comes back, so any
authorization decision would have to live in `TemplateService`. That class does
not exist: `app.services.template_service` is absent, so no contract states
whether such a check happens, and none can be inferred. The four backend document
routes take the opposite approach and compare ownership in the router body, at
`app/api/documents.py:L26`, `:L34` and `:L43`.

Error text is not a control. L35 and L43 send the detail
`"Template not found or user not authorized"`. The string names authorization,
and the code that produces it tests only a falsy service result, at L34 and L42.
A falsy result cannot separate an absent template from a forbidden one, so the
detail describes two conditions the handler never distinguishes. Reading that
wording as evidence of an ownership check would be a mistake.

Implementing a check would add production logic, so this pass records the gap
only.

The module cannot import. L3 requests `Template`, `TemplateCreate` and
`TemplateUpdate` from `app.schema.template`, and L4 requests `TemplateService`
from `app.services.template_service`. Neither module exists, so L3 raises
`ModuleNotFoundError` first. Those four names stay unresolved throughout the
file, so nothing defines what the handler calls below must pass. The
decorators at L10, L16, L22, L30 and L38 never execute, and `router` never
gains a route.

Export name mismatch: `app/main.py:L6` imports `templates_router` from this
module. L8 defines `router`, and no `templates_router` name exists here.

Route collision: `app/main.py:L50` mounts the document router with no prefix,
then `app/main.py:L52` mounts this router the same way. `POST /` at L10 and
`GET /` at L16 repeat the paths that `app/api/documents.py:L10` and
`app/api/documents.py:L16` already claim. The dynamic paths repeat them too,
because `/{template_id}` and `/{document_id}` compile to the same
single-segment pattern and the parameter name does not affect the match.
Starlette matches in registration order, so all five handlers below are
unreachable through the assembled application.

Line locators: every `Lnn` reference below numbers the tree at commit
06be74c7c88aa6bca652d465eaa00ad480a9e5c5, the frozen revision that precedes this
documentation pass. A bare `Lnn` points into this file, and a `path:Lnn` points into
the named file. Current HEAD numbers each documented file higher.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schema.template import Template, TemplateCreate, TemplateUpdate
from app.services.template_service import TemplateService
from app.api.auth import get_current_user
from app.schema.user import User

router = APIRouter()

@router.post('/')
async def create_template(template: TemplateCreate, current_user: User = Depends(get_current_user)) -> Template:
    """Create a template for the authenticated caller.

    L13 awaits `template_service.create_template(template, current_user)` and
    passes the whole `current_user` object.

    The handler authenticates and forwards. The dependency at L11 requires a
    bearer token, and no line below checks a role or a quota, so any
    authenticated caller can request a template. Whether the absent service
    records `current_user` as the owner is not stated anywhere.

    Args:
        template: The request body, declared `TemplateCreate`, one of the
            unresolved names imported at L3.
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `Template` named in the return annotation, returned at L14.
        `Template` is also unresolved at L3.

    Side effects:
        The decorator at L10 sets no `status_code`, so a success returns
        hypertext transfer protocol (HTTP) status 200.
    """
    template_service = TemplateService()
    created_template = await template_service.create_template(template, current_user)
    return created_template

@router.get('/')
async def get_templates(current_user: User = Depends(get_current_user)) -> List[Template]:
    """List templates for the authenticated caller.

    L19 awaits `template_service.get_templates(current_user)`.

    The handler authenticates and forwards. L20 returns the service result
    unfiltered, and no line scopes the list to the caller. Whether the absent
    service filters by owner is not stated anywhere, so this route offers no
    verifiable guarantee that a caller sees only their own templates.

    Args:
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `List[Template]` named in the return annotation, returned at L20.
        `Template` is unresolved at L3.
    """
    template_service = TemplateService()
    templates = await template_service.get_templates(current_user)
    return templates

@router.get('/{template_id}')
async def get_template(template_id: str, current_user: User = Depends(get_current_user)) -> Template:
    """Retrieve one template.

    L25 awaits `template_service.get_template(template_id, current_user)`,
    passing both the path parameter and the caller. L26 tests the result for
    falsity, which is the only condition this handler inspects.

    Args:
        template_id: Path parameter, declared `str`, naming the template to
            read.
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `Template` named in the return annotation, returned at L28.
        `Template` is unresolved at L3.

    The handler authenticates and forwards. L26 tests the service result for
    falsity and nothing else, so the route implements no ownership comparison. A
    caller who supplies another user's `template_id` receives that template
    unless the absent service refuses, and no contract says it would.

    Raises:
        HTTPException: HTTP 404 at L27, detail `"Template not found"`, when the
            L25 result is falsy. The detail names no authorization condition
            here, unlike L35 and L43.
    """
    template_service = TemplateService()
    template = await template_service.get_template(template_id, current_user)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.put('/{template_id}')
async def update_template(template_id: str, template: TemplateUpdate, current_user: User = Depends(get_current_user)) -> Template:
    """Apply an update to one template.

    L33 awaits
    `template_service.update_template(template_id, template, current_user)`.
    L34 tests the result for falsity.

    Args:
        template_id: Path parameter, declared `str`, naming the template to
            update.
        template: The request body, declared `TemplateUpdate`, one of the
            unresolved names imported at L3.
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `Template` named in the return annotation, returned at L36.
        `Template` is unresolved at L3.

    The handler authenticates and forwards. L34 tests the service result for
    falsity and nothing else, so the route implements no ownership comparison
    before it accepts a write to a template the caller may not own.

    Raises:
        HTTPException: HTTP 404 at L35, detail
            `"Template not found or user not authorized"`, when the L33 result
            is falsy. The single status covers the absent template and the
            unauthorized caller, because a falsy result does not separate them.
            The detail names authorization, and no line in this module performs an
            authorization check, so the wording is response text rather than
            evidence of a control. `app.services.template_service` is absent, so
            no contract shows that the service performs one either.
    """
    template_service = TemplateService()
    updated_template = await template_service.update_template(template_id, template, current_user)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Template not found or user not authorized")
    return updated_template

@router.delete('/{template_id}')
async def delete_template(template_id: str, current_user: User = Depends(get_current_user)) -> dict:
    """Delete one template.

    L41 awaits `template_service.delete_template(template_id, current_user)`.
    L42 tests the result for falsity.

    The handler authenticates and forwards. L42 tests the service result for
    falsity and nothing else, so the route implements no ownership comparison
    before it accepts a delete of a template the caller may not own.

    Args:
        template_id: Path parameter, declared `str`, naming the template to
            delete.
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `dict` named in the return annotation. L44 returns the literal
        `{"message": "Template deleted successfully"}`.

    Raises:
        HTTPException: HTTP 404 at L43, detail
            `"Template not found or user not authorized"`, when the L41 result
            is falsy. The detail names authorization, and no line in this module
            performs an authorization check, so the wording is response text
            rather than evidence of a control. `app.services.template_service` is
            absent, so no contract shows that the service performs one either.

    Side effects:
        The decorator at L38 sets no `status_code`, so a success returns HTTP
        status 200. L44 returns a fixed message, so the response reports nothing
        about what the service deleted.
    """
    template_service = TemplateService()
    deleted = await template_service.delete_template(template_id, current_user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Template not found or user not authorized")
    return {"message": "Template deleted successfully"}