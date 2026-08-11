"""Declare the Celery application and its three background tasks.

The broker URL comes from `settings.REDIS_URL`, and no committed environment
runs a broker: the Compose file declares no Redis service and the Terraform
configuration declares no managed instance. No route, service or script
enqueues any of these tasks, and no worker or beat process is defined
anywhere, so none of them runs as committed.

`datetime` is used twice below and only `timedelta` is imported, so both uses
raise `NameError`. `settings` is imported from `app.core.config`, which never
creates it, and `EXPORT_BUCKET_NAME` and `DOCUMENT_BUCKET_NAME` are declared
nowhere. See ./README.md for the task table.
"""
from celery import Celery
from google.cloud.storage import Client
from app.core.config import settings
from app.db.firestore import db
from app.services.document_service import DocumentService
from app.services.export_service import ExportService
from datetime import timedelta

celery_app = Celery('microsoft_word', broker=settings.REDIS_URL)

@celery_app.task
def process_document_export(document_id: str, export_format: str, user_id: str) -> str:
    """Export one document to the requested format and return a signed link.

    The task reads the document through `DocumentService`, converts it
    through `ExportService.convert_document`, uploads the result under
    `exports/{user_id}/{document_id}.{export_format}` and signs a one-hour
    link. Three steps cannot run: the read is not awaited on an `async`
    method, `ExportService` declares no `convert_document`, and the signing
    call passes no `version`. That last omission signs under the client
    default rather than the version 4 scheme the service methods request.
    See the HUMAN ASSISTANCE NEEDED marker below.

    The key here carries a user segment, and the two `ExportService` methods
    write `exports/{document.id}.{ext}` instead, so the same artifact has two
    layouts.

    Args:
        document_id: Document to export.
        export_format: Target format, used as the object extension.
        user_id: Owning user, used in the object key and passed to the read.

    Returns:
        A signed URL string for the uploaded object.
    """
    # HUMAN ASSISTANCE NEEDED
    # This function needs review for production readiness and error handling
    document_service = DocumentService()
    export_service = ExportService()
    storage_client = Client()

    # Retrieve document from DocumentService
    document = document_service.get_document(document_id, user_id)

    # Convert document to requested format using ExportService
    exported_file = export_service.convert_document(document, export_format)

    # Upload exported file to Google Cloud Storage
    bucket = storage_client.bucket(settings.EXPORT_BUCKET_NAME)
    blob = bucket.blob(f"exports/{user_id}/{document_id}.{export_format}")
    blob.upload_from_file(exported_file)

    # Generate signed URL for the exported file
    signed_url = blob.generate_signed_url(expiration=timedelta(hours=1))

    return signed_url

@celery_app.task
@celery_app.periodic_task(run_every=timedelta(days=1))
def cleanup_expired_documents():
    """Delete documents whose retention period has passed.

    For each expired record the task removes the Firestore document, the
    Cloud Storage object at `{user_id}/{doc_id}`, the permission records and
    the metadata record. Deletion is not transactional, so a failure part
    way through leaves the remaining artifacts in place.

    Three things stop it running. The stacked `@celery_app.periodic_task`
    decorator is not part of the Celery API, and `datetime` is never imported.
    The permission cleanup calls `.delete()` on the list that a query returns
    rather than on a document reference. No beat schedule exists, so nothing
    would trigger the daily run either. See the HUMAN ASSISTANCE NEEDED marker
    below.

    Returns:
        None.
    """
    # HUMAN ASSISTANCE NEEDED
    # This function needs review for production readiness, error handling, and optimization
    document_service = DocumentService()

    # Query Firestore for documents past their retention period
    expired_docs = db.collection('documents').where('expiration_date', '<=', datetime.now()).get()

    for doc in expired_docs:
        doc_id = doc.id
        user_id = doc.get('user_id')

        # Remove document data from Firestore
        db.collection('documents').document(doc_id).delete()

        # Delete associated files from Google Cloud Storage
        storage_client = Client()
        bucket = storage_client.bucket(settings.DOCUMENT_BUCKET_NAME)
        blob = bucket.blob(f"{user_id}/{doc_id}")
        blob.delete()

        # Remove any related metadata or permissions
        db.collection('document_permissions').where('document_id', '==', doc_id).get().delete()
        db.collection('document_metadata').document(doc_id).delete()

@celery_app.task
def update_document_statistics(document_id: str):
    """Recount a document's words and pages and store the result.

    The read at L135 omits the `user_id` the service declares, so the call
    raises `TypeError` before anything else runs. Supplying it would return a
    coroutine that is never awaited, so `document.content` at L138 would raise
    `AttributeError` next, then `document.pages` at L139, which no schema
    declares. `datetime` is never imported, so L146 would raise last.

    Args:
        document_id: Document to recount.

    Returns:
        None. The statistics are merged into the Firestore record under a
        `statistics` key.
    """
    document_service = DocumentService()

    # Retrieve document from DocumentService
    document = document_service.get_document(document_id)

    # Calculate statistics
    word_count = len(document.content.split())
    page_count = len(document.pages)

    # Update document metadata in Firestore
    db.collection('documents').document(document_id).update({
        'statistics': {
            'word_count': word_count,
            'page_count': page_count,
            'last_updated': datetime.now()
        }
    })

    # Trigger any necessary analytics events
    # This part would depend on the specific analytics service being used
    # For example:
    # analytics_service.track_event('document_statistics_updated', {
    #     'document_id': document_id,
    #     'word_count': word_count,
    #     'page_count': page_count
    # })