# backend/app/main.py
from fastapi import FastAPI
from .routes import customers as customers_router
from .routes import metrics as metrics_router


app = FastAPI(title="Analytics Platform API")

@app.get("/")
def root():
    return {"message": "Analytics Platform API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# include customers router
app.include_router(customers_router.router)
app.include_router(metrics_router.router)

