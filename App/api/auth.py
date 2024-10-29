from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.models.__init__ import UsersModel
from App.schemas.__init__ import User, Token
from App.crud.user_crud import Get_user
from App.db import get_db
from App.services.auth.auth_main import access_token
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from App.services.auth.auth_main import get_current_user_has_access

# Pegando o banco de dados
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return await access_token(form_data, db)

# Endpoint de autenticação
@router.get("/", status_code=status.HTTP_200_OK)
async def authenticate_user(user: dict = Depends(get_current_user_has_access), db: Session = Depends(get_db)):
    return Get_user(user, db)

