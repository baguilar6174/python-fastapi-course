from fastapi import FastAPI, HTTPException
from datetime import datetime
import zoneinfo

from models import CustomerCreate, Customer, Transaction, Invoice

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "PE": "America/Lima",
    "AZ": "America/Sao_Paulo",
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone = timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone)
    return {"time": datetime.now(tz)}


db_customers: list[Customer] = []


@app.post("/customers", response_model=Customer)
async def create_customer(data: CustomerCreate):
    customer = Customer.model_validate(data.model_dump())
    customer.id = len(db_customers)
    db_customers.append(customer)
    return customer


@app.get("/customers", response_model=list[Customer])
async def get_customers():
    return db_customers


@app.get("/customer/{id}", response_model=Customer)
async def get_customer_by_id(id: int):
    customer = next((c for c in db_customers if c.id == id), None)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.post("/transactions")
async def create_transaction(data: Transaction):
    return data


@app.post("/invoices")
async def create_invoice(data: Invoice):
    return data
