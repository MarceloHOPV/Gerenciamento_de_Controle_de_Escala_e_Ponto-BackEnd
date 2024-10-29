# App/api/employee.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.schemas.employee_schemas import EmployeeCreate  # Use o esquema Pydantic apropriado
from App.crud.employee_crud import fetch_employee_by_name, add_employee
from App.db import get_db
from App.services.auth.auth_main import get_current_user_has_access

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_employee(employee_data: EmployeeCreate, 
                          db: Session = Depends(get_db), 
                          current_user: dict = Depends(get_current_user_has_access)):
    # Verifique se o usuário atual é um gerente
    if current_user.user_type != "managers":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create employees")

    # Use o ID do usuário autenticado como `manager_id`
    manager_id = current_user.id

    # Cria o funcionário
    return await add_employee(employee_data, manager_id=manager_id, db=db)

@router.get("/{name}", status_code=status.HTTP_200_OK)
async def get_employee_by_name(name: str, db: Session = Depends(get_db)):
    return await fetch_employee_by_name(name, db)
