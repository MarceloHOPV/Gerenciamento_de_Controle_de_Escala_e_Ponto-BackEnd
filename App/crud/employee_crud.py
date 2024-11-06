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


async def fetch_employee_by_name(name: str, db: Session):
    employee = db.query(EmployeesModel).filter(EmployeesModel.name == name).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
