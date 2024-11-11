# App/api/__init__.py
from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .employees import router as employees_router
from .managers import router as managers_router

# Cria o roteador principal para incluir todos os sub-roteadores
api_router = APIRouter()

# Inclui os roteadores de cada módulo com prefixos opcionais
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(employees_router, prefix="/employees", tags=["Employees"])
api_router.include_router(managers_router, prefix="/managers", tags=["Managers"])
