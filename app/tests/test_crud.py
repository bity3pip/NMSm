import pytest
from unittest.mock import MagicMock
from app.schemas import NoteCreate
from app.routers.crud import get_note, get_notes, create_note, update_note_content, delete_note
from app.models import Note

@pytest.fixture
def mock_db():
    return MagicMock()

def test_create_note(mock_db):
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    note_data = NoteCreate(title="Test Title", content="Test Content")
    mock_db.query().filter().first.return_value = None

    note = create_note(mock_db, note_data)

    assert note.title == "Test Title"
    assert note.content == "Test Content"
    mock_db.add.assert_called()
    mock_db.commit.assert_called()

def test_get_note(mock_db):
    mock_note = Note(id=1, title="Mock Title", content="Mock Content")
    mock_db.query().filter().first.return_value = mock_note

    fetched_note = get_note(mock_db, 1)

    assert fetched_note is not None
    assert fetched_note.id == 1
    assert fetched_note.title == "Mock Title"

def test_get_notes(mock_db):
    mock_notes = [Note(id=1, title="Note1", content="Content1"), Note(id=2, title="Note2", content="Content2")]
    mock_db.query().offset().limit().all.return_value = mock_notes

    notes = get_notes(mock_db)

    assert len(notes) == 2
    assert notes[0].title == "Note1"

def test_update_note_content(mock_db):
    mock_note = Note(id=1, title="Mock Title", content="Old Content", versions=[])
    mock_db.query().filter().first.return_value = mock_note
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()

    updated_note = update_note_content(mock_db, 1, "New Content")

    assert updated_note.content == "New Content"
    mock_db.commit.assert_called()

def test_delete_note(mock_db):
    mock_note = Note(id=1, title="ToDelete", content="Content")
    mock_db.query().filter().first.return_value = mock_note
    mock_db.delete = MagicMock()
    mock_db.commit = MagicMock()

    deleted_note = delete_note(mock_db, 1)

    assert deleted_note is not None
    assert deleted_note.title == "ToDelete"
    mock_db.delete.assert_called()
    mock_db.commit.assert_called()
