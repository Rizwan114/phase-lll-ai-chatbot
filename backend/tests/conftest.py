import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from typing import Generator

from src.main import app
from src.database.database import engine


@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client