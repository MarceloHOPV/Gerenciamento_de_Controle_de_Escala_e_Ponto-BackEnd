from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from App.db import engine, get_db
from App.api import api_router
import App.models as models

# Inicializa a aplicação FastAPI
app = FastAPI()

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Inclui as rotas/endpoints
app.include_router(api_router)

