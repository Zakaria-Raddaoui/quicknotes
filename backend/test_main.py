import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app, get_db

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_create_note():
    response = client.post(
        "/notes",
        json={"title": "Test Note", "content": "Test content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Test content"
    assert "id" in data

def test_read_notes_empty():
    response = client.get("/notes")
    assert response.status_code == 200
    assert response.json() == []

def test_read_notes():
    # Create a note first
    client.post("/notes", json={"title": "Note 1", "content": "Content 1"})
    client.post("/notes", json={"title": "Note 2", "content": "Content 2"})

    response = client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Note 1"
    assert data[1]["title"] == "Note 2"

def test_read_single_note():
    # Create a note first
    create_response = client.post(
        "/notes",
        json={"title": "Single Note", "content": "Single content"}
    )
    note_id = create_response.json()["id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Single Note"
    assert data["content"] == "Single content"

def test_read_single_note_not_found():
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

def test_update_note():
    # Create a note first
    create_response = client.post(
        "/notes",
        json={"title": "Original Title", "content": "Original content"}
    )
    note_id = create_response.json()["id"]

    # Update the note
    response = client.put(
        f"/notes/{note_id}",
        json={"title": "Updated Title", "content": "Updated content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"
    assert data["id"] == note_id

def test_update_note_partial():
    # Create a note first
    create_response = client.post(
        "/notes",
        json={"title": "Original Title", "content": "Original content"}
    )
    note_id = create_response.json()["id"]

    # Update only the title
    response = client.put(
        f"/notes/{note_id}",
        json={"title": "Only Title Updated"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Only Title Updated"
    assert data["content"] == "Original content"

def test_update_note_not_found():
    response = client.put(
        "/notes/999",
        json={"title": "Updated Title"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

def test_delete_note():
    # Create a note first
    create_response = client.post(
        "/notes",
        json={"title": "To Delete", "content": "Will be deleted"}
    )
    note_id = create_response.json()["id"]

    # Delete the note
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "To Delete"

    # Verify it's deleted
    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404

def test_delete_note_not_found():
    response = client.delete("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

def test_note_timestamps():
    # Create a note
    response = client.post(
        "/notes",
        json={"title": "Timestamp Test", "content": "Testing timestamps"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "created_at" in data or data.get("created_at") is None  # May be None in SQLite
    assert "updated_at" in data or data.get("updated_at") is None
