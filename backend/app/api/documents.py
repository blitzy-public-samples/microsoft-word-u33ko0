"""Build the router for the five document create, read, update and delete routes.

Every handler declares `get_current_user` as a dependency, constructs its own
`DocumentService` and compares ownership in its own body.

Three call-site contracts do not hold. The service declares `user_id: str`
and receives the whole `User` object. `get_documents` is called and
`DocumentService` declares no such method. `get_document` declares
`(document_id, user_id)` and is called with one argument at three sites.
The bodies then read `.user_id` off a `Document`, whose schema declares
`owner_id`.

See ./README.md for the route table and the shared path collision.
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
    """Create a document owned by the authenticated caller.

    Answers 200 on success, because the decorator sets no `status_code`.
    The `current_user` object is passed where the service declares
    `user_id: str`, so the stored owner value is a `User` rather than an
    identifier.

    Args:
        document: Validated request body, declared `DocumentCreate`.
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        The created `Document`, as the return annotation declares.

    Raises:
        HTTPException: 400, raised by the service when the title or the
            content is empty.
    """
    document_service = DocumentService()
    created_document = await document_service.create_document(document, current_user)
    return created_document

@router.get('/')
async def get_documents(current_user: User = Depends(get_current_user)) -> List[Document]:
    """List the documents belonging to the authenticated caller.

    Args:
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        A `List[Document]`, as the return annotation declares.

    Raises:
        AttributeError: `DocumentService` declares no `get_documents`, so
            the call below fails on every request.
    """
    document_service = DocumentService()
    documents = await document_service.get_documents(current_user)
    return documents

@router.get('/{document_id}')
async def get_document(document_id: str, current_user: User = Depends(get_current_user)) -> Document:
    """Return one document when the caller owns it.

    Ownership is compared here rather than in the service, because the call
    below omits the `user_id` argument the service declares. The comparison
    reads `document.user_id`, and `Document` declares `owner_id`.

    Args:
        document_id: Firestore document identifier from the path.
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        The matching `Document`, as the return annotation declares.

    Raises:
        HTTPException: 404 from the service when no record exists, 403 here
            when the stored owner does not match the caller.
        TypeError: The service declares `(document_id, user_id)` and is
            called with one argument.
    """
    document_service = DocumentService()
    document = await document_service.get_document(document_id)
    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this document")
    return document

@router.put('/{document_id}')
async def update_document(document_id: str, document: DocumentUpdate, current_user: User = Depends(get_current_user)) -> Document:
    """Apply a partial update to a document the caller owns.

    Reads the document first to compare ownership, then updates, so a
    successful request performs the read twice: once here and once inside
    the service.

    Args:
        document_id: Firestore document identifier from the path.
        document: Validated request body, declared `DocumentUpdate`.
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        The updated `Document`, as the return annotation declares.

    Raises:
        HTTPException: 404 from the service when no record exists, 403 here
            when the stored owner does not match the caller.
        TypeError: Both service calls omit an argument the service
            declares.
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

    Args:
        document_id: Firestore document identifier from the path.
        current_user: The authenticated `User`, resolved by
            `get_current_user`.

    Returns:
        A dict carrying the literal message `"Document deleted
        successfully"`, whatever the delete did.

    Raises:
        HTTPException: 404 from the service when no record exists, 403 here
            when the stored owner does not match the caller.
        TypeError: Both service calls omit an argument the service
            declares.
    """
    document_service = DocumentService()
    existing_document = await document_service.get_document(document_id)
    if existing_document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this document")
    await document_service.delete_document(document_id)
    return {"message": "Document deleted successfully"}