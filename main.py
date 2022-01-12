from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Optional

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/seed")
def seed(db: Session = Depends(get_db)):
    crud.seed(db=db)
    return {
        "msg": "Success"
    }

@app.get("/items", response_model=list[schemas.Item])
def get_all_items(
    db: Session = Depends(get_db),
    compartment: Optional[str] = None
):
    return crud.getItems(db, compartment)
