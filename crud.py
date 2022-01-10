from sqlalchemy.orm import Session
from . import schemas
from .models import Item, Compartment

def seed(db: Session):
    refrigerator = Compartment(name="refrigerator")
    db.add(refrigerator)
    db.commit()
    db.refresh(refrigerator)

    freezer = Compartment(name="freezer")
    db.add(freezer)
    db.commit()
    db.refresh(refrigerator)

    apples = Item(name="Apple", quantity=3, compartmentId=refrigerator.id)
    db.add(apples)
    db.commit()
    db.refresh(apples)

    banana = Item(name="Banana", quantity=2, compartmentId=freezer.id)
    db.add(banana)
    db.commit()
    db.refresh(apples)

def getAllItems(db: Session):
    return db.query(Item.name, Item.unit, Item.quantity, Compartment.name.label("compartment")).\
              join(Compartment, Item.compartmentId==Compartment.id).\
              all()
