"""Define Pydantic models for document create, update, read, and version data."""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    """Describe the document fields shared by the create and read models.

    Attributes:
        title (str): Required document title.
        content (str): Required document body.
        owner_id (Optional[str]): Owner identifier, default `None`, so a
            document validates without an owner.
    """
    title: str
    content: str
    owner_id: Optional[str] = None

class DocumentCreate(DocumentBase):
    """Carry a document creation request body.

    The model adds no field of its own and inherits the whole `DocumentBase`
    shape.

    Attributes:
        title (str): Required document title, inherited from DocumentBase.
        content (str): Required document body, inherited from DocumentBase.
        owner_id (Optional[str]): Owner identifier, default `None`, inherited
            from DocumentBase.
    """
    pass

class DocumentUpdate(BaseModel):
    """Carry a partial document update patch.

    The model extends `BaseModel` rather than `DocumentBase`, so it redeclares
    both fields locally and models no owner.

    Attributes:
        title (Optional[str]): Replacement title, default `None`.
        content (Optional[str]): Replacement body, default `None`.
    """
    title: Optional[str] = None
    content: Optional[str] = None

class Document(DocumentBase):
    """Represent a stored document returned to the caller.

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