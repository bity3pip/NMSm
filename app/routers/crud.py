from sqlalchemy.orm import Session
import models, schemas


def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def get_notes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Note).offset(skip).limit(limit).all()


def create_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    version = models.NoteVersion(note_id=db_note.id, version_number=1, content=note.content)
    db.add(version)
    db.commit()

    db.refresh(db_note)
    return db_note


def update_note_content(db: Session, note_id: int, content: str):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note:
        db_note.content = content
        db_note.updated_at = models.datetime.utcnow()
        db.commit()

        version_number = len(db_note.versions) + 1
        new_version = models.NoteVersion(note_id=db_note.id, version_number=version_number, content=content)
        db.add(new_version)
        db.commit()

        db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note