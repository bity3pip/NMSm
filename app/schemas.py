from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    content: Optional[str] = None
    title: Optional[str] = None


class NoteInDB(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NoteVersionBase(BaseModel):
    content: str


class NoteVersionInDB(NoteVersionBase):
    id: int
    created_at: datetime
    version_number: int

    class Config:
        orm_mode = True


class NoteDetail(NoteInDB):
    versions: List[NoteVersionInDB] = []
