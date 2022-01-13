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

def IsItemExists(db: Session, item_name: str) -> bool:
    q = db.query(Item).filter(Item.name==item_name)
    return db.query(q.exists()).scalar()

def IsCompartmentExists(db: Session, compartment: str) -> bool:
    q = db.query(Compartment).filter(Compartment.name==compartment)
    return db.query(q.exists()).scalar()

def getItems(db: Session, compartment: str = None) -> list[Item]:
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

def getItem(db: Session, item_name: str) -> Item:
    return db.query(
        Item.name,
        Item.unit,
        Item.quantity,
        Compartment.name.label("compartment")
    ).filter(Item.name==item_name).first()

def getCompartment(db: Session, compartment: str) -> Compartment:
    return db.query(Compartment).\
              filter(Compartment.name==compartment).\
              first()

def createItem(db: Session, item: schemas.Item) -> Item:
    new_item = Item(
        name = item.name,
        unit = item.unit,
        quantity = item.quantity
    )

    compartment = getCompartment(db, item.compartment)
    new_item.compartmentId = compartment.id
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

