"""Build the router for the five document-template routes.

Nothing in this module can run. Two imports name modules that do not exist:
`app.schema.template`, for `Template`, `TemplateCreate` and
`TemplateUpdate`, and `app.services.template_service`, for `TemplateService`.
The five route paths repeat the five in `app/api/documents.py`, and
`app/main.py` mounts both routers without a prefix, so the document routes
registered first answer those paths.

Because `TemplateService` is absent, what each handler would do with a
template, including how it would treat ownership, cannot be established
from this repository. Each docstring below describes only what its own body
contains. See ./README.md for the combined route table.
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

    Args:
        template: Validated request body, declared `TemplateCreate` by an
            absent module.
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        The created `Template`, as the return annotation declares. The
        service that would build it does not exist.
    """
    template_service = TemplateService()
    created_template = await template_service.create_template(template, current_user)
    return created_template

@router.get('/')
async def get_templates(current_user: User = Depends(get_current_user)) -> List[Template]:
    """List the templates available to the authenticated caller.

    Args:
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        A `List[Template]`, as the return annotation declares. Which
        templates the absent service would return cannot be established
        here.
    """
    template_service = TemplateService()
    templates = await template_service.get_templates(current_user)
    return templates

@router.get('/{template_id}')
async def get_template(template_id: str, current_user: User = Depends(get_current_user)) -> Template:
    """Return one template by identifier.

    The body passes `current_user` to the service and performs no ownership
    comparison of its own, unlike the matching document handler. Whether
    the service would scope the lookup to the caller cannot be established,
    because `app.services.template_service` does not exist.

    Args:
        template_id: Template identifier from the path.
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        The matching `Template`, as the return annotation declares.

    Raises:
        HTTPException: 404 with the detail `"Template not found"` when the
            service returns a falsy value.
    """
    template_service = TemplateService()
    template = await template_service.get_template(template_id, current_user)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.put('/{template_id}')
async def update_template(template_id: str, template: TemplateUpdate, current_user: User = Depends(get_current_user)) -> Template:
    """Apply an update to one template.

    Args:
        template_id: Template identifier from the path.
        template: Validated request body, declared `TemplateUpdate` by an
            absent module.
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        The updated `Template`, as the return annotation declares.

    Raises:
        HTTPException: 404 with the detail
            `"Template not found or user not authorized"` when the service
            returns a falsy value. The one status covers both conditions,
            and the absent service decides which applies.
    """
    template_service = TemplateService()
    updated_template = await template_service.update_template(template_id, template, current_user)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Template not found or user not authorized")
    return updated_template

@router.delete('/{template_id}')
async def delete_template(template_id: str, current_user: User = Depends(get_current_user)) -> dict:
    """Delete one template.

    Args:
        template_id: Template identifier from the path.
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        A dict carrying the literal message `"Template deleted
        successfully"` when the service returns a truthy value.

    Raises:
        HTTPException: 404 with the detail
            `"Template not found or user not authorized"` when the service
            returns a falsy value.
    """
    template_service = TemplateService()
    deleted = await template_service.delete_template(template_id, current_user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Template not found or user not authorized")
    return {"message": "Template deleted successfully"}