# App/api/employee.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.models import EmployeesModel, ManagersModel
import App.schemas.employee_schemas as employee_schemas
from App.crud.employee_crud import fetch_employee_by_name
from App.db import get_db

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/{name}", status_code=status.HTTP_200_OK)
async def get_employee_by_name(name: str,db: Session = Depends(get_db)):
    return await fetch_employee_by_name(name,db)
