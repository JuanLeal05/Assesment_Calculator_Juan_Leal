class CalculatorError(Exception):
    """Base class for every domain error raised by the calculator."""
    def __init__(self, message="The calculation could not be performed."):
        self.message = message
        super().__init__(self.message)
