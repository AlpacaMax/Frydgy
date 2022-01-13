from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Union

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
    compartment: Optional[str] = None,
):
    return crud.getItems(db, compartment)

@app.get("/item/{item_name}", response_model=schemas.Item)
def get_a_item(
    item_name: str,
    db: Session = Depends(get_db),
):
    return crud.getItem(db, item_name)

@app.post(
    "/item",
    response_model=schemas.Item,
    status_code=status.HTTP_201_CREATED,
)
def create_a_item(
    item: schemas.Item,
    db: Session = Depends(get_db)
):
    if (crud.IsItemExists(db, item.name)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item already exists!",
        )
    if (not crud.IsCompartmentExists(db, item.compartment)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Compartment does not exist!",
        )

    crud.createItem(db, item)

    return item
