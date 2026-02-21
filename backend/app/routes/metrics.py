from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import SessionLocal
from .. import models
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/metrics", tags=["metrics"])


# -----------------------------
# Database Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Revenue by Segment
# -----------------------------
class RevenueBySegment(BaseModel):
    segment: str
    total_revenue: float

    class Config:
        from_attributes = True


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


# -----------------------------
# Revenue by Month
# -----------------------------
@router.get("/revenue-by-month")
def revenue_by_month(db: Session = Depends(get_db)):
    results = (
        db.query(
            func.strftime("%Y-%m", models.Order.order_date).label("year_month"),
            func.sum(models.Order.amount).label("total_revenue")
        )
        .group_by("year_month")
        .order_by("year_month")
        .all()
    )

    return [
        {
            "year_month": row.year_month,
            "total_revenue": round(row.total_revenue, 2)
        }
        for row in results
    ]


# -----------------------------
# Customer Lifetime Value
# -----------------------------
@router.get("/customer-lifetime-value")
def customer_lifetime_value(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Customer.id,
            models.Customer.name,
            func.sum(models.Order.amount).label("lifetime_value")
        )
        .join(models.Order, models.Customer.id == models.Order.customer_id)
        .group_by(models.Customer.id)
        .order_by(func.sum(models.Order.amount).desc())
        .all()
    )

    return [
        {
            "customer_id": row.id,
            "customer_name": row.name,
            "lifetime_value": round(row.lifetime_value, 2)
        }
        for row in results
    ]

@router.get("/top-customers")
def top_customers(limit: int = 5, db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Customer.id,
            models.Customer.name,
            func.sum(models.Order.amount).label("lifetime_value")
        )
        .join(models.Order, models.Customer.id == models.Order.customer_id)
        .group_by(models.Customer.id)
        .order_by(func.sum(models.Order.amount).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "customer_id": row.id,
            "customer_name": row.name,
            "lifetime_value": round(row.lifetime_value, 2)
        }
        for row in results
    ]
