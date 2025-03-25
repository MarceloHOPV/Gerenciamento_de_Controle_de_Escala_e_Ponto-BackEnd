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
    salario: Optional[float] = None
    genero: Optional[Genero] = None
    telefone: Optional[Telefone] = None
    endereco: Optional[Endereco] = None

class EmployeeInfo(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    genero: str
    cpf: str
    salario: float
    endereco: str
    telefone: str
    model_config = {
        "from_attributes": True
    }

class EmployeeSalary(BaseModel):
    name: str
    salario: float
    model_config = {
        "from_attributes": True
    }

class EmployeeListItem(BaseModel):
    name: str
    cpf: str
    email: str
    model_config = {
        "from_attributes": True
    }