from calculator.domain import calculator


class CalculatorService:
    def add(self, a: float, b: float) -> float:
        return self._validated(calculator.add(a, b))

    def subtract(self, a: float, b: float) -> float:
        return self._validated(calculator.subtract(a, b))

    def multiply(self, a: float, b: float) -> float:
        return self._validated(calculator.multiply(a, b))

    def divide(self, a: float, b: float) -> float:
        return self._validated(calculator.divide(a, b))

    def square_root(self, a: float) -> float:
        return self._validated(calculator.square_root(a))

    def power(self, a: float, b: float) -> float:
        return self._validated(calculator.power(a, b))

    def percent(self, a: float, b: float) -> float:
        return self._validated(calculator.percent(a, b))

    @staticmethod
    def _validated(result: float) -> float:
        calculator.validate_result(result)
        return result
