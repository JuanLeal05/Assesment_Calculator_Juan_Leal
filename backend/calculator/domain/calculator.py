import math
from backend.calculator.domain.exceptions import (DivisionByZeroError, NegativeSquareRootError, NonFiniteResultError, ComplexResultError)

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise DivisionByZeroError()
    return a / b

def square_root(a: float) -> float:
    if a < 0:
        raise NegativeSquareRootError()
    return math.sqrt(a)

def power(a: float, b: float) -> float:
    return a ** b

def percent(a: float, b: float) -> float:
    return (a * b) / 100

def validateResult(result: float) -> None:
    if isinstance(result, complex):
        raise ComplexResultError()
    if not math.isfinite(result):
        raise NonFiniteResultError()