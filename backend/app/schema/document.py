"""Define the Pydantic models that shape document requests and responses.

Five models cover the shared field set, the create request body, the partial update
patch, the stored read model, and a version snapshot.

Every import resolves and `import app.schema.document` succeeds, because this file
depends only on pydantic, typing and datetime, never on the absent `settings`
singleton in app/core/config.py. `List` on the typing import line is imported
and never used. No app/schema/template.py exists, though app/api/templates.py:L3
imports Template, TemplateCreate and TemplateUpdate from app.schema.template.

DocumentBase declares `owner_id` while DocumentVersion declares `user_id`. See
docs/data-model.md for the full comparison.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    """Declare the document fields shared by the create body and the read model.

    Extends `BaseModel`. DocumentCreate and Document both inherit every field
    declared here.

    Attributes:
        title (str): Required document title.
        content (str): Required document body, held as a plain string.
        owner_id (Optional[str]): Owner identifier, default `None`. A document
            therefore validates with no owner recorded, while ownership
            decides access at app/services/document_service.py:L35-L36.
    """
    title: str
    content: str
    owner_id: Optional[str] = None

class DocumentCreate(DocumentBase):
    """Carry an inbound document creation request body.

    Extends `DocumentBase` and adds no field, so the request body accepts a
    client-supplied `owner_id`. app/api/documents.py:L11 binds the model as
    the create request body.

    Attributes:
        title (str): Required document title, inherited from DocumentBase.
        content (str): Required document body, inherited from DocumentBase.
        owner_id (Optional[str]): Owner identifier, default `None`, inherited
            from DocumentBase.
    """
    pass

class DocumentUpdate(BaseModel):
    """Carry an inbound partial document update patch.

    Extends `BaseModel` rather than `DocumentBase`, so the model shares no
    field definition with the create path. app/api/documents.py:L31 binds the
    model as the update request body and passes it to the service signature
    at app/services/document_service.py:L43.

    Attributes:
        title (Optional[str]): Replacement title, default `None`.
        content (Optional[str]): Replacement body, default `None`.
    """
    title: Optional[str] = None
    content: Optional[str] = None

class Document(DocumentBase):
    """Represent a stored document returned to the caller.

    Extends `DocumentBase` and adds three required fields.

    `Document(**doc_data)` at app/services/document_service.py:L24 raises a
    Pydantic validation error on two missing required fields.
    app/services/document_service.py:L18-L21 assembles `doc_data` from
    `title`, `content`, `owner_id`, `user_id` and `id`, and writes neither
    `created_at` nor `updated_at`.

    app/api/documents.py:L26, :L34 and :L43 read `.user_id` on a value of this
    type. The model never declares `user_id`, so the attribute access fails.

    Attributes:
        id (str): Required Firestore document identifier.
        created_at (datetime): Required creation timestamp. No service writes
            the field.
        updated_at (datetime): Required modification timestamp. No service
            writes the field.
        title (str): Required document title, inherited from DocumentBase.
        content (str): Required document body, inherited from DocumentBase.
        owner_id (Optional[str]): Owner identifier, default `None`, inherited
            from DocumentBase.
    """
    id: str
    created_at: datetime
    updated_at: datetime

class DocumentVersion(BaseModel):
    """Represent a historical content snapshot of a document.

    Extends `BaseModel` and declares `user_id` where DocumentBase declares
    `owner_id`. No module imports the class, and the name appears exactly once
    across the repository's Python files, at this definition.

    Attributes:
        id (str): Required snapshot identifier.
        document_id (str): Required identifier of the document the snapshot
            belongs to.
        content (str): Required document body held by the snapshot.
        created_at (datetime): Required snapshot timestamp.
        user_id (str): Required user identifier recorded on the snapshot.
    """
    id: str
    document_id: str
    content: str
    created_at: datetime
    user_id: str