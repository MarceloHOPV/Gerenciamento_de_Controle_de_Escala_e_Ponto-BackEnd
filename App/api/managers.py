# App/api/manager.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.models import ManagersModel
from App.schemas import ManagerCreate
from App.crud.manager_crud import add_manager, fetch_manager_by_name
from App.db import get_db

router = APIRouter(prefix="/managers", tags=["Managers"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_manager(manager: ManagerCreate, db: Session = Depends(get_db)):
    return await add_manager(manager, db)

@router.get("/{username}", status_code=status.HTTP_200_OK)
async def get_manager_by_name(username: str, db: Session = Depends(get_db)):
    return await fetch_manager_by_name(username,db)
