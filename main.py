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
    if (not crud.IsItemExists(db, item_name)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item does not exist!",
        )

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

@app.get(
    "/compartment/{cmprtmnt_name}",
    response_model=schemas.Compartment
)
def get_a_compartment(cmprtmnt_name: str, db: Session = Depends(get_db)):
    cmprtmnt = crud.getCompartment(db, cmprtmnt_name)
    if (cmprtmnt is None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compartment does not exist!",
        )

    return cmprtmnt

@app.post(
    "/compartment",
    response_model=schemas.Compartment,
    status_code=status.HTTP_201_CREATED,
)
def create_a_compartment(
    cmprtmnt: schemas.CompartmentCreate,
    db: Session = Depends(get_db),
):
    return crud.createCompartment(db, cmprtmnt)

@app.put(
    "/compartment/{cmprtmnt_name}",
    response_model=schemas.Compartment,
)
def update_a_compartment(
    cmprtmnt_name: str,
    new_cmprtmnt: schemas.CompartmentCreate,
    db: Session = Depends(get_db)
):
    if (not crud.IsCompartmentExists(db, cmprtmnt_name)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compartment does not exist!",
        )

    return crud.updateCompartment(db, cmprtmnt_name, new_cmprtmnt)

@app.delete("/compartment/{cmprtmnt_name}")
def delete_a_compartment(
    cmprtmnt_name: str,
    db: Session = Depends(get_db)
):
    if (not crud.IsCompartmentExists(db, cmprtmnt_name)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compartment does not exist!",
        )

    crud.deleteCompartment(db, cmprtmnt_name)

    return {
        "msg": f"{cmprtmnt_name} deleted successfully!"
    }

