import pytest

from calculator.application.calculate import CalculatorService
from calculator.domain.exceptions import (
    ComplexResultError,
    DivisionByZeroError,
    NegativeSquareRootError,
    NonFiniteResultError,
)


@pytest.fixture
def service():
    return CalculatorService()


@pytest.mark.parametrize(
    ("operation", "args", "expected"),
    [
        ("add", (2, 3), 5),
        ("subtract", (5, 3), 2),
        ("multiply", (4, 2.5), 10),
        ("divide", (9, 3), 3),
        ("square_root", (16,), 4),
        ("power", (2, 10), 1024),
        ("percent", (200, 15), 30),
    ],
)
def test_service_returns_domain_result(service, operation, args, expected):
    assert getattr(service, operation)(*args) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("operation", "args", "error"),
    [
        ("add", (1e308, 1e308), NonFiniteResultError),
        ("subtract", (-1e308, 1e308), NonFiniteResultError),
        ("multiply", (1e308, 10), NonFiniteResultError),
        ("divide", (1e308, 1e-308), NonFiniteResultError),
        ("percent", (1e308, 1e308), NonFiniteResultError),
        ("power", (10.0, 1000), NonFiniteResultError),
        ("power", (-8, 0.5), ComplexResultError),
        ("power", (0, -1), DivisionByZeroError),
        ("divide", (1, 0), DivisionByZeroError),
        ("square_root", (-4,), NegativeSquareRootError),
    ],
)
def test_service_raises_domain_errors(service, operation, args, error):
    with pytest.raises(error):
        getattr(service, operation)(*args)
