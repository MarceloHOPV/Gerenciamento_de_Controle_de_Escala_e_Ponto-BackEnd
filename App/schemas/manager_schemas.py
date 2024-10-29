from pydantic import BaseModel
from typing import List, Optional
from App.utils.common_schemas_Enum import Telefone, Endereco, Genero
from App.schemas.user_schemas import User
from App.schemas.employee_schemas import EmployeeRead

class ManagerCreate(User):
    pass # Classe vazia pois não há campos adicionais

class ManagerRead(ManagerCreate):
    funcionarios: List[EmployeeRead] = []