import pytest

from tests.conftest import API_PREFIX

BINARY_OPERATIONS = ["add", "subtract", "multiply", "divide", "power", "percent"]


# --- Domain errors: 400 with a readable message ---

@pytest.mark.parametrize(
    ("operation", "payload", "detail"),
    [
        ("divide", {"a": 1, "b": 0}, "Division by zero is not allowed."),
        ("divide", {"a": 0, "b": 0}, "Division by zero is not allowed."),
        ("squareRoot", {"a": -4}, "Cannot calculate the square root of a negative number."),
        ("power", {"a": 0, "b": -1}, "Zero cannot be raised to a negative power."),
        ("power", {"a": -8, "b": 0.5}, "The result is a complex number."),
        ("power", {"a": 10, "b": 1000}, "The result is not a finite number."),
        ("multiply", {"a": 1e308, "b": 10}, "The result is not a finite number."),
        ("add", {"a": 1e308, "b": 1e308}, "The result is not a finite number."),
    ],
)
def test_domain_errors_return_400(client, operation, payload, detail):
    response = client.post(f"{API_PREFIX}/{operation}", json=payload)

    assert response.status_code == 400
    assert response.json() == {"detail": detail}


# --- Missing parameters: 422 ---

@pytest.mark.parametrize("operation", BINARY_OPERATIONS)
@pytest.mark.parametrize(
    ("payload", "missing"),
    [({"a": 1}, ["b"]), ({"b": 1}, ["a"]), ({}, ["a", "b"])],
)
def test_binary_operation_missing_fields(client, operation, payload, missing):
    response = client.post(f"{API_PREFIX}/{operation}", json=payload)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert sorted(e["loc"][-1] for e in errors) == missing
    assert all(e["type"] == "missing" for e in errors)


def test_unary_operation_missing_field(client):
    response = client.post(f"{API_PREFIX}/squareRoot", json={})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "a"]


@pytest.mark.parametrize("operation", ["add", "squareRoot"])
def test_missing_body(client, operation):
    response = client.post(f"{API_PREFIX}/{operation}")

    assert response.status_code == 422


# --- Invalid data: 422 ---

@pytest.mark.parametrize(
    "bad_value",
    ["abc", "", None, [1, 2], {"value": 1}, "nan", "inf", "-inf", "Infinity"],
)
def test_invalid_number_is_rejected(client, bad_value):
    response = client.post(f"{API_PREFIX}/add", json={"a": bad_value, "b": 1})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "a"]


@pytest.mark.parametrize("bad_value", ["abc", None, "nan"])
def test_invalid_number_is_rejected_on_unary(client, bad_value):
    response = client.post(f"{API_PREFIX}/squareRoot", json={"a": bad_value})

    assert response.status_code == 422


def test_malformed_json_is_rejected(client):
    response = client.post(
        f"{API_PREFIX}/add",
        content='{"a": 1, "b": ',
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "json_invalid"


def test_body_that_is_not_an_object_is_rejected(client):
    response = client.post(f"{API_PREFIX}/add", json=[1, 2])

    assert response.status_code == 422


# --- Unknown operation / wrong method ---

@pytest.mark.parametrize("operation", ["modulo", "sqrt", "ADD", "factorial"])
def test_unknown_operation_returns_404(client, operation):
    response = client.post(f"{API_PREFIX}/{operation}", json={"a": 1, "b": 2})

    assert response.status_code == 404


def test_unknown_api_version_returns_404(client):
    response = client.post("/api/v2/calculate/add", json={"a": 1, "b": 2})

    assert response.status_code == 404


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_wrong_http_method_returns_405(client, method):
    response = getattr(client, method)(f"{API_PREFIX}/add")

    assert response.status_code == 405
