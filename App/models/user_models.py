from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from App.db import Base
from App.utils.common_schemas_Enum import Genero

class UsersModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String, index=False)  # Remove o índice para hashed_password
    is_active = Column(Boolean, index=True)
    user_type = Column(String) 
    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': user_type
    }

class EmployeesModel(UsersModel):
    __tablename__ = 'employees'
    id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)
    genero = Column(Enum(Genero), index=True)
    cpf = Column(String, index=True)
    salario = Column(Float, index=True)

    manager_id = Column(Integer, ForeignKey("managers.id"))
    manager = relationship("ManagersModel", back_populates="employees", foreign_keys=[manager_id])

    bank_hours = relationship("BankHours", back_populates="employee")
    work_schedule = relationship("WorkSchedule", back_populates="employee")
    time_punches = relationship("TimePunches", back_populates="employee")
    
    __mapper_args__ = {
        'polymorphic_identity': 'employees'
    }

class ManagersModel(UsersModel):
    __tablename__ = 'managers'
    id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)
    employees = relationship("EmployeesModel", back_populates="manager", foreign_keys=[EmployeesModel.manager_id])

    __mapper_args__ = {
        'polymorphic_identity': 'managers' 
    }

