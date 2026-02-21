# Analytics Platform (Portfolio Capstone)

**Short summary:**  
End-to-end analytics platform demonstrating data + software skills: backend API (FastAPI), ORM (SQLAlchemy), SQLite analytics database, and business KPIs consumed by a BI tool (Power BI).

---

## Features
- FastAPI endpoints for:
  - `/customers` — list customers and their orders
  - `/metrics/revenue-by-segment` — total revenue by segment
  - `/metrics/revenue-by-month` — monthly revenue time series
  - `/metrics/customer-lifetime-value` — lifetime value per customer
- SQLAlchemy models (`Customer`, `Order`)
- Data generator + initializer that creates `data/customers.csv`, `data/orders.csv` and populates `data/analytics.db`
- Clean project structure and example queries

---

## Tech stack
- Python, FastAPI, Uvicorn
- SQLAlchemy ORM
- SQLite (data)
- Pandas (data generation)
- Power BI (dashboard - connect to SQLite)

---

## Quick start (local)
> Tested on Windows + VS Code

1. Clone the repo (when pushed to GitHub)
2. Create + activate venv:
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate
