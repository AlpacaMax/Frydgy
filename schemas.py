from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    unit: Optional[str]
    quantity: int = 1

    class Config:
        orm_mode = True

class Compartment(BaseModel):
    location: str
    items: list[Item]

    class Config:
        orm_mode = True
