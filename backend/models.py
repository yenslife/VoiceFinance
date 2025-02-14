from sqlalchemy import Column, Integer, String, DateTime
from datetime import date, datetime
from database import Base

# SQLAlchemy model
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String, index=True)
    date_ = Column(DateTime, index=True)
    amount = Column(Integer, index=True)
    create_at = Column(DateTime, default=datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    note = Column(String, index=True)

# Pydantic model
from pydantic import BaseModel
from typing import Optional

today = date.today()

class ItemBase(BaseModel):
    name: str
    location: Optional[str] = None
    date_: Optional[date] = today
    amount: int = 0
    create_at: Optional[datetime] = None
    note: Optional[str] = None
    class Config:
        orm_mode = True