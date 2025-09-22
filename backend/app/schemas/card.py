from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class CardCreate(BaseModel):
    word: str
    definition: str
    status: Optional[str] = None

class CardOut(BaseModel):
    id: UUID
    deck_id: UUID
    word: str
    definition: str
    status: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
