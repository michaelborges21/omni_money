# importa a classe FastAPI, que cria a aplicação web
from fastapi import FastAPI
# importa o router de conversão de moedas definido em outro arquivo
from src.router.converter_router import router

# cria a instância principal da aplicação
app = FastAPI()
# registra as rotas do router de conversão na aplicação
app.include_router(router=router)

# define a rota raiz ("/") que responde a requisições GET
@app.get("/")
def hello_world():
    # retorna uma mensagem de boas-vindas
    return "Bem vindo a Raíz"