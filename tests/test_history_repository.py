from decimal import Decimal

from app.repositories.history_repository import HistoryRepository


def test_create_and_list_history(session):
    repository = HistoryRepository(session)

    created = repository.create("1+1", Decimal("2"))
    items = repository.list_all()

    assert created.id is not None
    assert created.expression == "1+1"
    assert created.result == Decimal("2")
    assert len(items) == 1
    assert items[0].id == created.id


def test_get_delete_and_clear_history(session):
    repository = HistoryRepository(session)
    first = repository.create("2*3", Decimal("6"))
    second = repository.create("4/2", Decimal("2"))

    assert repository.get(first.id).expression == "2*3"
    assert repository.delete(first.id) is True
    assert repository.delete(first.id) is False
    assert repository.delete_all() == 1
    assert repository.get(second.id) is None
