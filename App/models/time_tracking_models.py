from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, Time
from sqlalchemy.orm import relationship
from App.db import Base
from App.utils.common_schemas_Enum import Dia_semana

class BankHours(Base):
    __tablename__ = 'bank_hours'
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    hours = Column(Integer)
    minutes = Column(Integer)

    # Relacionamento para acessar o EmployeesModel diretamente
    employee = relationship("EmployeesModel", back_populates="bank_hours")

class WorkSchedule(Base):
    __tablename__ = 'work_schedules'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    day_of_week = Column(Enum(Dia_semana))
    start_time = Column(Time)  # Hora de início
    end_time = Column(Time)    # Hora de término

    employee = relationship("EmployeesModel", back_populates="work_schedule")

class TimePunches(Base):
    __tablename__ = 'time_punches'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    punch_time = Column(DateTime)  # Data e hora exata do ponto batido

    employee = relationship("EmployeesModel", back_populates="time_punches")
