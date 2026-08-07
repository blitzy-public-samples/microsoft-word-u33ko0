"""Build the router for the create, read, update and delete document routes.

Five handlers serve `POST /`, `GET /`, `GET /{document_id}`, `PUT /{document_id}` and
`DELETE /{document_id}`. Every handler depends on `get_current_user`, so all five need a
bearer token. The module exports `router`.

`app/main.py` imports the name `documents_router` from this module, and this module
defines `router`. The template router registers the same five path shapes with no
prefix either. Starlette matches in registration order, so these handlers take every
request and the template routes never run.

The module cannot import. L47 requests `app.services.document_service`, whose
own chain reaches `settings` in `app.core.config` through
`app/db/firestore.py:L36`, and `app.core.config` defines only the `Settings`
class and a `get_settings()` factory. L47 therefore raises `ImportError` first.
L48 requests `app.api.auth` for the `get_current_user` defined at
`app/api/auth.py:L89`, and `app/api/auth.py:L81` requests that same absent
`settings`. `app/core/security.py:L117` defines a second `get_current_user`,
which this module does not import.

Ten sites disagree with the service contract in
`app/services/document_service.py`: seven service calls and three field reads,
grouped below into four categories, each naming the declaration it disagrees with.

- L108 passes the whole `current_user` object where `user_id: str` is
  declared (`app/services/document_service.py:L72`).
- L142 calls `get_documents`, and `DocumentService` defines no such method.
- L183, L231 and L278 pass one argument where two are declared
  (`app/services/document_service.py:L123`). L234 passes two where three are
  declared (`app/services/document_service.py:L183`). L281 passes one where two
  are declared (`app/services/document_service.py:L252`).
- L184, L232 and L279 read `user_id` from a `Document`, and that contract
  declares `owner_id` at `app/schema/document.py:L66`.
- The arity mismatches above raise `TypeError`, not `HTTPException`. FastAPI
  leaves an uncaught `TypeError` to the server error handler, so a caller
  receives HTTP 500 rather than a document, a 403 or a 404.

Each handler docstring below closes with a paragraph labelled "Internal notes",
carrying locators, storage details and contract-failure analysis.

Every `Lnn` reference below points at the current layout of the file it names. A
bare `Lnn` points into this file, and a `path:Lnn` points into the named file.
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

    The route requires a bearer token and attempts to store one new document
    owned by the caller. A success returns hypertext transfer protocol (HTTP)
    status 200, because the decorator sets no `status_code`.

    Args:
        document: Request body declared `DocumentCreate`, carrying `title`, `content`
            and an optional `owner_id`.
        current_user: The caller, injected through `Depends(get_current_user)`.

    Returns:
        The `Document` named in the return annotation.

    Raises:
        TypeError: Raised inside the service, from the Firestore encoder, for the
            reason the internal notes below record. The handler wraps L108 in no
            `try` block, so FastAPI converts the uncaught error into a 500
            response.

    Internal notes.

    The decorator sits at L53 and L109 returns the service result.

    Side effects:
        None can be established from this route. Writing one document to the
        Firestore `documents` collection is the intended effect, and the write
        does not reach the service's `set` remote procedure call. L108 passes the
        whole `current_user` object where
        `app/services/document_service.py:L72` declares `user_id: str`.
        `app/services/document_service.py:L116` places that Pydantic model under
        the `user_id` key of the dictionary, and `:L118` hands the dictionary to
        `DocumentReference.set`. The Firestore encoder accepts `None`, `bool`,
        `int`, `float`, `str`, `bytes`, `datetime`, `GeoPoint`,
        `DocumentReference`, `list` and `dict`, and rejects an arbitrary
        `BaseModel`, raising
        `TypeError('Cannot convert to a Firestore Value', ..., 'Invalid type', ...)`
        while it serializes the request. The encoding runs client-side, before any
        network call, so no document is created and no partial write is left
        behind.

    The failure belongs to this caller rather than to the service.
    `DocumentService.create_document` declares `user_id: str`, and a caller that
    passes `current_user.id` supplies an encodable value and reaches the write.
    `app/services/document_service.py` documents that correctly typed path,
    including the separate Pydantic validation error its return construction
    raises after the write commits.

    Intended behavior per documentation/Technical Specifications.md, SYSTEM
    DESIGN > API DESIGN (L437-L445): the example handler passes
    `current_user.id` to the service.
    """
    document_service = DocumentService()
    created_document = await document_service.create_document(document, current_user)
    return created_document

@router.get('/')
async def get_documents(current_user: User = Depends(get_current_user)) -> List[Document]:
    """List the documents belonging to the authenticated caller.

    Args:
        current_user: The caller, injected through `Depends(get_current_user)`.

    Returns:
        The `List[Document]` named in the return annotation.

    Raises:
        AttributeError: At L142, because `DocumentService` defines no
            `get_documents` method. The attribute lookup fails before any argument
            is passed, so the failure is certain on every request rather than
            conditional. The handler wraps L142 in no `try` block, so FastAPI
            converts the uncaught error into a 500 response and the declared
            `List[Document]` is never produced.

    Internal notes.

    L142 awaits `document_service.get_documents(current_user)`, and
    `DocumentService` defines no `get_documents` method. That class declares
    `create_document`, `get_document`, `update_document` and `delete_document`
    at `app/services/document_service.py:L72`, `:L123`, `:L183` and `:L252`. The
    declared `List[Document]` cannot be produced, and L143 never runs.

    Side effects:
        None. The failure at L142 precedes every Firestore call, so the route
        reads nothing and writes nothing.
    """
    document_service = DocumentService()
    documents = await document_service.get_documents(current_user)
    return documents

@router.get('/{document_id}')
async def get_document(document_id: str, current_user: User = Depends(get_current_user)) -> Document:
    """Return one document after checking that the caller owns it.

    Args:
        document_id: Path parameter naming the document to read.
        current_user: The caller, injected through `Depends(get_current_user)`.

    Returns:
        The `Document` named in the return annotation.

    Raises:
        TypeError: At L183, because the call passes one argument where
            `app/services/document_service.py:L123` declares `document_id` and
            `user_id` after `self`. Python raises before the method body runs, so
            the failure is certain on every request. The handler wraps L183 in no
            `try` block, so FastAPI converts the uncaught error into a 500
            response, and the 403 below is unreachable as committed.
        HTTPException: HTTP 403, detail
            `"Not authorized to access this document"`, when the caller does not
            own the document. Reachable only once the arity at L183 is corrected.

    Internal notes.

    The decorator sits at L145, the 403 at L185, and L186 returns the document.

    Side effects:
        None. The failure at L183 precedes the service's Firestore read, so the
        route reads nothing and writes nothing.

    Two call sites disagree with their contracts. L183 passes one argument where
    `app/services/document_service.py:L123` declares two, `document_id` and
    `user_id`. L184 reads `user_id` from a `Document`, and that contract declares
    `owner_id` at `app/schema/document.py:L66`. `owner_id` is optional and
    defaults to `None`, so a `Document` validates without the value the
    ownership check reads.
    """
    document_service = DocumentService()
    document = await document_service.get_document(document_id)
    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this document")
    return document

@router.put('/{document_id}')
async def update_document(document_id: str, document: DocumentUpdate, current_user: User = Depends(get_current_user)) -> Document:
    """Update one document after checking that the caller owns it.

    Args:
        document_id: Path parameter naming the document to update.
        document: Request body declared `DocumentUpdate`, carrying optional `title` and
            `content`.
        current_user: The caller, injected through `Depends(get_current_user)`.

    Returns:
        The updated `Document` named in the return annotation.

    Raises:
        TypeError: At L231, because the call passes one argument where
            `app/services/document_service.py:L123` declares `document_id` and
            `user_id` after `self`. Python raises before the method body runs, so
            the failure is certain on every request.
        TypeError: At L234, for the same class of mistake, because the call passes
            two arguments where `app/services/document_service.py:L183` declares
            `document_id`, `document` and `user_id` after `self`. L234 is
            unreachable while L231 raises first.
        HTTPException: HTTP 403, detail
            `"Not authorized to update this document"`, when the caller does not
            own the document. Reachable only once the arity at L231 is corrected.

        The handler wraps neither call in a `try` block, so FastAPI converts the
        uncaught `TypeError` into a 500 response and the caller sees a server
        error rather than a document.

    Internal notes.

    Side effects:
        None. The `TypeError` at L231 precedes the service's Firestore read, so the
        route reads nothing and writes nothing.

    Once the arity at L231 and L234 is corrected, the route performs one write to
    the Firestore `documents` collection, preceded by two reads: this handler's
    ownership read plus the service's own read-before-write. The ownership
    comparison at L232 reads `document.user_id` against a contract declaring
    `owner_id` at `app/schema/document.py:L66`.
    """
    document_service = DocumentService()
    existing_document = await document_service.get_document(document_id)
    if existing_document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this document")
    updated_document = await document_service.update_document(document_id, document)
    return updated_document

@router.delete('/{document_id}')
async def delete_document(document_id: str, current_user: User = Depends(get_current_user)) -> dict:
    """Delete one document after checking that the caller owns it.

    Args:
        document_id: Path parameter naming the document to delete.
        current_user: The caller, injected through `Depends(get_current_user)`.

    Returns:
        A dictionary carrying a `message` confirmation, per the `dict` annotation. The
        route answers HTTP 200 rather than 204.

    Raises:
        TypeError: At L278, because the call passes one argument where
            `app/services/document_service.py:L123` declares `document_id` and
            `user_id` after `self`. Python raises before the method body runs, so
            the failure is certain on every request.
        TypeError: At L281, for the same class of mistake, because the call passes
            one argument where `app/services/document_service.py:L252` declares
            `document_id` and `user_id` after `self`. L281 is unreachable while L278
            raises first.
        HTTPException: HTTP 403, detail
            `"Not authorized to delete this document"`, when the caller does not
            own the document. Reachable only once the arity at L278 is corrected.

        The handler wraps neither call in a `try` block, so FastAPI converts the
        uncaught `TypeError` into a 500 response and the caller sees a server
        error rather than the success message.

    Internal notes.

    Side effects:
        None. The `TypeError` at L278 precedes the service's Firestore read, so the
        route reads nothing and deletes nothing.

    Once the arity at L278 and L281 is corrected, the route performs one hard delete
    from the Firestore `documents` collection, with no soft-delete flag and no
    version retained. The ownership comparison at L279 reads `document.user_id`
    against a contract declaring `owner_id` at `app/schema/document.py:L66`.
    """
    document_service = DocumentService()
    existing_document = await document_service.get_document(document_id)
    if existing_document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this document")
    await document_service.delete_document(document_id)
    return {"message": "Document deleted successfully"}