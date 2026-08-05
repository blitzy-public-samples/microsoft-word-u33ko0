"""Build the router for the create, read, update and delete (CRUD) document routes.

Five handlers serve `POST /`, `GET /`, `GET /{document_id}`,
`PUT /{document_id}` and `DELETE /{document_id}` of the application programming
interface (API). L8 exports `router`. Every handler declares
`current_user: User = Depends(get_current_user)`, so all five routes require a
bearer token.

Export name mismatch: `app/main.py:L4` imports `documents_router` from this
module. L8 defines `router`, and no `documents_router` name exists here.

Route collision: `app/main.py:L50` mounts this router with no prefix and
`app/main.py:L52` mounts the template router the same way. The five routes in
`app/api/templates.py` carry identical path shapes, because `/{document_id}`
and `/{template_id}` match the same requests. Starlette matches in
registration order, so these five handlers take every one of those requests
and the five template routes never run.

The module cannot import. L4 requests `app.services.document_service`, whose
own chain reaches `settings` in `app.core.config` through
`app/db/firestore.py:L3`, and `app.core.config` defines only the `Settings`
class and a `get_settings()` factory. L4 therefore raises `ImportError` first.
L5 requests `app.api.auth` for the `get_current_user` defined at
`app/api/auth.py:L14`, and `app/api/auth.py:L6` requests that same absent
`settings`. `app/core/security.py:L32` defines a second `get_current_user`,
which this module does not import.

Four call sites disagree with the service contract in
`app/services/document_service.py`, whose locators follow in parentheses:

- L13 passes the whole `current_user` object where `user_id: str` is
  declared (L11).
- L19 calls `get_documents`, and `DocumentService` defines no such method.
- L25, L33 and L42 pass one argument where two are declared (L26). L36 passes
  two where three are declared (L43), and L45 passes one where two are
  declared (L63).
- L26, L34 and L43 read `user_id` from a `Document`, and that contract
  declares `owner_id` at `app/schema/document.py:L8`.

Line references point at the pre-documentation layout of commit `06be74c`, so
they exclude docstrings added by this pass.
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

    L13 passes the whole `current_user` object where
    `app/services/document_service.py:L11` declares `user_id: str`. The service
    stores that object under the `user_id` key at
    `app/services/document_service.py:L19`.

    Intended behavior per documentation/Technical Specifications.md, SYSTEM
    DESIGN > API DESIGN (L437-L445): the example handler passes
    `current_user.id` to the service.

    Args:
        document: The request body, declared `DocumentCreate`, carrying `title`,
            `content` and an optional `owner_id`.
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `Document` named in the return annotation, returned at L14.

    Side effects:
        Writes one new document to the Firestore `documents` collection. The
        decorator at L10 sets no `status_code`, so a success returns hypertext
        transfer protocol (HTTP) status 200.
    """
    document_service = DocumentService()
    created_document = await document_service.create_document(document, current_user)
    return created_document

@router.get('/')
async def get_documents(current_user: User = Depends(get_current_user)) -> List[Document]:
    """List the documents belonging to the authenticated caller.

    L19 awaits `document_service.get_documents(current_user)`, and
    `DocumentService` defines no `get_documents` method. That class declares
    `create_document`, `get_document`, `update_document` and `delete_document`
    at `app/services/document_service.py:L11`, `:L26`, `:L43` and `:L63`. The
    declared `List[Document]` cannot be produced.

    Args:
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `List[Document]` named in the return annotation, returned at L20.
    """
    document_service = DocumentService()
    documents = await document_service.get_documents(current_user)
    return documents

@router.get('/{document_id}')
async def get_document(document_id: str, current_user: User = Depends(get_current_user)) -> Document:
    """Retrieve one document when the caller owns it.

    Two call sites disagree with their contracts. L25 passes one argument where
    `app/services/document_service.py:L26` declares two, `document_id` and
    `user_id`. L26 reads `user_id` from a `Document`, and that contract declares
    `owner_id` at `app/schema/document.py:L8`. `owner_id` is optional and
    defaults to `None`, so a `Document` validates without the value the
    ownership check reads.

    Args:
        document_id: Path parameter, declared `str`, naming the document to
            read.
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `Document` named in the return annotation, returned at L28.

    Raises:
        HTTPException: HTTP 403 at L27, when the ownership comparison at L26
            finds a mismatch.
    """
    document_service = DocumentService()
    document = await document_service.get_document(document_id)
    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this document")
    return document

@router.put('/{document_id}')
async def update_document(document_id: str, document: DocumentUpdate, current_user: User = Depends(get_current_user)) -> Document:
    """Apply an update to a document the caller owns.

    Three call sites disagree with their contracts. L33 passes one argument
    where `app/services/document_service.py:L26` declares two. L34 reads
    `user_id` from a `Document`, and that contract declares `owner_id` at
    `app/schema/document.py:L8`. L36 passes two arguments where
    `app/services/document_service.py:L43` declares three, `document_id`,
    `document` and `user_id`.

    Args:
        document_id: Path parameter, declared `str`, naming the document to
            update.
        document: The request body, declared `DocumentUpdate`, carrying the
            optional `title` and `content` fields to change.
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `Document` named in the return annotation, returned at L37.

    Raises:
        HTTPException: HTTP 403 at L35, when the ownership comparison at L34
            finds a mismatch.

    Side effects:
        Writes the changed fields to the Firestore `documents` collection. The
        decorator at L30 sets no `status_code`, so a success returns HTTP 200.
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

    Three call sites disagree with their contracts. L42 passes one argument
    where `app/services/document_service.py:L26` declares two. L43 reads
    `user_id` from a `Document`, and that contract declares `owner_id` at
    `app/schema/document.py:L8`. L45 passes one argument where
    `app/services/document_service.py:L63` declares two.

    Args:
        document_id: Path parameter, declared `str`, naming the document to
            delete.
        current_user: The caller, declared `User`. FastAPI injects it through
            `Depends(get_current_user)`.

    Returns:
        The `dict` named in the return annotation. L46 returns the literal
        `{"message": "Document deleted successfully"}`, so the body reports
        nothing about what the service did.

    Raises:
        HTTPException: HTTP 403 at L44, when the ownership comparison at L43
            finds a mismatch.

    Side effects:
        Removes the document from the Firestore `documents` collection. The
        decorator at L39 sets no `status_code`, so a success returns HTTP 200.
    """
    document_service = DocumentService()
    existing_document = await document_service.get_document(document_id)
    if existing_document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this document")
    await document_service.delete_document(document_id)
    return {"message": "Document deleted successfully"}