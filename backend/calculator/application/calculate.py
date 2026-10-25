import math
from backend.calculator.domain import calculator

class CalculatorService:
    def add(self, a: float, b: float) -> float:
        result = calculator.add(a, b)
        calculator.validateResult(result)
        return result

    def subtract(self, a: float, b: float) -> float:
        result = calculator.subtract(a, b)
        calculator.validateResult(result)
        return result

    def multiply(self, a: float, b: float) -> float:
        result = calculator.multiply(a, b)
        calculator.validateResult(result)
        return result

    def divide(self, a: float, b: float) -> float:
        result = calculator.divide(a, b)
        calculator.validateResult(result)
        return result

    def square_root(self, a: float) -> float:
        result = calculator.square_root(a)
        calculator.validateResult(result)
        return result

    def power(self, a: float, b: float) -> float:
        result = calculator.power(a, b)
        calculator.validateResult(result)
        return result

    def percent(self, a: float, b: float) -> float:
        result = calculator.percent(a, b)
        calculator.validateResult(result)
        return result

