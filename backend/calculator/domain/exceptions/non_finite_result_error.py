class NonFiniteResultError(Exception):
    """Exception raised when a non-finite result is encountered."""
    def __init__(self, message="The result is not a finite number."):
        self.message = message
        super().__init__(self.message)