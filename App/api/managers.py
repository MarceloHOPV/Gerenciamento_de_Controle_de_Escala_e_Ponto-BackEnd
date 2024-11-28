# App/api/manager.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from App.schemas import ManagerCreate, EmployeeCreate, EmployeeInfo, EmployeeUpdate,WorkScheduleEntry, WorkScheduleSchema
from App.services.manager_services.manager_control import ManagerControl
from App.db import get_db

router = APIRouter(prefix="/managers", tags=["Managers"])

mc = ManagerControl()

# pega um employee pelo id
@router.get("/getEmployeById/{employee_id},{manager_id}",status_code=status.HTTP_200_OK,response_model=EmployeeInfo)
async def __employee_get(employee_id: int, manager_id: int,db: Session = Depends(get_db)):
    return await mc._get_employee_info(db,employee_id,manager_id)
# pega todos os employees de um manager
@router.get("/getEmployeList/{manager_id}", status_code=status.HTTP_200_OK)
async def __employee_list(manager_id: int,db: Session = Depends(get_db)):
    return await mc._list_employees(db, manager_id)
# posta um employee
@router.post("/postEmployee/", status_code=status.HTTP_201_CREATED)
async def __register_employee(employee_data: EmployeeCreate, db: Session = Depends(get_db)):
    # Verifique se o usuário atual é um gerente caso usassemos o token
    # if current_user.user_type != "managers":
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create employees")
    # Cria o funcionário
    return await mc._employee_register(db=db, employee_data= employee_data)

@router.delete("/deleteEmployee/{employee_id},{manager_id}", status_code=status.HTTP_200_OK)
async def __employee_delete(employee_id: int,manager_id: int, db: Session = Depends(get_db)):
    return await mc._delete_employee(db, employee_id,manager_id)

@router.get("/getPunches/{employee_id},{manager_id}", status_code=status.HTTP_200_OK)
async def __get_punches(employee_id: int, manager_id: int, db: Session = Depends(get_db)):
    return await mc._get_punches_employee(db, employee_id, manager_id)

@router.get("/getSalaryList/{manager_id}", status_code=status.HTTP_200_OK)
async def __get_salary_list(manager_id: int, db: Session = Depends(get_db)):
    return await mc._get_salary_list(db, manager_id)

@router.put("/updateEmployee/{employee_id},{manager_id}", status_code=status.HTTP_200_OK)
async def __update_employee_info(employee_id: int, manager_id: int, update_data: EmployeeUpdate, db: Session = Depends(get_db)):
    return await mc._update_employee(db, employee_id, update_data,manager_id)

@router.post("/employees/{employee_id}{this_manager_id}/work-schedules", response_model=dict)
async def __work_schedule_post(
    employee_id: int,
    work_schedule_data: WorkScheduleEntry,
    this_manager_id: int,
    db: Session = Depends(get_db)
):
    return await mc._post_work_schedule(db, work_schedule_data, employee_id, this_manager_id)


# Endpoint para listar horários de trabalho
@router.get("/employees/{employee_id}{this_manager_id}/work-schedules", response_model=WorkScheduleSchema)
async def __work_scheduleget(
    employee_id: int,
    this_manager_id: int,
    db: Session = Depends(get_db)
):
    return await mc._get_work_schedule_list(db, employee_id, this_manager_id)

#Endoints da aplicação em geral
# pega o manager pelo id
@router.get("/getManagerByID/{manager_id}", status_code=status.HTTP_200_OK)
async def __id_manager_get(manager_id: int,db: Session = Depends(get_db)):
    return await mc._get_manager_by_id(db,manager_id)

# posta um manager
@router.post("/registerManager", status_code=status.HTTP_201_CREATED)
async def __manager_create(manager_data: ManagerCreate, db: Session = Depends(get_db)):
    return await mc._manager_register(manager_data, db)
