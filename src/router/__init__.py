# importa a classe usada para criar e agrupar rotas
from fastapi import APIRouter

# importa o router de conversão de moedas com um novo nome (alias)
from .converter_router import router as converter_router

# cria um router principal para agrupar os demais routers do projeto
router = APIRouter()
# adiciona o router de conversão dentro do router principal
router.include_router(converter_router)
