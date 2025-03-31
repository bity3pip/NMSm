from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .gemini import analyze_text, generate_note_content, analyze_note_from_db
from .notes import get_db

router = APIRouter()

# Make sure to await the result of analyze_text
@router.post("/analyze-text")
async def analyze_endpoint(note: str):
    result = await analyze_text(note)  # Await the asynchronous function
    return {'analysis': result}


# Make sure to await the result of analyze_note_from_db
@router.get("/analyze/{note_id}")
async def analyze_from_db_endpoint(note_id: int, db: Session = Depends(get_db)):
    result = await analyze_note_from_db(db, note_id)  # Await the asynchronous function
    if result == "Note not found":
        raise HTTPException(status_code=404, detail="Note not found")
    return {'analysis': result}


# Make sure to await the result of generate_note_content
@router.post("/generate-note-content")
async def generate_note_content_endpoint(query: str):
    result = await generate_note_content(query)  # Await the asynchronous function
    return {'generate_text': result}