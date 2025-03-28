import pandas as pd
from collections import Counter
import numpy as np
import nltk
from sqlalchemy.orm import Session
from models import Note  # Assuming you have a Note model

# Function to get statistics from notes
def analyze_notes(db: Session):
    # Fetch all notes
    notes = db.query(Note).all()
    notes_text = [note.content for note in notes]

    # Total word count
    total_word_count = sum(len(note.split()) for note in notes_text)

    # Average note length (in words)
    avg_note_length = total_word_count / len(notes_text) if notes_text else 0

    # Most common words or phrases
    all_words = ' '.join(notes_text).split()
    most_common_words = Counter(all_words).most_common(10)

    # Top 3 longest and shortest notes
    longest_notes = sorted(notes_text, key=len, reverse=True)[:3]
    shortest_notes = sorted(notes_text, key=len)[:3]

    # Compile stats
    stats = {
        "total_word_count": total_word_count,
        "average_note_length": avg_note_length,
        "most_common_words": most_common_words,
        "top_3_longest_notes": longest_notes,
        "top_3_shortest_notes": shortest_notes,
    }

    return stats

