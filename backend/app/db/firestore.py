"""Build the shared Firestore client and expose four document helpers.

`L7` constructs one Google Cloud Firestore client at module scope, so every
importer shares a single instance. The four helpers below run synchronously
and cover create, read, update and delete (CRUD) work against a collection
that the caller names on each call.

`L3` imports `settings` from `app.core.config`, and that module defines only
the `Settings` class and the `get_settings` factory. No module-level
`settings` exists there, so importing this module raises ImportError at `L3`
before the credential call at `L6` runs.

`L6` runs Application Default Credentials (ADC) discovery through the
`default` function imported at `L2`. Nothing reads either name that `L6`
binds. `L7` takes the project identifier from `settings.GOOGLE_CLOUD_PROJECT`
rather than from the `project` that `L6` returns, and no line reads
`credentials`. Importing this module therefore requires working Google
credentials for no benefit.

No module imports `get_document`, `create_document`, `update_document` or
`delete_document`. Three modules import the `db` client that `L7` builds:
`app/main.py:L8`, `app/services/document_service.py:L4` and
`app/tasks/background_tasks.py:L4`. Each of the three calls that client
directly instead of through these helpers, at `document_service.py:L17` and
`:L21` and at `background_tasks.py:L43`, `:L50`, `:L59`, `:L60` and `:L74`.
Those callers reach the `documents`, `document_permissions` and
`document_metadata` collections.

`app/main.py:L22` calls `db.is_connected()` and `app/main.py:L34` awaits
`db.close()`. A Firestore `Client` defines neither method.

None of the four helpers opens a transaction, sets a retry policy, sets a
timeout, or catches an exception.

Every `Lnn` locator in this module names a line of the file as committed,
before these docstrings shifted the numbering.
"""
from google.cloud.firestore import Client
from google.auth import default
from app.core.config import settings

# Initialize Firestore client
credentials, project = default()
db = Client(project=settings.GOOGLE_CLOUD_PROJECT)

def get_document(collection: str, document_id: str) -> dict:
    """Retrieve one document's stored fields from a named collection.

    The body performs one synchronous read against the named collection at
    `L10` and `L11`.

    Args:
        collection: Name of the Firestore collection holding the document.
        document_id: Identifier of the document to read.

    Returns:
        The stored fields as a dictionary when the snapshot exists, per `L12`
        and `L13`. `L14` returns None when the snapshot does not exist, which
        contradicts the `-> dict` annotation at `L9`. A caller that trusts
        that annotation and subscripts the result raises TypeError whenever
        the document is missing.

    Example:
        fields = get_document("documents", "abc123")
        title = fields["title"]

        The example cannot run as committed, because `L3` imports a
        `settings` name that `app/core/config.py` never defines.
    """
    doc_ref = db.collection(collection).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def create_document(collection: str, data: dict) -> str:
    """Add a document to a named collection and return its new identifier.

    The body performs one synchronous write at `L17` that creates a document
    with a server-generated identifier.

    `L17` calls `add`, which returns a two-element tuple holding the write
    timestamp and the new document reference. `L18` indexes element 1 to
    reach that reference before reading `.id`. The local name `doc_ref`
    therefore holds a tuple, not a document reference.

    Args:
        collection: Name of the Firestore collection to write to.
        data: Field names and values to store on the new document.

    Returns:
        The server-generated document identifier, per `L18`.

    Example:
        new_id = create_document("documents", {"title": "Draft"})

        The example cannot run as committed, because `L3` imports a
        `settings` name that `app/core/config.py` never defines.
    """
    doc_ref = db.collection(collection).add(data)
    return doc_ref[1].id

def update_document(collection: str, document_id: str, data: dict) -> None:
    """Merge the supplied fields into an existing document.

    The body performs one synchronous partial update at `L22`. Firestore
    rewrites only the keys present in `data` and leaves every other stored
    field unchanged.

    Args:
        collection: Name of the Firestore collection holding the document.
        document_id: Identifier of the document to modify.
        data: Field names and values to merge into the stored document.

    Returns:
        Nothing. The function is annotated `-> None` at `L20` and its body
        contains no return statement.
    """
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.update(data)

def delete_document(collection: str, document_id: str) -> None:
    """Delete a document from a named collection.

    The body performs one synchronous delete at `L26` that removes the
    document permanently. The helper writes no tombstone, sets no deleted
    flag, and asks for no confirmation before the delete.

    Args:
        collection: Name of the Firestore collection holding the document.
        document_id: Identifier of the document to remove.

    Returns:
        Nothing. The function is annotated `-> None` at `L24` and its body
        contains no return statement.
    """
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.delete()