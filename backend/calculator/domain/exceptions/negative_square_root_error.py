class NegativeSquareRootError(Exception):
    """Exception raised when trying to calculate the square root of a negative number."""
    def __init__(self, message="Cannot calculate the square root of a negative number."):
        self.message = message
        super().__init__(self.message)