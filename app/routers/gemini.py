import os
from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session
from app.models import Note

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API"))

def analyze_text(note_text: str):
    prompt = (
        "Analyze my note as a professional psychologist and create a personality profile.\n\n"
        f"Note:\n{note_text}"
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text

def analyze_note_from_db(db: Session, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        return "Note not found."

    return  analyze_text(note.content)

def generate_note_content(query: str):
    prompt = "Help me create a title and text for my note.\n\n" f"Topic of the note:\n{query}"
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text