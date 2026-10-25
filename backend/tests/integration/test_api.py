import pytest

from tests.conftest import API_PREFIX


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize(
    ("operation", "payload", "expected"),
    [
        ("add", {"a": 2, "b": 3}, 5),
        ("add", {"a": -1.5, "b": 0.5}, -1),
        ("subtract", {"a": 10, "b": 4}, 6),
        ("multiply", {"a": 3, "b": -4}, -12),
        ("divide", {"a": 7, "b": 2}, 3.5),
        ("squareRoot", {"a": 81}, 9),
        ("power", {"a": 2, "b": 8}, 256),
        ("power", {"a": 4, "b": -0.5}, 0.5),
        ("percent", {"a": 200, "b": 15}, 30),
    ],
)
def test_operation_returns_result(client, operation, payload, expected):
    response = client.post(f"{API_PREFIX}/{operation}", json=payload)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"result": pytest.approx(expected)}


def test_numeric_strings_are_coerced(client):
    response = client.post(f"{API_PREFIX}/add", json={"a": "2", "b": "3.5"})

    assert response.status_code == 200
    assert response.json() == {"result": 5.5}


def test_extra_fields_are_ignored(client):
    response = client.post(f"{API_PREFIX}/squareRoot", json={"a": 9, "b": 100})

    assert response.status_code == 200
    assert response.json() == {"result": 3}


def test_cors_preflight_allows_frontend_origin(client):
    response = client.options(
        f"{API_PREFIX}/add",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_rejects_unknown_origin(client):
    response = client.options(
        f"{API_PREFIX}/add",
        headers={
            "Origin": "http://evil.example",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert "access-control-allow-origin" not in response.headers


def test_openapi_lists_every_operation(client):
    paths = client.get("/openapi.json").json()["paths"]

    for operation in ("add", "subtract", "multiply", "divide", "squareRoot", "power", "percent"):
        assert f"{API_PREFIX}/{operation}" in paths
