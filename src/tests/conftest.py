import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from src.main import app
from src.database.models import Base
from src.database.database import get_async_session

SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_async_session] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def author_payload():
    return {
        "title": "Test title"
    }


@pytest.fixture()
def author_payload_updated():
    return {
        "title": "Updated title"
    }


# Fixture to generate a user payload
@pytest.fixture()
def book_payload():
    return {
        "title": "Test title",
        "author": 1
    }


@pytest.fixture()
def book_payload_updated():
    return {
        "title": "Updated title"
    }
