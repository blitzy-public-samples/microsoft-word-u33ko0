from google.cloud.firestore import Client
from google.auth import default
from app.core.config import settings

# Initialize Firestore client
credentials, project = default()
db = Client(project=settings.GOOGLE_CLOUD_PROJECT)

def get_document(collection: str, document_id: str) -> dict:
    doc_ref = db.collection(collection).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def create_document(collection: str, data: dict) -> str:
    doc_ref = db.collection(collection).add(data)
    return doc_ref[1].id

def update_document(collection: str, document_id: str, data: dict) -> None:
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.update(data)

def delete_document(collection: str, document_id: str) -> None:
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.delete()