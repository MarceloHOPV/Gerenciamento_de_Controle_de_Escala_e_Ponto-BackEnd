# Importa todos os modelos de cada arquivo
from App.db import Base, engine
from .user_models import UsersModel, EmployeesModel, ManagersModel
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
