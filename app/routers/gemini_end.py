from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from .gemini import analyze_text, generate_note_content, analyze_note_from_db
from .notes import get_db

router = APIRouter()

@router.post("/analyze-text")
async def analyze_endpoint(note: str):
    result = analyze_text(note)
    return {'analysis': result}

@router.get("/analyze/{note_id}")
async def analyze_from_db_endpoint(
    note_id: int = Path(..., title="Note ID",),
    db: Session = Depends(get_db)
):
    result = analyze_note_from_db(db, note_id)
    if result == "Note not found":
        raise HTTPException(status_code=404, detail="Note not found")
    return {'analysis': result}

@router.post("/generate-note-content")
async def generate_note_content_endpoint(query: str):
    result = generate_note_content(query)
    return {'generate_text': result}
