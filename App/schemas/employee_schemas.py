from pydantic import BaseModel
from typing import List, Optional
from App.utils.common_schemas_Enum import Telefone, Endereco, Genero
from App.schemas.user_schemas import User, UserUpdate
#*********************Employee******************************#

class EmployeeCreate(User):
    salario: float
    genero: Genero
    telefone: Telefone
    endereco: Endereco
    manager_id: int

class EmployeeRead(EmployeeCreate):
    id: int

class EmployeeUpdate(UserUpdate):
    salario: Optional[float]
    genero: Optional[Genero]
    telefone: Optional[Telefone]
    endereco: Optional[Endereco]
