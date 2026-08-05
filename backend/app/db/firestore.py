"""Expose synchronous Firestore document helpers.

The imported settings singleton is unresolved.
If that import is repaired, module import performs Application Default
Credentials discovery even though neither returned binding is passed to the
Firestore client. All four helpers are synchronous, and no service consumes
them.
"""
from google.cloud.firestore import Client
from google.auth import default
from app.core.config import settings

# Initialize Firestore client
credentials, project = default()
db = Client(project=settings.GOOGLE_CLOUD_PROJECT)

def get_document(collection: str, document_id: str) -> dict:
    """Retrieve one document's stored fields from a named collection.

    Args:
        collection: Name of the Firestore collection holding the document.
        document_id: Identifier of the document to read.

    Returns:
        The stored fields as a dictionary when the snapshot exists, and None
        when it does not. The None result contradicts the declared `dict`
        return type, so callers must guard before subscripting.

    Example:
        fields = get_document("documents", "abc123")
        if fields is not None:
            title = fields["title"]

        The example cannot run as committed, because the unresolved settings
        import fails first.
    """
    doc_ref = db.collection(collection).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def create_document(collection: str, data: dict) -> str:
    """Add a document to a named collection and return its new identifier.

    Firestore's `add` returns a two-element tuple of write timestamp and new
    document reference, so the identifier comes from element one.

    Args:
        collection: Name of the Firestore collection to write to.
        data: Field names and values to store on the new document.

    Returns:
        The server-generated document identifier, declared `str`.

    Example:
        new_id = create_document("documents", {"title": "Draft"})

        The example cannot run as committed, because the unresolved settings
        import fails first.
    """
    doc_ref = db.collection(collection).add(data)
    return doc_ref[1].id

def update_document(collection: str, document_id: str, data: dict) -> None:
    """Merge the supplied fields into an existing document.

    Firestore rewrites only the keys present in `data` and leaves every other
    stored field unchanged.

    Args:
        collection: Name of the Firestore collection holding the document.
        document_id: Identifier of the document to modify.
        data: Field names and values to merge into the stored document.

    Returns:
        Nothing, declared `None`.
    """
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.update(data)

def delete_document(collection: str, document_id: str) -> None:
    """Delete a document from a named collection.

    The call addresses one Firestore document. The helper does not verify
    removal from subcollections, backups, exports, versions, or related
    records.

    Args:
        collection: Name of the Firestore collection holding the document.
        document_id: Identifier of the document to remove.

    Returns:
        Nothing, declared `None`.
    """
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.delete()