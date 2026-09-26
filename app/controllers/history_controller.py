from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.history_repository import HistoryRepository
from app.schemas.calculation import ErrorResponse
from app.schemas.history import HistoryItem, HistoryResponse

router = APIRouter(prefix="/api/history", tags=["history"])


def get_repository(db: Session = Depends(get_db)) -> HistoryRepository:
    return HistoryRepository(db)


@router.get("", response_model=HistoryResponse)
def list_history(repository: HistoryRepository = Depends(get_repository)):
    items = [
        HistoryItem(
            id=record.id,
            expression=record.expression,
            result=float(record.result),
            created_at=record.created_at,
        )
        for record in repository.list_all()
    ]
    return HistoryResponse(items=items)


@router.delete(
    "/{record_id}",
    status_code=204,
    responses={404: {"model": ErrorResponse}},
)
def delete_history(
    record_id: int,
    repository: HistoryRepository = Depends(get_repository),
):
    if not repository.delete(record_id):
        raise HTTPException(
            status_code=404,
            detail={"success": False, "message": "History record not found"},
        )
    return Response(status_code=204)


@router.delete("", status_code=204)
def clear_history(repository: HistoryRepository = Depends(get_repository)):
    repository.delete_all()
    return Response(status_code=204)
