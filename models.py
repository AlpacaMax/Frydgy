from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    unit = Column(String)
    quantity = Column(Integer, default=1)
    compartmentId = Column(Integer, ForeignKey("compartments.id"))

    compartment = relationship("Compartment", back_populates="items")

class Compartment(Base):
    __tablename__ = "compartments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    items = relationship("Item", back_populates="compartment")
