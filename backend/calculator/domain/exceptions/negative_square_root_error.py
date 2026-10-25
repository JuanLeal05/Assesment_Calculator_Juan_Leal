from calculator.domain.exceptions.calculator_error import CalculatorError


class NegativeSquareRootError(CalculatorError):
    """Exception raised when trying to calculate the square root of a negative number."""
    def __init__(self, message="Cannot calculate the square root of a negative number."):
        super().__init__(message)