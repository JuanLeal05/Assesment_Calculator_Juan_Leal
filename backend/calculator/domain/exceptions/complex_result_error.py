from calculator.domain.exceptions.calculator_error import CalculatorError


class ComplexResultError(CalculatorError):
    def __init__(self, message="The result is a complex number."):
        super().__init__(message)