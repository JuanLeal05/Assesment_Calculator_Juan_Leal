from calculator.domain.exceptions.calculator_error import CalculatorError


class NonFiniteResultError(CalculatorError):
    """Exception raised when a non-finite result is encountered."""
    def __init__(self, message="The result is not a finite number."):
        super().__init__(message)