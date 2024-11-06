#Import-tabela
from App.models import UsersModel
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from App.db import Base
from App.utils.common_schemas_Enum import Genero
#Import-CRUD
from sqlalchemy.orm import Session
from App.utils.employee_utils import merge_adress
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from App.schemas import EmployeeUpdate, EmployeeCreate

#*********************Employee******************************#
class EmployeesModel(UsersModel):
    __tablename__ = 'employees'
    id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)
    genero = Column(Enum(Genero), index=True)
    cpf = Column(String, index=True)
    salario = Column(Float, index=True)
    endereco = Column(String, index=True)
    DDD = Column(String, index=True)
    telefone = Column(String, index=True)

    manager_id = Column(Integer, ForeignKey("managers.id"))
    manager = relationship("ManagersModel", back_populates="employees", foreign_keys=[manager_id])

    bank_hours = relationship("BankHours", back_populates="employee")
    work_schedule = relationship("WorkSchedule", back_populates="employee")
    time_punches = relationship("TimePunches", back_populates="employee")
    
    __mapper_args__ = {
        'polymorphic_identity': 'employee'
    }

