"""Create, read, update and delete documents in one Firestore collection.

The service compares a caller identifier before reading, updating, or deleting
an existing document. create_document writes the supplied user identifier
without an ownership comparison.

The imported settings singleton is unresolved.
The service authenticates no identity. Each method trusts the supplied user_id
as the requester and stores or compares it directly.
"""
from fastapi import HTTPException
from google.cloud.firestore import Client
from app.schema.document import Document, DocumentCreate, DocumentUpdate
from app.db.firestore import db
from app.core.config import settings

class DocumentService:
    """Store and retrieve user-owned documents in one Firestore collection.

    Every method is declared `async def`, and every Firestore call inside is
    synchronous and blocking. Each call holds the event loop for a full network
    round trip, so declaring the methods as coroutines adds no concurrency.

    The Document contract in app.schema.document requires `created_at` and
    `updated_at`, and no method here writes either field. Every method that
    builds a Document from a stored record therefore raises
    `pydantic.ValidationError` rather than returning the document.

    Public methods:
        create_document: Write a new document to Firestore.
        get_document: Return one document after an ownership check.
        update_document: Apply a partial change and re-read the document.
        delete_document: Remove a document after an ownership check.

    Attributes:
        db: The shared Firestore client imported from `app.db.firestore`.
    """

    def __init__(self):
        """Bind the shared Firestore client to the instance.

        The constructor reuses the module-level client built by
        `app.db.firestore` and opens no connection of its own.
        """
        self.db = db

    async def create_document(self, document: DocumentCreate, user_id: str) -> Document:
        """Write a new document to Firestore and return it.

        Args:
            document: A DocumentCreate carrying the title and content to store.
            user_id: Identifier stored on the new document as its owner.

        Returns:
            A Document built from the written dictionary.

        Raises:
            HTTPException: 400 if either the title or the content is empty.
            pydantic.ValidationError: On the return construction, for every
                request that passes the emptiness check. The Document contract
                requires `created_at` and `updated_at`, and this write stores
                neither, so no caller receives a document.

        Side effects:
            Writes one document to the `documents` collection. The write stores
            the owner under the key `user_id`, while the Document contract
            declares `owner_id`. The write also persists the `owner_id` key
            that `document.dict()` supplies, and DocumentCreate defaults that
            field to `None`, so the stored `owner_id` is always null. The write
            stores no `created_at` and no `updated_at`.
        """
        # Validate input data
        if not document.title or not document.content:
            raise HTTPException(status_code=400, detail="Title and content are required")

        # Create new document in Firestore
        doc_ref = self.db.collection('documents').document()
        doc_data = document.dict()
        doc_data['user_id'] = user_id
        doc_data['id'] = doc_ref.id
        doc_ref.set(doc_data)

        # Return created document
        return Document(**doc_data)

    async def get_document(self, document_id: str, user_id: str) -> Document:
        """Retrieve a single document if the caller owns it.

        Args:
            document_id: Firestore document identifier.
            user_id: Identifier of the requesting user, compared against
                the stored owner for the 403 ownership check.

        Returns:
            The matching Document.

        Raises:
            HTTPException: 404 if not found, 403 if user_id does not match
                the stored owner.
            KeyError: If the stored record follows the Document contract and
                has owner_id but no user_id key.
            pydantic.ValidationError: If the stored record carries no
                `created_at` and no `updated_at`, which is every record
                `create_document` writes. The Document contract requires both.

        The 404 check runs before the 403 check, so callers can distinguish a
        missing identifier from another user's existing document.
        """
        # Retrieve document from Firestore
        doc_ref = self.db.collection('documents').document(document_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="Document not found")

        # Check user permissions
        if doc.to_dict()['user_id'] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this document")

        # Return document if authorized
        return Document(**doc.to_dict())

    # HUMAN ASSISTANCE NEEDED
    # This function might need additional error handling and validation
    async def update_document(self, document_id: str, document: DocumentUpdate, user_id: str) -> Document:
        """Apply a partial change to a document the caller owns and return it.

        See the assistance marker in the comment block directly above this
        signature: the method validates nothing beyond the ownership check.

        Args:
            document_id: Firestore document identifier.
            document: A DocumentUpdate holding the fields to change. Only the
                fields the caller set are sent to Firestore.
            user_id: Identifier of the requesting user, compared against the
                stored owner for the 403 ownership check.

        Returns:
            The Document as re-read after the write.

        Raises:
            HTTPException: 404 if not found, 403 if user_id does not match the
                stored owner.
            KeyError: If the stored record has no user_id key.
            pydantic.ValidationError: On the re-read construction, whenever the
                stored record carries no `created_at` and no `updated_at`. The
                write sends only the fields the caller set, so a record that
                reached Firestore without timestamps keeps none.

        Side effects:
            Missing and unauthorized paths stop after the first read. A
            successful authorized update performs read, write, and read. The
            write never maintains `updated_at`, so the stored modification
            timestamp that the Document contract requires stays absent.

        The ownership check and write use no transaction or precondition. A
        concurrent ownership change can therefore make the decision stale.
        """
        # Retrieve existing document
        doc_ref = self.db.collection('documents').document(document_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="Document not found")

        # Check user permissions
        if doc.to_dict()['user_id'] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this document")

        # Update document in Firestore
        update_data = document.dict(exclude_unset=True)
        doc_ref.update(update_data)

        # Return updated document
        updated_doc = doc_ref.get()
        return Document(**updated_doc.to_dict())

    async def delete_document(self, document_id: str, user_id: str) -> bool:
        """Delete a document the caller owns.

        Args:
            document_id: Firestore document identifier.
            user_id: Identifier of the requesting user, compared against the
                stored owner for the 403 ownership check.

        Returns:
            `True` after the delete call returns without raising. The method
            ignores the client result and has no branch returning `False`.

        Raises:
            HTTPException: 404 if not found, 403 if user_id does not match the
                stored owner.
            KeyError: If the stored record has no user_id key.
            Exception: A client delete failure propagates and prevents the
                `True` return.

        Side effects:
            Deletes one document after an ownership read. The check and delete
            are non-transactional, so a concurrent ownership change can make
            the decision stale.
        """
        # Retrieve document
        doc_ref = self.db.collection('documents').document(document_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="Document not found")

        # Check user permissions
        if doc.to_dict()['user_id'] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this document")

        # Delete document from Firestore
        doc_ref.delete()

        # Return deletion status
        return True