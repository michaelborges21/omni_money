# path parameter
# query parameter ( /url?to_currencies=USB, EUR, GBP&price=5.55) ele filtra
# body parameter

# código para chamar a função que faz a conversão  monetaria e cria a rota
# importa a classe usada para criar rotas
from fastapi import APIRouter, Path, Query
# importa as funções de conversão (síncrona e assíncrona)
from src.converter import async_converter
# importa a função que executa várias tarefas assíncronas em paralelo
from asyncio import gather

# cria o router com o prefixo "/converter" para todas as rotas deste arquivo
router = APIRouter(prefix="/converter")

# rota assíncrona: faz as conversões em paralelo, uma para cada moeda de destino
@router.get("/async/{from_currency}")
async def async_converter_router(
                                  from_currency: str = Path(max_length=3, regex='^[A-Z]{3}$'), 
                                  to_currencies: str = Query(max_length=50, regex='^[A-Z]{3}(,[A-Z]{3})*$'), 
                                  price: float = Query(gt=0)
                               ):

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
