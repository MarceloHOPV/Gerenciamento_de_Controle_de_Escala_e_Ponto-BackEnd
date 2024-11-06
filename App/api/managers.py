# App/api/manager.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.models import ManagersModel
from App.schemas import ManagerCreate, EmployeeCreate
from App.services.manager_services.manager_control import create_employee, get_employee_list, get_employee,get_manager_by_id, update_employee, delete_employee, add_manager
from App.db import get_db

router = APIRouter(prefix="/managers", tags=["Managers"])

# Endpoints do manager

# pega um employee pelo id
@router.get("/getEmployeById/{employee_id}{manager_id}",status_code=status.HTTP_201_CREATED)
async def employee_get(employee_id: int, manager_id: int,db: Session = Depends(get_db)):
    return await get_employee(db,employee_id,manager_id)


# pega todos os employees de um manager
@router.get("/getEmployeList/{manager_id}", status_code=status.HTTP_200_OK)
async def employee_list(manager_id: int,db: Session = Depends(get_db)):
    return await get_employee_list(db,manager_id)

# posta um employee
@router.post("/postEmployee/{manager_id}", status_code=status.HTTP_201_CREATED)
async def employee_create(employee_data: EmployeeCreate, 
                          db: Session = Depends(get_db)):
    
    # Verifique se o usuário atual é um gerente caso usassemos o token
    # if current_user.user_type != "managers":
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create employees")

    # Cria o funcionário
    return await create_employee(employee_data, manager_id=employee_data.manager_id, db=db)
    
#Endoints da aplicação em geral

# pega o manager pelo id
@router.get("/getManagerByID/{manager_id}", status_code=status.HTTP_200_OK)
async def id_manager_get(manager_id: int,db: Session = Depends(get_db)):
    return await get_manager_by_id(db,manager_id)

# posta um manager

@router.post("/registerManager", status_code=status.HTTP_201_CREATED)
async def manager_create(manager_data: ManagerCreate, db: Session = Depends(get_db)):
    return await add_manager(manager_data, db)
