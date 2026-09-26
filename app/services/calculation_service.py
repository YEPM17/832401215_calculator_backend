from app.repositories.history_repository import HistoryRepository
from app.services.expression_parser import ExpressionParser, normalize_expression


class CalculationService:
    def __init__(
        self,
        repository: HistoryRepository,
        parser: ExpressionParser | None = None,
    ):
        self.repository = repository
        self.parser = parser or ExpressionParser()

    def calculate(self, expression: str):
        normalized = normalize_expression(expression)
        result = self.parser.evaluate(normalized)
        return self.repository.create(normalized, result)
