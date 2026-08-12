import asyncio

import pytest
from fastapi import HTTPException

from src.converter import async_converter


def test_async_converter_retorna_valor_convertido(mock_session_get, valid_exchange_response):
    mock_session_get(valid_exchange_response)

    result = asyncio.run(async_converter("USD", "EUR", 100))

    assert result == {"to_currency": "EUR", "converted_value": 92.0}


def test_async_converter_sem_chave_esperada_gera_erro_400(mock_session_get, rate_limited_response):
    mock_session_get(rate_limited_response)

    with pytest.raises(HTTPException) as exc:
        asyncio.run(async_converter("USD", "EUR", 100))

    assert exc.value.status_code == 400


def test_async_converter_com_falha_na_requisicao_gera_erro_400(mocker):
    mocker.patch("aiohttp.ClientSession.get", side_effect=Exception("timeout"))

    with pytest.raises(HTTPException) as exc:
        asyncio.run(async_converter("USD", "EUR", 100))

    assert exc.value.status_code == 400
