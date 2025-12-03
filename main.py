from fastapi import FastAPI, HTTPException, status
from datetime import datetime
import zoneinfo
from sqlmodel import select

from models import CustomerCreate, CustomerUpdate, Customer, Transaction, Invoice
from db import SessionDependency, create_all_tables

app = FastAPI(lifespan=create_all_tables)

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
async def create_customer(data: CustomerCreate, session: SessionDependency):
    customer = Customer.model_validate(data.model_dump())

    # save in database
    session.add(customer)
    session.commit()
    session.refresh(customer)

    """
    In local memory
    customer.id = len(db_customers)
    db_customers.append(customer)
    """
    return customer


@app.get("/customers", response_model=list[Customer])
async def get_customers(session: SessionDependency):
    """
    In local memory
    return db_customers
    """
    return session.exec(select(Customer)).all()


@app.get("/customer/{id}", response_model=Customer)
async def get_customer_by_id(id: int, session: SessionDependency):
    """
    In local memory
    customer = next((c for c in db_customers if c.id == id), None)
    """
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@app.delete("/customer/{id}")
async def remove_customer_by_id(id: int, session: SessionDependency):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return { "detail": "Customer deleted" }


@app.patch("/customer/{id}", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def update_customer_by_id(id: int, data: CustomerUpdate, session: SessionDependency):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    data_dict = data.model_dump(exclude_unset = True)
    customer.sqlmodel_update(data_dict)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@app.post("/transactions")
async def create_transaction(data: Transaction):
    return data


@app.post("/invoices")
async def create_invoice(data: Invoice):
    return data
