# App/api/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.models import UsersModel
from App.schemas import User
from App.crud.user_crud import fetch_user_by_name
import App.crud.user_crud as user_crud
from App.db import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{name}", status_code=status.HTTP_200_OK)
async def get_users_by_name(name: str,db: Session = Depends(get_db)):
    return await fetch_user_by_name(name, db)
