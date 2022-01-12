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
    db.refresh(freezer)

    apples = Item(name="Apple", quantity=3, compartmentId=refrigerator.id)
    db.add(apples)
    db.commit()
    db.refresh(apples)

    banana = Item(name="Banana", quantity=2, compartmentId=freezer.id)
    db.add(banana)
    db.commit()
    db.refresh(banana)

def getItems(db: Session, compartment: str = None):
    query = db.query(
        Item.name,
        Item.unit,
        Item.quantity,
        Compartment.name.label("compartment")
    ).join(
        Compartment,
        Item.compartmentId==Compartment.id
    )

    if (compartment is not None):
        query = query.filter(Compartment.name==compartment)

    return query.all()
