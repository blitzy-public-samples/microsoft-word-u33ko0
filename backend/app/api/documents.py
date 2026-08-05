"""Expose authenticated document CRUD routes.

The router export name and several service calls do not match their consumers.
Four mismatch categories cover ten sites: one wrong argument type, one absent
service method, five arity errors, and three reads of an undeclared user_id
field.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schema.document import Document, DocumentCreate, DocumentUpdate
from app.services.document_service import DocumentService
from app.api.auth import get_current_user
from app.schema.user import User

router = APIRouter()

@router.post('/')
async def create_document(document: DocumentCreate, current_user: User = Depends(get_current_user)) -> Document:
    """Create a document for the authenticated caller.

    \N{FORM FEED}

    Args:
        document: A DocumentCreate carrying the title and content to store.
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        The created document, declared `Document`.

    Side effects:
        Writes one document through DocumentService. The service expects a
        `user_id` string, and this call passes the whole User object.
    """
    document_service = DocumentService()
    created_document = await document_service.create_document(document, current_user)
    return created_document

@router.get('/')
async def get_documents(current_user: User = Depends(get_current_user)) -> List[Document]:
    """List the documents belonging to the authenticated caller.

    \N{FORM FEED}

    Args:
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        The caller's documents, declared `List[Document]`.

    Raises:
        AttributeError: DocumentService defines no `get_documents` method.
    """
    document_service = DocumentService()
    documents = await document_service.get_documents(current_user)
    return documents

@router.get('/{document_id}')
async def get_document(document_id: str, current_user: User = Depends(get_current_user)) -> Document:
    """Return one document after comparing its owner with the caller.

    \N{FORM FEED}

    The comparison reads `user_id` from the result, while the Document
    contract declares `owner_id`.

    Args:
        document_id: Identifier of the document to read.
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        The requested document, declared `Document`.

    Raises:
        HTTPException: 403 when the stored owner differs from the caller.
        TypeError: The service call omits the required `user_id` argument.
    """
    document_service = DocumentService()
    document = await document_service.get_document(document_id)
    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this document")
    return document

@router.put('/{document_id}')
async def update_document(document_id: str, document: DocumentUpdate, current_user: User = Depends(get_current_user)) -> Document:
    """Apply a partial change to a document the caller owns.

    \N{FORM FEED}

    Args:
        document_id: Identifier of the document to change.
        document: A DocumentUpdate holding the replacement fields.
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        The updated document, declared `Document`.

    Raises:
        HTTPException: 403 when the stored owner differs from the caller.
        TypeError: The first service call omits the required `user_id`
            argument.

    Side effects:
        None as committed: the preceding get_document call omits user_id and
        raises TypeError before the update operation.
    """
    document_service = DocumentService()
    existing_document = await document_service.get_document(document_id)
    if existing_document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this document")
    updated_document = await document_service.update_document(document_id, document)
    return updated_document

@router.delete('/{document_id}')
async def delete_document(document_id: str, current_user: User = Depends(get_current_user)) -> dict:
    """Delete a document the caller owns.

    \N{FORM FEED}

    Args:
        document_id: Identifier of the document to remove.
        current_user: The authenticated User, injected by `get_current_user`.

    Returns:
        A dictionary holding a confirmation message, declared `dict`.

    Raises:
        HTTPException: 403 when the stored owner differs from the caller.
        TypeError: The first service call omits the required `user_id`
            argument.

    Side effects:
        None as committed: the preceding get_document call omits user_id and
        raises TypeError before the delete operation.
    """
    document_service = DocumentService()
    existing_document = await document_service.get_document(document_id)
    if existing_document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this document")
    await document_service.delete_document(document_id)
    return {"message": "Document deleted successfully"}