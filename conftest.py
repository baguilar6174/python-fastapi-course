import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from app.main import app
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # This helps IDEs understand that app has dependency_overrides
    app: FastAPI
from db import get_session

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url, connect_args={'check_same_thread': False}, poolclass=StaticPool)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override  # type: ignore
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()  # type: ignore