from fastapi import HTTPException
from google.cloud.firestore import Client
from app.schema.document import Document, DocumentCreate, DocumentUpdate
from app.db.firestore import db
from app.core.config import settings

class DocumentService:
    def __init__(self):
        self.db = db

    async def create_document(self, document: DocumentCreate, user_id: str) -> Document:
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