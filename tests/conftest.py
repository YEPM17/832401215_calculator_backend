import pytest
from sqlalchemy.orm import sessionmaker

from app.database import create_database


@pytest.fixture()
def session_factory(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    _, factory = create_database(database_url)
    return factory


@pytest.fixture()
def session(session_factory):
    with session_factory() as db:
        yield db
