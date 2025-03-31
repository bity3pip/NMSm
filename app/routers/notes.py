from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas
from ..routers import crud
from ..database import SessionLocal


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.NoteInDB)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db=db, note=note)


@router.get("/", response_model=List[schemas.NoteInDB])
def read_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_notes(db=db, skip=skip, limit=limit)


@router.get("/{note_id}", response_model=schemas.NoteDetail)
def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.get_note(db=db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@router.put("/{note_id}", response_model=schemas.NoteInDB)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    db_note = crud.get_note(db=db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.content:
        db_note = crud.update_note_content(db=db, note_id=note_id, content=note.content)

    return db_note


@router.delete("/{note_id}", response_model=schemas.NoteInDB)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.delete_note(db=db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note
