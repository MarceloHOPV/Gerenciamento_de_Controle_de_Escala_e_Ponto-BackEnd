# Importa todos os modelos de cada arquivo
from App.db import Base, engine
from .user_models import UsersModel
from .employee_model import EmployeesModel
from .manager_model import ManagersModel
from .time_tracking_models import BankHours, WorkSchedule, TimePunches

# Exporta os modelos para serem acessados ao importar o módulo `models`
__all__ = [
    "UsersModel",
    "EmployeesModel",
    "ManagersModel",
    "BankHours",
    "WorkSchedule",
    "TimePunches"
]
