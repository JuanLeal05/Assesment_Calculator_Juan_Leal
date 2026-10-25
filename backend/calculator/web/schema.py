from pydantic import BaseModel

class BinaryCalculationRequest(BaseModel):
    a: float
    b: float

class UnaryCalculationRequest(BaseModel):
    a: float

class CalculationResponse(BaseModel):
    result: float