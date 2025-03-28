from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime,  default=func.now())
    updated_at = Column(DateTime,  default=func.now(), onupdate=func.now())

    versions = relationship("NoteVersion", back_populates="note")

class NoteVersion(Base):
    __tablename__ = "note_versions"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id"))
    version_number = Column(Integer, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    note = relationship("Note", back_populates="versions")