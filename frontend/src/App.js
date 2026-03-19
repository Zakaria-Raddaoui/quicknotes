import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = 'http://localhost:8000';

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${API_URL}/notes`);
      if (!res.ok) throw new Error('Failed to fetch notes');
      const data = await res.json();
      setNotes(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) {
      alert('Please fill in both title and content');
      return;
    }

    try {
      if (editingId) {
        // Update existing note
        const res = await fetch(`${API_URL}/notes/${editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title, content })
        });
        if (!res.ok) throw new Error('Failed to update note');
        const updatedNote = await res.json();
        setNotes(notes.map(note => note.id === editingId ? updatedNote : note));
        setEditingId(null);
      } else {
        // Create new note
        const res = await fetch(`${API_URL}/notes`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title, content })
        });
        if (!res.ok) throw new Error('Failed to create note');
        const newNote = await res.json();
        setNotes([...notes, newNote]);
      }
      setTitle('');
      setContent('');
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error(err);
    }
  };

  const handleEdit = (note) => {
    setTitle(note.title);
    setContent(note.content);
    setEditingId(note.id);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this note?')) {
      return;
    }

    try {
      const res = await fetch(`${API_URL}/notes/${id}`, {
        method: 'DELETE'
      });
      if (!res.ok) throw new Error('Failed to delete note');
      setNotes(notes.filter(note => note.id !== id));
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error(err);
    }
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setTitle('');
    setContent('');
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Quick Notes</h1>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleSubmit} className="note-form">
          <input
            type="text"
            placeholder="Note title..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="input-title"
          />
          <textarea
            placeholder="Note content..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="input-content"
            rows="4"
          />
          <div className="form-buttons">
            <button type="submit" className="btn btn-primary">
              {editingId ? 'Update Note' : 'Add Note'}
            </button>
            {editingId && (
              <button type="button" onClick={handleCancelEdit} className="btn btn-secondary">
                Cancel
              </button>
            )}
          </div>
        </form>

        <div className="notes-list">
          {loading ? (
            <p>Loading notes...</p>
          ) : notes.length === 0 ? (
            <p className="empty-state">No notes yet. Create your first note above!</p>
          ) : (
            notes.map(note => (
              <div key={note.id} className="note-card">
                <h3>{note.title}</h3>
                <p>{note.content}</p>
                {note.created_at && (
                  <div className="note-meta">
                    Created: {new Date(note.created_at).toLocaleString()}
                  </div>
                )}
                <div className="note-actions">
                  <button onClick={() => handleEdit(note)} className="btn btn-edit">
                    Edit
                  </button>
                  <button onClick={() => handleDelete(note.id)} className="btn btn-delete">
                    Delete
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
