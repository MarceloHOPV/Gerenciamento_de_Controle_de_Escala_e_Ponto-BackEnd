from fastapi import HTTPException, Depends
from App.models import EmployeesModel, ManagersModel, UsersModel
from sqlalchemy.orm import Session
from App.models.time_tracking_models import TimePunches
from datetime import datetime

async def async_get_employee(db: Session, employee_id: int, this_manager_id: int):
    # Resposta pro front end se o manager existe
    manager = db.query(ManagersModel).filter(ManagersModel.id == this_manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    # Resposta pro front end se o employee existe
    employee = db.query(EmployeesModel).filter(EmployeesModel.id == employee_id, EmployeesModel.manager_id == this_manager_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    # return se a operação foi um sucesso
    return employee

async def time_punch(db: Session, employee_id: int) -> dict:
    # Busca o funcionário pelo ID
    db_employee = db.query(EmployeesModel).filter(EmployeesModel.id == employee_id).first()
    # Verifica se o funcionário existe
    if not db_employee:
        return {"detail": "Employee not found", "status": 404}
    
    # Cria um registro de batida de ponto com a data e hora atual
    db_time_punch = TimePunches(
        employee_id=employee_id,
        punch_time=datetime.now()  # Data e hora exata
    )
    db.add(db_time_punch)
    db.commit()
    db.refresh(db_time_punch)
    
    # Retorno com as informações do funcionário e a confirmação
    return {
        "id": db_employee.id,
        "name": db_employee.name,
        "detail": "Time successfully punched",
        "status": 200
    }
    