from sqlalchemy.orm import Session
import models

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def search_items(db: Session, name: str):
    """
    Search items by name, using LIKE query
    """
    return db.query(models.Item).filter(models.Item.name.like(f"%{name}%")).all()

def create_item(db: Session, item: models.ItemBase):
    print(item)
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db.query(models.Item).filter(models.Item.id == item_id).delete()
    db.commit()
    return {"message": "Delete successfully"}

def update_item(db: Session, item_id: int, item: models.ItemBase):
    db.query(models.Item).filter(models.Item.id == item_id).update(item.model_dump())
    db.commit()
    return {"message": "Update successfully"}