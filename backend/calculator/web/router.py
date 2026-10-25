from fastapi import APIRouter, Depends, HTTPException
from backend.calculator.web.schema import BinaryOperationRequest, UnaryOperationRequest, OperationResponse
from backend.calculator.application.calculate import CalculatorService

router = APIRouter(prefix="/calculate", tags=["Calculator"])

@router.post("/add", response_model=OperationResponse)
def add(request: BinaryOperationRequest, service: CalculatorService = Depends()):
    result = service.add(request.a, request.b)
    return OperationResponse(result=result)

@router.post("/subtract", response_model=OperationResponse)
def subtract(request: BinaryOperationRequest, service: CalculatorService = Depends()):
    result = service.subtract(request.a, request.b)
    return OperationResponse(result=result)

@router.post("/multiply", response_model=OperationResponse)
def multiply(request: BinaryOperationRequest, service: CalculatorService = Depends()):
    result = service.multiply(request.a, request.b)
    return OperationResponse(result=result)

@router.post("/divide", response_model=OperationResponse)
def divide(request: BinaryOperationRequest, service: CalculatorService = Depends()):
    result = service.divide(request.a, request.b)
    return OperationResponse(result=result)

@router.post("/square_root", response_model=OperationResponse)
def square_root(request: UnaryOperationRequest, service: CalculatorService = Depends()):
    result = service.square_root(request.a)
    return OperationResponse(result=result)

@router.post("/power", response_model=OperationResponse)
def power(request: BinaryOperationRequest, service: CalculatorService = Depends()):
    result = service.power(request.a, request.b)
    return OperationResponse(result=result)

@router.post("/percent", response_model=OperationResponse)
def percent(request: BinaryOperationRequest, service: CalculatorService = Depends()):
    result = service.percent(request.a, request.b)
    return OperationResponse(result=result)
