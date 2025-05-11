from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Todo

router = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.get("/todos")
def read_todos(db: Session = Depends(get_db)):
  return db.query(Todo).all()

@router.post("/todos")
def create_todos(title: str, db: Session = Depends(get_db)):
  todo = Todo(title=title)
  db.add(todo)
  db.commit()
  db.refresh(todo)
  return todo

@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, completed: bool, db: Session = Depends(get_db)):
  todo = db.query(Todo).filter(Todo.id == todo_id).first()
  if todo:
    todo.comleted = completed
    db.commit()
  return todo

