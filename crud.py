from sqlalchemy.orm import Session
from . import models, schemas

def seed(db: Session):
    refrigerator = models.Compartment(name="refrigerator")
    db.add(refrigerator)
    db.commit()
    db.refresh(refrigerator)

    freezer = models.Compartment(name="freezer")
    db.add(freezer)
    db.commit()
    db.refresh(refrigerator)

    apples = models.Item(name="Apple", quantity=3, compartmentId=refrigerator.id)
    db.add(apples)
    db.commit()
    db.refresh(apples)

    banana = models.Item(name="Banana", quantity=2, compartmentId=freezer.id)
    db.add(banana)
    db.commit()
    db.refresh(apples)

def getAllItems(db: Session):
    return db.query(models.Item).all()
