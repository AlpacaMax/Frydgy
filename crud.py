from sqlalchemy import update, delete
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
    ).join(
        Compartment,
        Item.compartmentId==Compartment.id
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

def updateItem(db: Session, item_name: str, item: schemas.ItemUpdate) -> Item:
    item_dict = item.dict(exclude_unset=True)

    if ("compartment" in item_dict):
        item_dict["compartmentId"] = getCompartment(db, item.compartment).id
        del item_dict["compartment"]

    stmt = update(Item).where(Item.name==item_name).\
                        values(**item_dict).\
                        execution_options(synchronize_session="fetch")

    db.execute(stmt)
    db.commit()
    return getItem(db, item_name)

def deleteItem(db: Session, item_name: str) -> None:
    stmt = delete(Item).where(Item.name==item_name)

    db.execute(stmt)
    db.commit()

def createCompartment(db: Session, compartment: schemas.Compartment) -> Compartment:
    compartment_dict = compartment.dict(exclude_unset=True)
    new_compartment = Compartment(**compartment_dict)

    db.add(new_compartment)
    db.commit()
    db.refresh(new_compartment)

    return new_compartment

def updateCompartment(
    db: Session,
    cmprtmnt_name: str,
    cmprtmnt: schemas.CompartmentCreate,
) -> Compartment:
    compartment_dict = cmprtmnt.dict(exclude_unset=True)

    stmt = update(Compartment).where(Compartment.name==cmprtmnt_name).\
                               values(**compartment_dict).\
                               execution_options(synchronize_session="fetch")

    db.execute(stmt)
    db.commit()

    return getCompartment(db, compartment_dict["name"])
