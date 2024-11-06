# Importa os schemas de cada arquivo
from .user_schemas import User
from .employee_schemas import EmployeeCreate, EmployeeRead, EmployeeUpdate
from .manager_schemas import ManagerCreate, ManagerRead
from .time_tracking_schemas import BankHours, WorkSchedule, TimePunches
from .token_schemas import TokenData, Token

# Define os schemas que serão exportados ao importar `schemas`
__all__ = [
    "User",
    "EmployeeCreate",
    "EmployeeUpdate",
    "EmployeeRead",
    "ManagerCreate",
    "ManagerRead",
    "BankHours",
    "WorkSchedule",
    "TimePunches",
    "TokenData",
    "Token"
]