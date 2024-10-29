from pydantic import BaseModel
from typing import List, Optional
from App.utils.common_schemas_Enum import Telefone, Endereco, Genero
from App.schemas.user_schemas import User
#*********************Employee******************************#

class EmployeeCreate(User):
    salario_publico: float
    genero_publico: Genero
    telefone_publico: Telefone
    endereco_publico: Endereco

class EmployeeRead(EmployeeCreate):
    id: int