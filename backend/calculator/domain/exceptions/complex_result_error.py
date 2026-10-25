class ComplexResultError(Exception):
    def __init__(self, message="The result is a complex number."):
        self.message = message
        super().__init__(self.message)