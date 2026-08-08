"""Declare the Pydantic contracts for documents and document versions.

Five models cover the shared fields, the create and update payloads, the read
model and a version record. Two names for the owner appear in this one file:
`DocumentBase.owner_id` and `DocumentVersion.user_id`, and the service layer
writes a third position by storing `user_id` on the document record itself.

`List` is imported and never used. See ./README.md and
../../../docs/data-model.md, which sets the four ownership positions side by
side.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    """Carry the fields every document representation shares.

    Attributes:
        title: Document title, required.
        content: Document body, required.
        owner_id: Owning user identifier. Optional with a default of `None`,
            so a document validates without the field the routers compare
            for authorization.
    """
    title: str
    content: str
    owner_id: Optional[str] = None

class DocumentCreate(DocumentBase):
    """Model the create request body.

    Inherits every field from `DocumentBase` and adds none, so a create
    request may carry a client-supplied `owner_id`. The service overwrites
    the stored owner with its own `user_id` key.
    """
    pass

class DocumentUpdate(BaseModel):
    """Model the update request body.

    Does not inherit `DocumentBase`, so an update cannot change the owner.

    Attributes:
        title: New title, optional.
        content: New body, optional.
    """
    title: Optional[str] = None
    content: Optional[str] = None

class Document(DocumentBase):
    """Model a stored document as the API returns it.

    Attributes:
        id: Firestore document identifier.
        created_at: Creation timestamp, required.
        updated_at: Last-modification timestamp, required.

    Both timestamps are required and no service writes either, so building
    this model from a stored record raises a validation error.
    """
    id: str
    created_at: datetime
    updated_at: datetime

class DocumentVersion(BaseModel):
    """Model one stored revision of a document.

    Attributes:
        id: Version identifier.
        document_id: Identifier of the document this revision belongs to.
        content: The document body at this revision.
        created_at: When the revision was written.
        user_id: Author of the revision, and the second owner field name
            in the file.

    No route, service or task reads or writes this model, so no revision is
    ever stored.
    """
    id: str
    document_id: str
    content: str
    created_at: datetime
    user_id: str