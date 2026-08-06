"""Build the router for the five document-template routes.

Five handlers serve `POST /`, `GET /`, `GET /{template_id}`, `PUT /{template_id}` and
`DELETE /{template_id}`, all behind `get_current_user`. The module exports `router`.

Two imports name modules that do not exist: `app.schema.template` for `Template`,
`TemplateCreate` and `TemplateUpdate`, and `app.services.template_service` for
`TemplateService`. `app/main.py` imports the name `templates_router` from this module,
and this module defines `router`.

Object-level authorization is unimplemented here and unverifiable anywhere. No
handler below compares a template's owner against `current_user`, reads a role,
consults an access-control list or inspects a share list. Each handler forwards
`current_user` to the service and returns whatever comes back, so any
authorization decision would have to live in `TemplateService`. That class does
not exist: `app.services.template_service` is absent, so no contract states
whether such a check happens, and none can be inferred. Three of the five backend
document routes take the opposite approach and compare ownership in the router
body, at `app/api/documents.py:L187`, `:L34` and `:L43`; the create and list routes
at `:L10` and `:L16` compare nothing.

Error text is not a control. L35 and L43 send the detail
`"Template not found or user not authorized"`. The string names authorization,
and the code that produces it tests only a falsy service result, at L34 and L42.
A falsy result cannot separate an absent template from a forbidden one, so the
detail describes two conditions the handler never distinguishes. Reading that
wording as evidence of an ownership check would be a mistake.

No caller reaches a template handler as committed, so every authorization
statement in this module describes a hypothetical rather than a live control.
Three independent barriers block that reach, each one sufficient on its own, and
the three paragraphs below set them out in turn: the import failure at L3, the
`templates_router` export mismatch against `app/main.py:L19`, and the route
collision with the document router.

Once all three are repaired, no line below narrows the reach: any authenticated
caller would then hold every template identifier, because no handler compares an
owner and no committed file supplies a service that could.

The module cannot import. L3 requests `Template`, `TemplateCreate` and
`TemplateUpdate` from `app.schema.template`, and L4 requests `TemplateService`
from `app.services.template_service`. Neither module exists, so L3 raises
`ModuleNotFoundError` first. Those four names stay unresolved throughout the
file, so nothing defines what the handler calls below must pass. The
decorators at L10, L16, L22, L30 and L38 never execute, and `router` never
gains a route.

Export name mismatch: `app/main.py:L19` imports `templates_router` from this
module. L8 defines `router`, and no `templates_router` name exists here.

Route collision: `app/main.py:L126` mounts the document router with no prefix,
then `app/main.py:L128` mounts this router the same way. `POST /` at L10 and
`GET /` at L16 repeat the paths that `app/api/documents.py:L56` and
`app/api/documents.py:L114` already claim. The dynamic paths repeat them too,
because `/{template_id}` and `/{document_id}` compile to the same
single-segment pattern and the parameter name does not affect the match.
Starlette matches in registration order, so all five handlers below are
unreachable through the assembled application.

Each handler below splits its docstring at a form-feed marker, spelled as the
Unicode named escape for that character. FastAPI publishes the text above that
marker as the route description in the generated OpenAPI document and drops
everything below it. Each lower section is labelled "Internal notes" and carries
locators, absent-module names and the call-specific authorization facts. The
general account of what this module does and does not control sits above, under
"Access control", and no handler repeats it.

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

    The route requires a bearer token. A success returns hypertext transfer
    protocol (HTTP) status 200, because the decorator sets no `status_code`.

    Args:
        template: The request body, declared `TemplateCreate`.
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `Template` named in the return annotation.
    \N{FORM FEED}
    Internal notes.

    L13 awaits `template_service.create_template(template, current_user)` and
    passes the whole `current_user` object. L14 returns the service result.
    `TemplateCreate` and `Template` are both unresolved names imported at L3.
    The decorator sits at L10.

    The handler authenticates and forwards. The dependency at L11 requires a
    bearer token, and no line below checks a role or a quota, so any
    authenticated caller can request a template. Whether the absent service
    records `current_user` as the owner is not stated anywhere.

    No side effect executes as committed. L12 instantiates `TemplateService`, a
    name L4 imports from the absent module `app.services.template_service`, so
    the module raises `ModuleNotFoundError` at L3 before the decorator at L10 is
    ever evaluated. No external write can be established either way, because the
    absent service defines no persistence behavior: nothing in the repository
    states which store a created template would reach, which fields it would
    carry, or whether `current_user` would be recorded as its owner. L10 sets no
    `status_code`, so a success would carry hypertext transfer protocol (HTTP)
    status 200.
    """
    template_service = TemplateService()
    created_template = await template_service.create_template(template, current_user)
    return created_template

@router.get('/')
async def get_templates(current_user: User = Depends(get_current_user)) -> List[Template]:
    """List templates for the authenticated caller.

    The route requires a bearer token. A success returns HTTP status 200,
    because the decorator sets no `status_code`.

    Args:
        current_user: The caller, injected through `Depends(get_current_user)`.

    Returns:
        The `List[Template]` named in the return annotation.
    \N{FORM FEED}
    Internal notes.

    L19 awaits `template_service.get_templates(current_user)` and L20 returns the
    result. `Template` is an unresolved name imported at L3, and the decorator
    sits at L16. L16 sets no `status_code`, so a success would carry HTTP status
    200.

    The handler authenticates and forwards. L20 returns the service result
    unfiltered, and no line scopes the list to the caller. Whether the absent
    service filters by owner is not stated anywhere, so this route offers no
    verifiable guarantee that a caller sees only their own templates.

    A read is the only effect the route would have, and none executes as
    committed, because the awaited call at L19 never runs: L3 raises
    `ModuleNotFoundError` at import.
    """
    template_service = TemplateService()
    templates = await template_service.get_templates(current_user)
    return templates

@router.get('/{template_id}')
async def get_template(template_id: str, current_user: User = Depends(get_current_user)) -> Template:
    """Retrieve one template.

    The route requires a bearer token. A success returns HTTP status 200,
    because the decorator sets no `status_code`.

    Args:
        template_id: Path parameter naming the template to read.
        current_user: The caller, injected through `Depends(get_current_user)`.

    Returns:
        The `Template` named in the return annotation.

    Raises:
        HTTPException: HTTP 404, detail `"Template not found"`, when the lookup
            yields no template.
    \N{FORM FEED}
    Internal notes.

    L25 awaits `template_service.get_template(template_id, current_user)`,
    passing both the path parameter and the caller. L26 tests the result for
    falsity, which is the only condition this handler inspects. L28 returns the
    result, `Template` is an unresolved name imported at L3, the decorator sits
    at L22 and the 404 at L27. L22 sets no `status_code`, so a success would
    carry HTTP status 200.

    A read is the only effect the route would have, and none executes as
    committed, because the awaited call at L25 never runs: L3 raises
    `ModuleNotFoundError` at import.

    The handler authenticates and forwards. L26 tests the service result for
    falsity and nothing else, so the route implements no ownership comparison. A
    caller who supplies another user's `template_id` would receive that template
    unless the absent service refused, and no contract says it would.

    The 404 detail names no authorization condition here, unlike L35 and L43.
    """
    template_service = TemplateService()
    template = await template_service.get_template(template_id, current_user)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.put('/{template_id}')
async def update_template(template_id: str, template: TemplateUpdate, current_user: User = Depends(get_current_user)) -> Template:
    """Apply an update to one template.

    The route requires a bearer token. A success returns HTTP status 200,
    because the decorator sets no `status_code`. Actual side effects are none.
    The handler is intended to store the changed fields, and no committed file
    states which fields an update would change or whether the change is partial.
    documentation/Technical Specifications.md, SYSTEM DESIGN > API DESIGN
    (L431), declares the route `PUT /templates/{id}` and no persistence detail.

    Args:
        template_id: Path parameter, declared `str`, naming the template to
            update.
        template: The request body, declared `TemplateUpdate`.
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `Template` named in the return annotation.

    Raises:
        HTTPException: HTTP 404, detail
            `"Template not found or user not authorized"`, when the update
            yields no template. The single status covers both an absent template
            and a caller the update refuses.
    \N{FORM FEED}
    Internal notes.

    L33 awaits
    `template_service.update_template(template_id, template, current_user)`.
    L34 tests the result for falsity and L36 returns it. `TemplateUpdate` and
    `Template` are both unresolved names imported at L3, the decorator sits at
    L30 and the 404 at L35. L30 sets no `status_code`, so a success would carry
    HTTP status 200.

    No write executes as committed. The awaited call at L33 never runs, because L3
    raises `ModuleNotFoundError` at import. No external write can be established
    either way: the absent service defines no persistence behavior, so nothing in
    the repository states which fields an update would change, whether the change
    is partial or a full replacement, or whether ownership is checked before the
    write.

    The handler authenticates and forwards. L34 tests the service result for
    falsity and nothing else, so the route implements no ownership comparison
    before it accepts a write to a template the caller may not own.

    A falsy result does not separate an absent template from a forbidden one. The
    L35 detail names authorization, and no line in this module performs an
    authorization check, so the wording is response text rather than evidence of a
    control. `app.services.template_service` is absent, so no contract shows that
    the service performs one either.
    """
    template_service = TemplateService()
    updated_template = await template_service.update_template(template_id, template, current_user)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Template not found or user not authorized")
    return updated_template

@router.delete('/{template_id}')
async def delete_template(template_id: str, current_user: User = Depends(get_current_user)) -> dict:
    """Delete one template.

    The route requires a bearer token. A success returns HTTP status 200,
    because the decorator sets no `status_code`. Actual side effects are none.
    The handler is intended to remove the stored template, and no committed file
    states which store a delete would reach or whether the removal is hard or
    soft. documentation/Technical Specifications.md, SYSTEM DESIGN > API DESIGN
    (L432), declares the route `DELETE /templates/{id}` and no persistence
    detail.

    Args:
        template_id: Path parameter naming the template to delete.
        current_user: The caller, injected through `Depends(get_current_user)`.

    Returns:
        The `dict` named in the return annotation, holding the literal
        `{"message": "Template deleted successfully"}`. The message is fixed, so
        the response reports nothing about what was deleted.

    Raises:
        HTTPException: HTTP 404, detail
            `"Template not found or user not authorized"`, when the delete
            yields a falsy result. The single status covers both an absent
            template and a caller the delete refuses.
    \N{FORM FEED}
    Internal notes.

    L41 awaits `template_service.delete_template(template_id, current_user)` and
    L42 tests the result for falsity. The decorator sits at L38, the 404 at L43,
    and L44 returns the fixed message. L38 sets no `status_code`, so a success
    would carry HTTP status 200.

    The handler authenticates and forwards. L42 tests the service result for
    falsity and nothing else, so the route implements no ownership comparison
    before it accepts a delete of a template the caller may not own.

    The L43 detail names authorization, and no line in this module performs an
    authorization check, so the wording is response text rather than evidence of a
    control. `app.services.template_service` is absent, so no contract shows that
    the service performs one either.

    No delete executes as committed. The awaited call at L41 never runs, because
    L3 raises `ModuleNotFoundError` at import. No external delete can be
    established either way: the absent service defines no deletion behavior, so
    nothing in the repository states which store a delete would reach, whether the
    removal is hard or soft, or whether any dependent record is cleaned up.
    """
    template_service = TemplateService()
    deleted = await template_service.delete_template(template_id, current_user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Template not found or user not authorized")
    return {"message": "Template deleted successfully"}