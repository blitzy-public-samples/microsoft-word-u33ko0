"""Build the shared Firestore client and four collection-level helpers.

Import of this module has side effects. Application Default Credentials are
resolved and the client is constructed at import time, so a missing
credential fails here rather than at first query. `settings` is imported
from `app.core.config`, which never creates it, so neither statement runs as
committed.

The four helpers are synchronous and no service calls any of them: the
services reach Firestore through `self.db.collection(...)` directly. Three
modules import this file and all three import only `db`.
See ./README.md for that comparison.
"""
from google.cloud.firestore import Client
from google.auth import default
from app.core.config import settings

# Initialize Firestore client
credentials, project = default()
db = Client(project=settings.GOOGLE_CLOUD_PROJECT)

def get_document(collection: str, document_id: str) -> dict:
    """Read one document from a collection and return its fields.

    Args:
        collection: Firestore collection name.
        document_id: Identifier of the document to read.

    Returns:
        The document fields as a dict, or `None` when no document exists.
        The declared return type is `dict`, and the absent case returns
        `None`, so the annotation does not cover both paths.

    Example:
        >>> fields = get_document('documents', 'abc123')
        >>> if fields is None:
        ...     ...  # no such document
    """
    doc_ref = db.collection(collection).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def create_document(collection: str, data: dict) -> str:
    """Add a document to a collection and return its generated identifier.

    Firestore generates the identifier, so the caller cannot choose it.

    Args:
        collection: Firestore collection name.
        data: Field values to store.

    Returns:
        The new document identifier, taken from the reference that `add()`
        returns as the second element of its tuple.

    Example:
        >>> doc_id = create_document('documents', {'title': 'Notes'})
    """
    doc_ref = db.collection(collection).add(data)
    return doc_ref[1].id

def update_document(collection: str, document_id: str, data: dict) -> None:
    """Merge field values into an existing document.

    Args:
        collection: Firestore collection name.
        document_id: Identifier of the document to change.
        data: Field values to merge.

    Returns:
        None. The write reaches Firestore directly.

    Raises:
        NotFound: When the target document does not exist.
    """
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.update(data)

def delete_document(collection: str, document_id: str) -> None:
    """Delete one document from a collection.

    Args:
        collection: Firestore collection name.
        document_id: Identifier of the document to delete.

    Returns:
        None. Firestore treats deleting an absent document as success, so
        the call reports nothing about whether one existed.
    """
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.delete()