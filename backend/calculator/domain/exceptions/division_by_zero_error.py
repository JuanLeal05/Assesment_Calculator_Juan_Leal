from calculator.domain.exceptions.calculator_error import CalculatorError


class DivisionByZeroError(CalculatorError):
    def __init__(self, message="Division by zero is not allowed."):
        super().__init__(message)