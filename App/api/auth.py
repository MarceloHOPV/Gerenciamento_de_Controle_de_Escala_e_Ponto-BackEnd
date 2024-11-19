from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.models.__init__ import UsersModel
from App.schemas.__init__ import User, Token
from App.db import get_db
from App.services.auth.auth_main import access_token, Get_user
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from App.services.auth.auth_main import get_current_user_has_access

# Pegando o banco de dados
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Verifica se o usuário existe
    user = db.query(UsersModel).filter(UsersModel.name == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Gera o token de acesso (isso deve retornar apenas o token)
    token_data = await access_token(form_data, db)
    
    # Retorna o token, tipo de token e user_type
    return {
        #"access_token": token_data['access_token'],  # Corrige para pegar a string
        #"token_type": "bearer",
        "user_name": user.name,  # Adiciona o nome do usuário
        "user_type": user.user_type,  # Adiciona o tipo de usuário
        "id_user": user.id  # Troca para id_user
    }
# Endpoint de autenticação
@router.get("/", status_code=status.HTTP_200_OK)
async def authenticate_user(user: dict = Depends(get_current_user_has_access), db: Session = Depends(get_db)):
    return Get_user(user, db)