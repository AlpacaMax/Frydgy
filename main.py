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
def get_an_item(
    item_name: str,
    db: Session = Depends(get_db),
):
    return crud.getItem(db, item_name)

@app.post(
    "/item",
    response_model=schemas.Item,
    status_code=status.HTTP_201_CREATED,
)
def create_an_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db)
):
    crud.createItem(db, item)
    return item

@app.put(
    "/item/{item_name}",
    response_model=schemas.Item,
)
def update_an_item(
    item_name: str,
    item: schemas.ItemUpdate,
    db: Session = Depends(get_db),
):
    if (not crud.IsItemExists(db, item_name)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item does not exist!",
        )

    return crud.updateItem(db, item_name, item)

@app.delete("/item/{item_name}")
def delete_an_item(item_name: str, db: Session = Depends(get_db)):
    if (not crud.IsItemExists(db, item_name)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item does not exist!",
        )

    crud.deleteItem(db, item_name)

    return {
        "msg": f"{item_name} deleted successfully!"
    }
