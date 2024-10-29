from sqlalchemy.orm import Session
from App.db import SessionLocal
from typing import Annotated
from fastapi import HTTPException, Depends
from App.models import EmployeesModel, ManagersModel
from App.schemas import EmployeeCreate, EmployeeRead
from App.utils.employee_utils import merge_adress
import logging
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def add_employee(employee_data: EmployeeCreate, manager_id: int, db: Session):
    try:
        # Verifica se já existe um funcionário com o mesmo email
        existing_employee = db.query(EmployeesModel).filter(EmployeesModel.email == employee_data.email).first()
        if existing_employee:
            raise HTTPException(status_code=400, detail="Employee with this email already exists")

        # Cria uma nova instância de EmployeesModel com o manager_id do gerente autenticado
        db_employee = EmployeesModel(
            name=employee_data.name,
            email=employee_data.email,
            hashed_password=bcrypt_context.hash(employee_data.hashed_password),  # Certifique-se de que esta senha está sendo hasheada antes
            is_active=employee_data.is_active,
            user_type="employee",
            genero=employee_data.genero,
            cpf=employee_data.cpf,
            salario=employee_data.salario,
            manager_id=manager_id,  # Usa o ID do gerente autenticado
            DDD=employee_data.telefone.ddd,
            telefone=employee_data.telefone.numero,
            endereco=merge_adress(employee_data.endereco)
        )

        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee

    except Exception as e:
        logging.error(f"Erro ao adicionar funcionário: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


    except Exception as e:
        logging.error(f"Erro ao adicionar funcionário: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def fetch_employee_by_name(name: str, db: Session):
    employee = db.query(EmployeesModel).filter(
        EmployeesModel.name == name,
        EmployeesModel.user_type == "employee"  # Certifica-se de que o tipo é 'employee'
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
