# App/api/employee.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.schemas import EmployeeCreate, TimePunchCreate  # Use o esquema Pydantic apropriado
from App.db import get_db
from App.services.auth.auth_main import get_current_user_has_access
from App.services.employee_services.employee_control import async_get_employee, time_punch  

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/getEmployeById/{employee_id}{manager_id}",status_code=status.HTTP_200_OK)
async def employee_get(employee_id: int, manager_id: int,db: Session = Depends(get_db)):
    return await async_get_employee(db,employee_id,manager_id)

@router.post("/postEmployee/", status_code=status.HTTP_201_CREATED)
async def punch_time(time_punches: TimePunchCreate, db: Session = Depends(get_db)):
    return await time_punch(db=db, employee_id= time_punches.employee_id)