from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum
#**************************************************************#
# Tipos / Enumerações

class Genero(str, Enum):
    masculino = 'masculino'
    feminino = 'feminino'

class Telefone(BaseModel):
    ddd: int
    numero: int

class Endereco(BaseModel):
    rua: str
    numero: int
    bairro: str
    cidade: str
    estado: str
    cep: int
    complemento: Optional[str] = None

class Hora(BaseModel):
    hora: int
    minuto: int

class Dia_semana(str, Enum):
    segunda = "Segunda-feira"
    terca = "Terça-feira"
    quarta = "Quarta-feira"
    quinta = "Quinta-feira"
    sexta = "Sexta-feira"
    sabado = "Sábado"
    domingo = "Domingo"

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"