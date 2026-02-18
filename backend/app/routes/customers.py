from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from typing import List
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/customers", tags=["customers"])

# Pydantic schemas
class OrderOut(BaseModel):
    id: int
    order_date: date
    amount: float

    class Config:
        from_attributes = True  # For SQLAlchemy 2.0 compatibility

class CustomerOut(BaseModel):
    id: int
    name: str
    email: str
    signup_date: date
    segment: str
    orders: List[OrderOut] = []

    class Config:
        from_attributes = True

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CustomerOut])
def list_customers(limit: int = 50, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
