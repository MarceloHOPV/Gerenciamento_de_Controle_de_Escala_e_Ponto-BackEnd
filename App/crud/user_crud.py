from sqlalchemy.orm import Session
from App.db import SessionLocal
from typing import Annotated
from fastapi import HTTPException, Depends
from App.models import UsersModel
from App.schemas import User


async def Get_user(user: None, db: Session):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return {"User": user}

async def fetch_user_by_name(name: str, db: Session):
    user = db.query(UsersModel).filter(UsersModel.name == name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user