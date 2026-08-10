# path parameter
# query parameter ( /url?to_currencies=USB, EUR, GBP&price=5.55) ele filtra
# body parameter

# código para chamar a função que faz a conversão  monetaria e cria a rota
# importa a classe usada para criar rotas
from fastapi import APIRouter
# importa as funções de conversão (síncrona e assíncrona)
from src.converter import sync_converter, async_converter
# importa a função que executa várias tarefas assíncronas em paralelo
from asyncio import gather

# cria o router com o prefixo "/converter" para todas as rotas deste arquivo
router = APIRouter(prefix="/converter")

# rota síncrona: converte um preço de uma moeda para uma ou mais moedas
@router.get("/{from_currency}")
def converter(from_currency: str, to_currencies: str, price: float):
     # separa a string de moedas de destino em uma lista, usando a vírgula
     to_currencies = to_currencies.split(',')
     resultado = [] # lista de moedas

     # percorre cada moeda de destino informada
     for currency in to_currencies:
        # chama a conversão síncrona para a moeda atual
        response = sync_converter(from_currency=from_currency, to_currency=currency, price=price)
        # guarda o resultado na lista
        resultado.append(response)

     # retorna a lista com os valores convertidos
     return resultado


# rota assíncrona: faz as conversões em paralelo, uma para cada moeda de destino
@router.get("/async/{from_currency}")
async def async_converter_router(from_currency: str, to_currencies: str, price: float):
     # separa a string de moedas de destino em uma lista, usando a vírgula
     to_currencies = to_currencies.split(',')

     coroutines = []
     # resultado = [] # lista de moedas

     # percorre cada moeda de destino informada
     for currency in to_currencies:
        # cria a corrotina de conversão para a moeda atual (ainda não executada)
        coroutine = async_converter(from_currency=from_currency, to_currency=currency, price=price)
        # guarda a corrotina na lista para executar depois
        coroutines.append(coroutine)

     # executa todas as corrotinas em paralelo e espera todas terminarem
     result = await gather(*coroutines)

     # retorna a lista com os valores convertidos
     return result
