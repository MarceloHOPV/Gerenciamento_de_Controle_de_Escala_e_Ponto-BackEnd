from sqlalchemy.orm import Session
from App.db import SessionLocal
from typing import Annotated
from fastapi import HTTPException, Depends
from App.models import EmployeesModel, ManagersModel
from App.schemas import EmployeeCreate, EmployeeRead

async def add_employee(employee: EmployeeCreate,manager_id: int, db: Session):
    # Verifica se o manager_id existe no banco
    manager = db.query(ManagersModel).filter(ManagersModel.id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    # Cria o novo funcionário
    db_employee = EmployeesModel(name=employee.name,
                                email=employee.email,
                                hashed_password=employee.hashed_password,
                                is_active=employee.is_active,
                                user_type="employee",
                                genero=employee.genero,
                                cpf=employee.cpf,
                                salario=employee.salario,
                                manager_id=employee.manager_id)
    # Adiciona o funcionário a fila de commit
    db.add(db_employee)
    # Comita o funcionário
    db.commit()
    # Atualiza o objeto db_employee
    db.refresh(db_employee)
    return db_employee


async def fetch_employee_by_name(name: str, db: Session):
    employee = db.query(EmployeesModel).filter(
        EmployeesModel.name == name,
        EmployeesModel.user_type == "employee"  # Certifica-se de que o tipo é 'employee'
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

async def get_password(question_id: int, db: Session):
    return