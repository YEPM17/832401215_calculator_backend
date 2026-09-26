from datetime import datetime

from pydantic import BaseModel


class HistoryItem(BaseModel):
    id: int
    expression: str
    result: float
    created_at: datetime


class HistoryResponse(BaseModel):
    success: bool = True
    items: list[HistoryItem]
