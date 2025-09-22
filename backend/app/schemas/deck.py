from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class DeckCreate(BaseModel):
    title: str
    description: Optional[str] = None

class DeckOut(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True