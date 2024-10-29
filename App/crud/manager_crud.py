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

async def add_manager(manager_data: ManagerCreate, db: Session):
    try:
        # Verifica se já existe um gerente com o mesmo email para evitar duplicatas
        existing_manager = db.query(ManagersModel).filter(ManagersModel.email == manager_data.email).first()
        if existing_manager:
            raise HTTPException(status_code=400, detail="Manager with this email already exists")

        # Cria uma nova instância de ManagersModel
        db_manager = ManagersModel(
            name=manager_data.name,
            email=manager_data.email,
            hashed_password=bcrypt_context.hash(manager_data.hashed_password),
            is_active=True,
            user_type="managers"
        )

        # Adiciona e comita o novo gerente ao banco de dados
        db.add(db_manager)
        db.commit()
        db.refresh(db_manager)
        return db_manager

    except Exception as e:
        logging.error(f"Erro ao adicionar gerente: {e}", exc_info=True)  # Exibe o erro completo no log
        raise HTTPException(status_code=500, detail="Internal Server Error")   

async def fetch_manager_by_name(name: str, db: Session):
    manager = db.query(ManagersModel).filter(ManagersModel.name == name).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    return manager