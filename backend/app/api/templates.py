"""Expose authenticated template CRUD routes.

The template schema, template service, and router export expected by app.main
are unresolved.
Bearer authentication is the only verifiable control. No handler performs an
ownership or role check, and the absent service supplies no contract that
proves object authorization. Authorization-flavored error text is not a check.
The application mounts this router after the document router with no prefix,
so the matching collection and identifier paths are unreachable.
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
        template: A TemplateCreate carrying the new template's fields.
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        The created template, declared `Template`.

    Side effects:
        Writes one template through TemplateService.
    """
    template_service = TemplateService()
    created_template = await template_service.create_template(template, current_user)
    return created_template

@router.get('/')
async def get_templates(current_user: User = Depends(get_current_user)) -> List[Template]:
    """List the templates available to the authenticated caller.

    Args:
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        The caller's templates, declared `List[Template]`.
    """
    template_service = TemplateService()
    templates = await template_service.get_templates(current_user)
    return templates

@router.get('/{template_id}')
async def get_template(template_id: str, current_user: User = Depends(get_current_user)) -> Template:
    """Return one template belonging to the authenticated caller.

    Args:
        template_id: Identifier of the template to read.
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        The requested template, declared `Template`.

    Raises:
        HTTPException: 404 when the service returns a falsy value.
    """
    template_service = TemplateService()
    template = await template_service.get_template(template_id, current_user)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.put('/{template_id}')
async def update_template(template_id: str, template: TemplateUpdate, current_user: User = Depends(get_current_user)) -> Template:
    """Apply a change to a template belonging to the authenticated caller.

    Args:
        template_id: Identifier of the template to change.
        template: A TemplateUpdate holding the replacement fields.
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        The updated template, declared `Template`.

    Raises:
        HTTPException: 404 when the service returns a falsy value, which
            covers both a missing template and a failed authorization check.

    Side effects:
        Writes the supplied fields through TemplateService.
    """
    template_service = TemplateService()
    updated_template = await template_service.update_template(template_id, template, current_user)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Template not found or user not authorized")
    return updated_template

@router.delete('/{template_id}')
async def delete_template(template_id: str, current_user: User = Depends(get_current_user)) -> dict:
    """Delete a template belonging to the authenticated caller.

    Args:
        template_id: Identifier of the template to remove.
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        A dictionary holding a confirmation message, declared `dict`.

    Raises:
        HTTPException: 404 when the service returns a falsy value, which
            covers both a missing template and a failed authorization check.

    Side effects:
        Deletes the template through TemplateService.
    """
    template_service = TemplateService()
    deleted = await template_service.delete_template(template_id, current_user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Template not found or user not authorized")
    return {"message": "Template deleted successfully"}