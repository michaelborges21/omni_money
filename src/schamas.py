"""
Passagem de parâmetro através do body (  body parameter )
Ex:
   {
      "price":123,
      "to_currencies": ['USB','GBP']
   }
"""

import re

from pydantic import BaseModel, Field, validator
from typing import List

# schema do body da rota v2: valida o preço (deve ser positivo) e a lista de moedas de destino
class ConverterInput(BaseModel):
   price: float = Field(gt=0)
   to_currencies: List[str]

   # valida que cada moeda em "to_currencies" segue o padrão de 3 letras maiúsculas (ex: USD, EUR)
   @validator('to_currencies')
   def validate_to_currencies(cls, value):
      for currency in value:
         if not re.match('^[A-Z]{3}$', currency):
            raise ValueError(f'Invalid currency {currency}')
      return value


# schema da resposta da rota v2: mensagem de status + lista com o resultado de cada conversão
class ConverterOutput(BaseModel):
   message: str
   data: List[dict]
