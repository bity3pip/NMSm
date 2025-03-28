from fastapi import APIRouter, Depends
from database import SessionLocal
from sqlalchemy.orm import Session
from analytics import analyze_notes


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/analytics/")
def get_notes_analytics(db: Session = Depends(get_db)):
    stats = analyze_notes(db)
    return stats
