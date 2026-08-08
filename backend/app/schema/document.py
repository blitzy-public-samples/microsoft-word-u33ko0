"""Declare the Pydantic contracts for documents and document versions.

Five models: `DocumentBase`, `DocumentCreate`, `DocumentUpdate`, `Document` and
`DocumentVersion`. The module imports cleanly and is one of the few backend modules that
does. `List` is imported and unused.

Pydantic publishes each model's own docstring as the `description` of the JSON
Schema it generates, and FastAPI copies that schema into the OpenAPI document it
serves. Every class docstring below therefore states the public contract only, and
the internal analysis for all five models sits in this module docstring, which
Pydantic never publishes.

Every import resolves and `import app.schema.document` succeeds, because this file
depends only on pydantic, typing and datetime, never on the absent `settings`
singleton in app/core/config.py. `List` on the typing import line is imported
and never used. No app/schema/template.py exists, though app/api/templates.py:L70
imports Template, TemplateCreate and TemplateUpdate from app.schema.template.

Consumers. app/api/documents.py:L54 binds DocumentCreate as the create request
body. app/api/documents.py:L189 binds DocumentUpdate as the update request body and
passes it to the service signature at app/services/document_service.py:L192.
DocumentCreate adds no field of its own, so the create request body accepts a
client-supplied `owner_id`. No module imports DocumentVersion, and the name
appears exactly once across the repository's Python files, at its definition on
L114.

DocumentBase declares `owner_id` while DocumentVersion declares `user_id`. See
docs/data-model.md for the full comparison. `owner_id` at `document.py:L66` is
optional with a default of `None`, so a document validates with no owner recorded,
and ownership decides access at app/services/document_service.py:L184, :L250 and :L289.

`Document(**doc_data)` at app/services/document_service.py:L130 raises a Pydantic
validation error on two missing required fields.
app/services/document_service.py:L124-L126 assembles `doc_data` from `title`,
`content`, `owner_id`, `user_id` and `id`, and writes neither `created_at` nor
`updated_at`, which L111 and L112 declare as required.

app/api/documents.py:L184, :L232 and :L279 read `.user_id` on a value of the
`Document` type. The model never declares `user_id`, so the attribute access
fails.

No field carries a length bound. `title` and `content` at L64 and L65, and the two
DocumentUpdate fields at L93 and L94, all carry bare `str` or `Optional[str]`
annotations with no `min_length` and no `max_length`, and no model declares a
`@validator`. No route and no committed middleware caps the request body size, so
an authenticated caller can submit an arbitrarily large `title` or `content`.

Every `Lnn` reference below points at the current layout of the file it names. A
bare `Lnn` points into this file, and a `path:Lnn` points into the named file.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    """Carry the fields shared by every document representation.

    Attributes:
        title (str): Required document title.
        content (str): Required document body, held as a plain string.
        owner_id (Optional[str]): Owner identifier, default `None`, so a
            document validates with no owner recorded.
    """
    title: str
    content: str
    owner_id: Optional[str] = None

class DocumentCreate(DocumentBase):
    """Request body for creating a document.

    Extends `DocumentBase` and adds no field, so the request body accepts a
    client-supplied `owner_id`.

    Attributes:
        title (str): Required document title, inherited from DocumentBase.
        content (str): Required document body, inherited from DocumentBase.
        owner_id (Optional[str]): Owner identifier, default `None`, inherited
            from DocumentBase.
    """
    pass

class DocumentUpdate(BaseModel):
    """Request body for updating a document.

    Extends `BaseModel` rather than `DocumentBase`, so the model shares no
    field definition with the create path. Both fields are optional, so a caller
    may send either one alone.

    Attributes:
        title: Replacement title. Optional.
        content: Replacement body. Optional.
    """
    title: Optional[str] = None
    content: Optional[str] = None

class Document(DocumentBase):
    """Represent a stored document returned to the caller.

    Extends `DocumentBase` and adds three required fields.

    Attributes:
        id (str): Required Firestore document identifier.
        created_at (datetime): Required creation timestamp.
        updated_at (datetime): Required modification timestamp.
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
    `owner_id`.

    Attributes:
        id: Version identifier. Required.
        document_id: Identifier of the document this snapshot belongs to. Required.
        content: Snapshot body. Required.
        created_at: Snapshot timestamp. Required.
        user_id: Identifier of the user who produced the snapshot. Required, and named
            `owner_id` on `DocumentBase` above.

    Note:
        No code path constructs this model, so no version record is ever written.
    """
    id: str
    document_id: str
    content: str
    created_at: datetime
    user_id: str