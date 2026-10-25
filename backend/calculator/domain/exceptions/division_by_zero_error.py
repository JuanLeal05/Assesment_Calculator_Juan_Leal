class DivisionByZeroError(Exception):
    def __init__(self, message="Division by zero is not allowed."):
        self.message = message
        super().__init__(self.message)