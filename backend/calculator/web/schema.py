from pydantic import BaseModel, ConfigDict

class BinaryOperationRequest(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False)

    a: float
    b: float

class UnaryOperationRequest(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False)

    a: float

class OperationResponse(BaseModel):
    result: float