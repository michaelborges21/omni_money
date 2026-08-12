from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def valid_exchange_response():
    return {
        "Realtime Currency Exchange Rate": {
            "1. From_Currency Code": "USD",
            "3. To_Currency Code": "EUR",
            "5. Exchange Rate": "0.92",
        }
    }


@pytest.fixture
def rate_limited_response():
    return {"Information": "limite de requisições excedido"}


@pytest.fixture
def mock_session_get(mocker):
    def _mock(json_data):
        response = AsyncMock()
        response.json.return_value = json_data

        session_get = MagicMock()
        session_get.__aenter__.return_value = response
        session_get.__aexit__.return_value = None

        mocker.patch("aiohttp.ClientSession.get", return_value=session_get)

    return _mock
