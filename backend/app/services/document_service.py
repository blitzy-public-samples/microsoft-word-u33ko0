"""Hold the document service: create, read, update and delete against Firestore.

The class is the only service a router constructs. Every one of its methods
is declared `async` while the Firestore calls inside are synchronous and
blocking, so awaiting one of them yields no concurrency.

`settings` is imported from `app.core.config`, which never creates it, and
`Client` is imported and never used. `app/api/documents.py` calls a
`get_documents` method this class does not declare, and calls `get_document`,
`update_document` and `delete_document` with one argument fewer than each
declares. See ./README.md for the call table.
"""
from fastapi import HTTPException
from google.cloud.firestore import Client
from app.schema.document import Document, DocumentCreate, DocumentUpdate
from app.db.firestore import db
from app.core.config import settings

class DocumentService:
    """Read and write document records in the `documents` collection.

    `get_document`, `update_document` and `delete_document` compare the
    stored `user_id` against the caller, and those three are the only
    object-level authorization here. `create_document` compares nothing.
    The class declares no `get_documents`, and `app/api/documents.py` calls one.

    Public methods:
        create_document: Store a new document and return it.
        get_document: Return one document the caller owns.
        update_document: Apply a partial change and return the result.
        delete_document: Remove a document the caller owns.
    """
    def __init__(self):
        """Bind the shared Firestore client to the instance.

        The client comes from `app.db.firestore`, which builds it at import
        time. The constructor takes no arguments, so a test cannot pass a
        substitute client.
        """
        self.db = db

    async def create_document(self, document: DocumentCreate, user_id: str) -> Document:
        """Store a new document owned by the given user.

        The record is assembled from the request body, then a `user_id` key
        and the Firestore-generated `id` are added. Given the declared `str`,
        the record would carry `user_id` while `Document` declares `owner_id`.
        The router passes a `User`, which Firestore cannot encode, so the
        write raises before it is sent and nothing is stored. Neither
        `created_at` nor `updated_at` is written, and both are required.

        Args:
            document: The validated request body, declared `DocumentCreate`.
            user_id: Identifier of the owning user. The router passes the
                whole `User` object instead.

        Returns:
            The stored `Document`.

        Raises:
            HTTPException: 400 when the title or the content is empty.
            TypeError: From Firestore encoding when `user_id` holds a `User`.
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

        The ownership test reads the `user_id` key out of the stored record
        rather than off the `Document` model, because the model declares
        `owner_id` and the record carries `user_id`. A record written
        without that key raises `KeyError` before the comparison, which
        answers 500 rather than 403. Every caller in
        `app/api/documents.py` omits the second argument.

        Args:
            document_id: Firestore document identifier.
            user_id: Identifier of the requesting user, compared against
                the stored owner for the 403 ownership check.

        Returns:
            The matching Document.

        Raises:
            HTTPException: 404 if not found, 403 if user_id does not match
                the stored owner.
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
        """Apply a partial change to a document the caller owns.

        The method reads the record, writes the merged fields, then reads it
        again to build the return value, so one update costs three Firestore
        operations. `exclude_unset=True` means an omitted field is left
        alone rather than cleared, and a request that sets no field issues
        an empty update. `updated_at` is not written, so the record still
        cannot satisfy the `Document` contract. See the HUMAN ASSISTANCE
        NEEDED marker above.

        Args:
            document_id: Firestore document identifier.
            document: The validated change set, declared `DocumentUpdate`.
            user_id: Identifier of the requesting user, compared against
                the stored owner.

        Returns:
            The re-read `Document`.

        Raises:
            HTTPException: 404 when no record exists, 403 when the stored
                owner does not match.
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
            user_id: Identifier of the requesting user, compared against
                the stored owner.

        Returns:
            The literal `True`. Firestore reports nothing about the delete,
            so the value states that the code reached the end rather than
            that a record was removed.

        Raises:
            HTTPException: 404 when no record exists, 403 when the stored
                owner does not match.
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