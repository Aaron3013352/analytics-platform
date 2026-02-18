# backend/app/init_db.py
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models
import os

def generate_sample_csv(path="data/sample_data.csv", n_customers=30, orders_per_customer=5):
    # create data dir if missing
    os.makedirs(os.path.dirname(path), exist_ok=True)

    customers = []
    orders = []
    base_date = datetime.today() - timedelta(days=365)

    for cid in range(1, n_customers + 1):
        signup = base_date + timedelta(days=int(cid * 3 % 365))
        segment = ["Corporate", "Home Office", "Consumer"][cid % 3]
        email = f"user{cid}@example.com"
        customers.append({
            "id": cid,
            "name": f"Customer {cid}",
            "email": email,
            "signup_date": signup.date().isoformat(),
            "segment": segment
        })
        for o in range(orders_per_customer):
            order_date = signup + timedelta(days=(o * 30 + cid) % 365)
            amount = round(20 + ((cid * o) % 200) + (o * 3.14), 2)
            orders.append({
                "id": (cid - 1) * orders_per_customer + o + 1,
                "customer_id": cid,
                "order_date": order_date.date().isoformat(),
                "amount": amount
            })

    # write two CSVs
    customers_df = pd.DataFrame(customers)
    orders_df = pd.DataFrame(orders)
    customers_df.to_csv("data/customers.csv", index=False)
    orders_df.to_csv("data/orders.csv", index=False)
    print("Generated data/customers.csv and data/orders.csv")

def create_db_and_load():
    # create tables
    models.Base.metadata.create_all(bind=engine)
    print("Created tables in database")

    # load CSVs if present (if not, generate)
    if not (os.path.exists("data/customers.csv") and os.path.exists("data/orders.csv")):
        generate_sample_csv()

    customers_df = pd.read_csv("data/customers.csv", parse_dates=["signup_date"])
    orders_df = pd.read_csv("data/orders.csv", parse_dates=["order_date"])

    db: Session = SessionLocal()
    try:
        # simple insert (no dedupe logic; intended for initial run)
        for _, row in customers_df.iterrows():
            db.add(models.Customer(
                id=int(row["id"]),
                name=row["name"],
                email=row["email"],
                signup_date=row["signup_date"].date(),
                segment=row["segment"]
            ))
        for _, row in orders_df.iterrows():
            db.add(models.Order(
                id=int(row["id"]),
                customer_id=int(row["customer_id"]),
                order_date=row["order_date"].date(),
                amount=float(row["amount"])
            ))
        db.commit()
        print("Inserted sample rows into customers and orders")
    except Exception as e:
        db.rollback()
        print("Error loading data:", e)
    finally:
        db.close()

if __name__ == "__main__":
    create_db_and_load()
