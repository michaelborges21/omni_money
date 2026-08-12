# Testes

Resumo do que foi feito na suíte de testes do projeto.

## Estrutura

```
tests/
├── conftest.py                    # fixtures compartilhadas
├── test_converter.py              # testes da função de conversão (src/converter.py)
└── router/
    └── test_converter_router.py   # testes das rotas HTTP (src/router/converter_router.py)
```

## Configuração

- `testpaths = ["tests"]` foi adicionado em `pyproject.toml` para o pytest achar os testes automaticamente.
- Dependências de teste: `pytest`, `pytest-mock` (fixture `mocker`), `httpx` (usado pelo `TestClient` do FastAPI).

## Fixtures (`conftest.py`)

- `valid_exchange_response`: JSON de exemplo simulando uma resposta válida da API AlphaVantage.
- `rate_limited_response`: JSON simulando resposta de limite de requisições excedido (sem a chave `"Realtime Currency Exchange Rate"`).
- `mock_session_get`: substitui `aiohttp.ClientSession.get` por um mock assíncrono, permitindo controlar o JSON retornado sem fazer chamada HTTP real.

## `test_converter.py` — testa `async_converter`

| Teste | O que valida |
|---|---|
| `test_async_converter_retorna_valor_convertido` | Com uma resposta válida da API, o valor convertido é calculado corretamente. |
| `test_async_converter_sem_chave_esperada_gera_erro_400` | Se a resposta não tiver a chave `"Realtime Currency Exchange Rate"` (ex: limite excedido), a função levanta `HTTPException(400)`. |
| `test_async_converter_com_falha_na_requisicao_gera_erro_400` | Se a requisição HTTP falhar (exceção/timeout), a função levanta `HTTPException(400)`. |

## `test_converter_router.py` — testa as rotas

Usa `TestClient` do FastAPI sobre a `app` de `main.py`, com `async_converter` mockado (não testa a API externa, só o comportamento da rota).

| Teste | O que valida |
|---|---|
| `test_async_converter_route_retorna_conversoes` | `GET /converter/async/{from_currency}` com `to_currencies` e `price` via query params retorna 200 e a lista de conversões. |
| `test_async_converter_route_body_retorna_conversoes` | `GET /converter/async/body/{from_currency}` recebendo `to_currencies` e `price` pelo body retorna 200 e a resposta no formato `{"message": "success", "data": [...]}`. |
| `test_async_converter_route_body_rejeita_moeda_invalida` | Envio de uma moeda inválida (`"EURO"`, 4 letras) no body é rejeitado com 422 pela validação do Pydantic. |

## Rodando os testes

```bash
python -m pytest -v
```

Estado atual: 6 testes, todos passando.
