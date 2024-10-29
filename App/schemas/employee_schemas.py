from pydantic import BaseModel
from typing import List, Optional
from App.utils.common_schemas_Enum import Telefone, Endereco, Genero
from App.schemas.user_schemas import User
#*********************Employee******************************#

class EmployeeCreate(User):
    salario: float
    genero: Genero
    telefone: Telefone
    endereco: Endereco
    manager_id: Optional[int]

class EmployeeRead(EmployeeCreate):
    id: int

    