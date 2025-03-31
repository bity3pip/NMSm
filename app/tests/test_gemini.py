import pytest
import os
from unittest import mock
from sqlalchemy.orm import Session
from app.models import Note
from app.routers.gemini import analyze_text, analyze_note_from_db, generate_note_content


@pytest.fixture(autouse=True)
def mock_env_vars():
    with mock.patch.dict(os.environ, {"GOOGLE_API": "fake-api-key"}):
        yield


@pytest.fixture
def mock_genai_client():
    with mock.patch("google.genai.Client") as mock_client:
        yield mock_client


@pytest.fixture
def mock_db_session():
    db_session = mock.MagicMock(spec=Session)
    note = mock.MagicMock(spec=Note)
    note.content = "This is a test note content."
    db_session.query(Note).filter(Note.id == 1).first.return_value = note
    yield db_session


@pytest.mark.asyncio
async def test_analyze_text(mock_genai_client):
    mock_response = mock.MagicMock()
    mock_response.text = "Personality profile: Analytical, thoughtful, and introspective."
    mock_genai_client.models.generate_content.return_value = mock_response

    result = await analyze_text("This is a test note content.")

    assert result == "Personality profile: Analytical, thoughtful, and introspective."
    mock_genai_client.models.generate_content.assert_called_once_with(
        model="gemini-2.0-flash",
        contents="Analyze my note as a professional psychologist and create a personality profile.\n\nNote:\nThis is a test note content."
    )


@pytest.mark.asyncio
async def test_analyze_note_from_db(mock_db_session, mock_genai_client):
    mock_response = mock.MagicMock()
    mock_response.text = "Personality profile: Creative, intuitive, and open-minded."
    mock_genai_client.models.generate_content.return_value = mock_response

    result = await analyze_note_from_db(mock_db_session, 1)

    assert result == "Personality profile: Creative, intuitive, and open-minded."
    mock_db_session.query(Note).filter(Note.id == 1).first.assert_called_once()
    mock_genai_client.models.generate_content.assert_called_once_with(
        model="gemini-2.0-flash",
        contents="Analyze my note as a professional psychologist and create a personality profile.\n\nNote:\nThis is a test note content."
    )


@pytest.mark.asyncio
async def test_generate_note_content(mock_genai_client):
    mock_response = mock.MagicMock()
    mock_response.text = "Generated Title: My First Note\nGenerated Content: This is a test note."
    mock_genai_client.models.generate_content.return_value = mock_response

    result = await generate_note_content("My first test note")

    assert result == "Generated Title: My First Note\nGenerated Content: This is a test note."
    mock_genai_client.models.generate_content.assert_called_once_with(
        model="gemini-2.0-flash",
        contents="Help me create a title and text for my note.\n\nTopic of the note:\nMy first test note"
    )
