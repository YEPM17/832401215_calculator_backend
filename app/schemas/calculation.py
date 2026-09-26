from pydantic import BaseModel


class CalculationRequest(BaseModel):
    expression: str


class CalculationResponse(BaseModel):
    success: bool = True
    expression: str
    result: float


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
