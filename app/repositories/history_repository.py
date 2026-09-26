from decimal import Decimal

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.database import CalculationHistory


class HistoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, expression: str, result: Decimal) -> CalculationHistory:
        item = CalculationHistory(expression=expression, result=result)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def list_all(self) -> list[CalculationHistory]:
        statement = select(CalculationHistory).order_by(
            CalculationHistory.id.desc()
        )
        return list(self.session.scalars(statement).all())

    def get(self, record_id: int) -> CalculationHistory | None:
        return self.session.get(CalculationHistory, record_id)

    def delete(self, record_id: int) -> bool:
        item = self.get(record_id)
        if item is None:
            return False
        self.session.delete(item)
        self.session.commit()
        return True

    def delete_all(self) -> int:
        count = self.session.scalar(
            select(func.count()).select_from(CalculationHistory)
        )
        self.session.execute(delete(CalculationHistory))
        self.session.commit()
        return int(count or 0)
