from datetime import datetime
from app.models import Note, NoteVersion


def test_create_note():
    note = Note(title="Test Note", content="This is a test content")

    assert note.title == "Test Note"
    assert note.content == "This is a test content"
    assert isinstance(note.created_at, datetime)
    assert isinstance(note.updated_at, datetime)


def test_create_note_version():
    note = Note(id=1, title="Test Note", content="This is a test content")
    version = NoteVersion(note_id=note.id, version_number=1, content="Version 1 content")

    assert version.note_id == 1
    assert version.version_number == 1
    assert version.content == "Version 1 content"
    assert isinstance(version.created_at, datetime)


def test_relationship_between_note_and_versions():
    note = Note(id=1, title="Test Note", content="This is a test content")
    version1 = NoteVersion(note_id=note.id, version_number=1, content="Version 1 content")
    version2 = NoteVersion(note_id=note.id, version_number=2, content="Version 2 content")

    note.versions = [version1, version2]

    assert len(note.versions) == 2
    assert note.versions[0].content == "Version 1 content"
    assert note.versions[1].content == "Version 2 content"