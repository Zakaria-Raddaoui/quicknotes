# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import SessionLocal, engine, Base
from sqlalchemy.exc import OperationalError
import time
from fastapi.middleware.cors import CORSMiddleware

MAX_RETRIES = 10

for i in range(MAX_RETRIES):
    try:
        Base.metadata.create_all(bind=engine)
        break
    except OperationalError:
        print(f"[DB Retry] Attempt {i+1}/{MAX_RETRIES} - Waiting for database...")
        time.sleep(2)
else:
    raise Exception("Database connection failed after multiple retries.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/notes", response_model=list[schemas.NoteOut])
def read_notes(db: Session = Depends(get_db)):
    return crud.get_notes(db)

@app.post("/notes", response_model=schemas.NoteOut)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, note)

@app.delete("/notes/{note_id}", response_model=schemas.NoteOut)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.delete_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
