import os
from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session
from app.models import Note

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API"))

# Ensure analyze_text is an async function
async def analyze_text(note_text: str):
    prompt = (
        "Analyze my note as a professional psychologist and create a personality profile.\n\n"
        f"Note:\n{note_text}"
    )
    response = await client.models.generate_content(  # Ensure async call
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text

# Ensure analyze_note_from_db is async
async def analyze_note_from_db(db: Session, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        return "Note not found."

    return await analyze_text(note.content)

# Ensure generate_note_content is async
async def generate_note_content(query: str):
    prompt = "Help me create a title and text for my note.\n\n" f"Topic of the note:\n{query}"
    response = await client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text