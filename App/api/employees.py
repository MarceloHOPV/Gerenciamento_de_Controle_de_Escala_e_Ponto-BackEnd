# App/api/employee.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.schemas.employee_schemas import EmployeeCreate  # Use o esquema Pydantic apropriado
from App.db import get_db
from App.services.auth.auth_main import get_current_user_has_access

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/{name}", status_code=status.HTTP_200_OK)
async def get_employee_by_name(name: str, db: Session = Depends(get_db)):
    return await fetch_employee_by_name(name, db)
