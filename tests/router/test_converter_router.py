from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_async_converter_route_retorna_conversoes(mocker):
    mocker.patch(
        "src.router.converter_router.async_converter",
        return_value={"to_currency": "EUR", "converted_value": 92.0},
    )

    response = client.get("/converter/async/USD?to_currencies=EUR&price=100")

    assert response.status_code == 200
    assert response.json() == [{"to_currency": "EUR", "converted_value": 92.0}]


def test_async_converter_route_body_retorna_conversoes(mocker):
    mocker.patch(
        "src.router.converter_router.async_converter",
        return_value={"to_currency": "EUR", "converted_value": 92.0},
    )

    response = client.request(
        "GET",
        "/converter/async/body/USD",
        json={"price": 100, "to_currencies": ["EUR"]},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "success",
        "data": [{"to_currency": "EUR", "converted_value": 92.0}],
    }


def test_async_converter_route_body_rejeita_moeda_invalida():
    response = client.request(
        "GET",
        "/converter/async/body/USD",
        json={"price": 100, "to_currencies": ["EURO"]},
    )

    assert response.status_code == 422
