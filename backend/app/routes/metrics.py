from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import SessionLocal
from .. import models
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/metrics", tags=["metrics"])

class RevenueBySegment(BaseModel):
    segment: str
    total_revenue: float

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/revenue-by-segment", response_model=List[RevenueBySegment])
def revenue_by_segment(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Customer.segment,
            func.sum(models.Order.amount).label("total_revenue")
        )
        .join(models.Order, models.Customer.id == models.Order.customer_id)
        .group_by(models.Customer.segment)
        .all()
    )

    return [
        RevenueBySegment(
            segment=row.segment,
            total_revenue=round(row.total_revenue, 2)
        )
        for row in results
    ]
