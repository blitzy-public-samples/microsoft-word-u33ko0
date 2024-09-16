from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    content: str
    owner_id: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Document(DocumentBase):
    id: str
    created_at: datetime
    updated_at: datetime

class DocumentVersion(BaseModel):
    id: str
    document_id: str
    content: str
    created_at: datetime
    user_id: str