"""
      {
            "Realtime Currency Exchange Rate": {
                "1. From_Currency Code": "USD",
                "2. From_Currency Name": "United States Dollar",
                "3. To_Currency Code": "JPY",
                "4. To_Currency Name": "Japanese Yen",
                "5. Exchange Rate": "158.45695667",
                "6. Last Refreshed": "2026-08-06 19:45:49",
                "7. Time Zone": "UTC",
                "8. Bid Price": "158.45456397",
                "9. Ask Price": "158.45856501"
            }
}
"""

# biblioteca para fazer requisições HTTP de forma assíncrona (não bloqueante)
import aiohttp
# função para ler variáveis de ambiente do sistema
from os import getenv
# função que carrega as variáveis do arquivo .env para o ambiente
from dotenv import load_dotenv
# exceção do FastAPI usada para retornar erros HTTP customizados
from fastapi import HTTPException

# carrega as variáveis definidas no arquivo .env
load_dotenv()

# lê a chave de acesso da API AlphaVantage a partir das variáveis de ambiente
ALPHAVANTAGE_APIKEY = getenv('ALPHAVANTAGE_APIKEY')

# versão assíncrona da função de conversão, usada para várias conversões em paralelo
async def async_converter(from_currency: str, to_currency: str, price: float):
    # monta a url da API informando moeda de origem, moeda de destino e a chave de acesso
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHAVANTAGE_APIKEY}"

    try:
        # response = requests.get(url=url) # verifica se o dicionário está certo com a url
        # abre uma sessão HTTP assíncrona
        async with aiohttp.ClientSession() as session:
            # faz a requisição GET sem bloquear a execução
            async with session.get(url=url) as response:
                # espera e converte a resposta em um dicionário Python
                data = await response.json()

    except Exception as error:
        # se a requisição falhar, retorna um erro HTTP 400 com o motivo
        raise HTTPException(status_code=400, detail=error)
    
    if "Information" in data:
        print(f"{data['Information']}\n")
    if "Realtime Currency Exchange Rate" not in data:  # Analisa se o json contém o tema esperado
        # se a chave esperada não existir na resposta, retorna erro HTTP 400
        raise HTTPException(status_code=400, detail="Realtime Currency Exchange Rate")

    exchange_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]) # pega o valor da moeda estrageira

    return price * exchange_rate # faz o calculo entre a moeda estrageira com o valor da moeda selecionada