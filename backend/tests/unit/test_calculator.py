import math

import pytest

from calculator.domain import calculator
from calculator.domain.exceptions import (
    CalculatorError,
    ComplexResultError,
    DivisionByZeroError,
    NegativeSquareRootError,
    NonFiniteResultError,
)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(2, 3, 5), (-2, -3, -5), (-2, 3, 1), (0, 0, 0), (0.1, 0.2, 0.3)],
)
def test_add(a, b, expected):
    assert calculator.add(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(5, 3, 2), (3, 5, -2), (-2, -3, 1), (0, 0, 0), (0.3, 0.1, 0.2)],
)
def test_subtract(a, b, expected):
    assert calculator.subtract(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(2, 3, 6), (-2, 3, -6), (-2, -3, 6), (5, 0, 0), (0.5, 0.5, 0.25)],
)
def test_multiply(a, b, expected):
    assert calculator.multiply(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(6, 3, 2), (-6, 3, -2), (-6, -3, 2), (0, 5, 0), (1, 3, 1 / 3), (7, 2, 3.5)],
)
def test_divide(a, b, expected):
    assert calculator.divide(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a", [1, 0, -1, 0.0, -0.0])
def test_divide_by_zero_raises(a):
    with pytest.raises(DivisionByZeroError):
        calculator.divide(a, 0)


@pytest.mark.parametrize(
    ("a", "expected"),
    [(0, 0), (1, 1), (4, 2), (2, math.sqrt(2)), (0.25, 0.5)],
)
def test_square_root(a, expected):
    assert calculator.square_root(a) == pytest.approx(expected)


@pytest.mark.parametrize("a", [-1, -0.0001, -100])
def test_square_root_of_negative_raises(a):
    with pytest.raises(NegativeSquareRootError):
        calculator.square_root(a)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(2, 3, 8), (2, 0, 1), (0, 0, 1), (2, -1, 0.5), (9, 0.5, 3), (-2, 3, -8), (-2, 2, 4)],
)
def test_power(a, b, expected):
    assert calculator.power(a, b) == pytest.approx(expected)


def test_power_of_zero_to_negative_exponent_raises():
    with pytest.raises(DivisionByZeroError):
        calculator.power(0, -1)


def test_power_overflow_raises():
    with pytest.raises(NonFiniteResultError):
        calculator.power(10.0, 1000)


def test_power_of_negative_base_to_fraction_returns_complex():
    # The domain returns Python's raw result; validate_result is what rejects it.
    assert isinstance(calculator.power(-8, 0.5), complex)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(200, 15, 30), (50, 50, 25), (100, 0, 0), (-200, 10, -20), (80, 12.5, 10)],
)
def test_percent(a, b, expected):
    assert calculator.percent(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("value", [0, 1.5, -1e308, 1e308])
def test_validate_result_accepts_finite_numbers(value):
    calculator.validate_result(value)


@pytest.mark.parametrize("value", [math.inf, -math.inf, math.nan])
def test_validate_result_rejects_non_finite(value):
    with pytest.raises(NonFiniteResultError):
        calculator.validate_result(value)


def test_validate_result_rejects_complex():
    with pytest.raises(ComplexResultError):
        calculator.validate_result(1 + 2j)


@pytest.mark.parametrize(
    "error",
    [ComplexResultError, DivisionByZeroError, NegativeSquareRootError, NonFiniteResultError],
)
def test_domain_errors_share_base_and_have_message(error):
    exc = error()
    assert isinstance(exc, CalculatorError)
    assert exc.message
    assert str(exc) == exc.message
