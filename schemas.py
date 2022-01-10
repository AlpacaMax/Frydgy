from typing import Optional
from pydantic import BaseModel, Field

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

class Compartment(BaseModel):
    location: str
    items: list[Item]

    class Config:
        orm_mode = True
