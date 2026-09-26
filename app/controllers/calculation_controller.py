from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.history_repository import HistoryRepository
from app.schemas.calculation import (
    CalculationRequest,
    CalculationResponse,
    ErrorResponse,
)
from app.services.calculation_service import CalculationService
from app.services.expression_parser import ExpressionError

router = APIRouter(prefix="/api", tags=["calculation"])


def get_service(db: Session = Depends(get_db)) -> CalculationService:
    return CalculationService(HistoryRepository(db))


@router.post(
    "/calculate",
    response_model=CalculationResponse,
    responses={400: {"model": ErrorResponse}},
)
def calculate(
    payload: CalculationRequest,
    service: CalculationService = Depends(get_service),
):
    try:
        record = service.calculate(payload.expression)
    except ExpressionError as error:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "message": str(error)},
        ) from error

    return CalculationResponse(
        expression=record.expression,
        result=float(record.result),
    )
