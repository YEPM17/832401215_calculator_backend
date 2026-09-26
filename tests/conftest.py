import pytest
from fastapi.testclient import TestClient

from app.database import create_database
from app.main import create_app


@pytest.fixture()
def session_factory(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    _, factory = create_database(database_url)
    return factory


@pytest.fixture()
def session(session_factory):
    with session_factory() as db:
        yield db


@pytest.fixture()
def client(tmp_path):
    app = create_app(f"sqlite:///{tmp_path / 'api.db'}")
    with TestClient(app) as test_client:
        yield test_client
