"""Build the shared Firestore client and expose four document helpers.

One client is constructed at module scope, so every importer shares a single instance.
The four helpers run synchronously and cover create, read, update and delete work
against a collection the caller names on each call.

`settings` is requested from `app.core.config`, which defines only the `Settings` class
and a `get_settings` factory, so importing this module raises `ImportError` before the
credential call runs. Importing it also runs Application Default Credentials discovery,
which fails without resolvable Google credentials, and binds `credentials` and `project`
that no line in the repository reads.

No module imports the four helpers. Three modules import the `db` client and call it
directly instead: `app/main.py`, `app/services/document_service.py` and
`app/tasks/background_tasks.py`.

`app/main.py:L22` calls `db.is_connected()`, and a Firestore `Client` defines no
such method, so that call raises `AttributeError`.

`app/main.py:L34` awaits `db.close()`, and the outcome differs. The client does
carry `close`, inherited from the shared Google Cloud client base class, and that
method is synchronous: it shuts the underlying transport session and returns
`None`. The `await` then receives `None`, which is not awaitable, so the statement
performs the close and afterwards raises `TypeError`. No backend dependency
manifest is committed, so nothing pins `google-cloud-firestore` and the inherited
surface is whatever the resolved release provides.

None of the four helpers opens a transaction, sets a retry policy, sets a
timeout, or catches an exception.

Line locators: every `Lnn` reference below numbers the tree at commit
06be74c7c88aa6bca652d465eaa00ad480a9e5c5, the frozen revision that precedes this
documentation pass. A bare `Lnn` points into this file, and a `path:Lnn` points into
the named file. Current HEAD numbers each documented file higher.
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
        The stored fields as a dictionary when the snapshot exists, and `None` when it
        does not. The `None` branch contradicts the `-> dict` annotation, so a caller
        that trusts the annotation and subscripts the result raises `TypeError` for a
        missing document.

    Example:
        fields = get_document("documents", "abc123")
        if fields is not None:
            title = fields["title"]

        The guard is required, because `L14` returns None for a missing
        snapshot. The example cannot run as committed, because `L3` imports a
        `settings` name that `app/core/config.py` never defines.
    """
    doc_ref = db.collection(collection).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def create_document(collection: str, data: dict) -> str:
    """Add a document to a named collection and return its generated identifier.

    Args:
        collection: Name of the Firestore collection to add to.
        data: Field values to store. Written as given, with no validation against any
            Pydantic model.

    Returns:
        The new document's identifier, taken from the second element of the tuple
        `add()` returns.

    Example:
        document_id = create_document("documents", {"title": "Draft"})

    Note:
        Side effect is one write to the named collection. Firestore generates the
        identifier, so the caller cannot supply one through this helper.
    """
    doc_ref = db.collection(collection).add(data)
    return doc_ref[1].id

def update_document(collection: str, document_id: str, data: dict) -> None:
    """Merge field values into an existing document.

    Args:
        collection: Name of the Firestore collection holding the document.
        document_id: Identifier of the document to update.
        data: Field values to merge. Keys absent from the dictionary are left as stored.

    Returns:
        Nothing.

    Note:
        Side effect is one write. `update()` requires an existing document and raises
        `NotFound` otherwise, and this helper does not catch that.
    """
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.update(data)

def delete_document(collection: str, document_id: str) -> None:
    """Delete one document from a named collection.

    Args:
        collection: Name of the Firestore collection holding the document.
        document_id: Identifier of the document to delete.

    Returns:
        Nothing.

    Note:
        Side effect is one hard delete, with no version retained. Deleting an absent
        document succeeds silently, so the caller learns nothing about what existed.
    """
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.delete()