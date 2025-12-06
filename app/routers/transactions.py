from fastapi import APIRouter, HTTPException, status, Query
from models import Transaction, TransactionCreate, Customer
from sqlmodel import select, func
from pydantic import BaseModel
from math import ceil

from db import SessionDependency

router = APIRouter()


class PaginatedTransactionsResponse(BaseModel):
    transactions: list[Transaction]
    total_records: int
    total_pages: int
    current_page: int
    records_per_page: int


@router.post("/transactions", status_code=status.HTTP_201_CREATED, tags=["transactions"])
async def create_transaction(data: TransactionCreate, session: SessionDependency):
    transaction_data_dict = data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get("customer_id"))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db


@router.get("/transactions", response_model=PaginatedTransactionsResponse, tags=["transactions"])
async def list_transactions(
        session: SessionDependency,
        skip: int = Query(0, description="Number of records to skip"),
        limit: int = Query(10, description="Number of records to return"),
):
    # Get total count of transactions
    count_query = select(func.count(Transaction.id))
    total_records = session.exec(count_query).one()

    # Get paginated transactions
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()

    # Calculate pagination info
    total_pages = ceil(total_records / limit) if limit > 0 else 1
    current_page = (skip // limit) + 1 if limit > 0 else 1

    return PaginatedTransactionsResponse(
        transactions=list(transactions),
        total_records=total_records,
        total_pages=total_pages,
        current_page=current_page,
        records_per_page=limit
    )
