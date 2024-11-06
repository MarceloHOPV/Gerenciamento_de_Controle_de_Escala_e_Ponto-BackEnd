from sqlalchemy.orm import Session
from App.db import SessionLocal
from typing import Annotated
from fastapi import HTTPException, Depends
from App.models import ManagersModel, UsersModel
from App.schemas import ManagerCreate, ManagerRead
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def fetch_manager_by_name(name: str, db: Session):
    manager = db.query(ManagersModel).filter(ManagersModel.name == name).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    return manager