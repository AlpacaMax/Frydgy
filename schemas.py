from typing import Optional
from pydantic import BaseModel, Field, validator

from . import crud, models, schemas
from .database import SessionLocal

def compartment_must_exist(v: str) -> str:
    db = SessionLocal()
    if (not crud.IsCompartmentExists(db, v)):
        raise ValueError("Compartment does not exist!")
    db.close()
    return v

class Item(BaseModel):
    name: str
    unit: Optional[str]
    quantity: int = Field(
        1,
        ge=1,
    )
    compartment: str

    class Config:
        orm_mode = True

class ItemCreate(Item):
    @validator("name")
    def name_not_exist(cls, v):
        db = SessionLocal()
        if (crud.IsItemExists(db, v)):
            raise ValueError("Item already exists!")
        db.close()
        return v

    _compartment_must_exist = validator(
        "compartment",
        allow_reuse=True
    )(compartment_must_exist)

class Compartment(BaseModel):
    location: str
    items: list[Item]

    class Config:
        orm_mode = True

class ItemUpdate(BaseModel):
    name: Optional[str]
    unit: Optional[str]
    quantity: Optional[int] = Field(
        None,
        ge=1,
    )
    compartment: Optional[str]

    @validator("name")
    def name_must_exist(cls, v):
        db = SessionLocal()
        if (crud.IsItemExists(db, v)):
            raise ValueError("New item name conflicts with existing one!")
        db.close()
        return v

    _compartment_must_exist = validator(
        "compartment",
        allow_reuse=True
    )(compartment_must_exist)
