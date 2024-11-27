from fastapi import HTTPException, Depends
from App.models import EmployeesModel, ManagersModel, UsersModel
from sqlalchemy.orm import Session
from App.models.time_tracking_models import TimePunches
from datetime import datetime
from App.utils.Interfaces.EmployeeGeter import EmployeeGeter
from abc import ABC, abstractmethod
from App.schemas import EmployeeInfo

class EmployeeControl(EmployeeGeter):

    def __init__(self):
        pass

    def get_employee(self, db: Session, employee_id: int):
            # Resposta pro front end se o employee existe
            employee = db.query(EmployeesModel).filter(EmployeesModel.id == employee_id).first()
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            # return se a operação foi um sucesso
            return employee

    async def async_get_employee(self, db: Session, employee_id: int):
        return self.get_employee(db, employee_id)
    
    async def _get_employee_info(self, db: Session, employee_id: int) -> EmployeeInfo:
        db_employee = await self.async_get_employee(db, employee_id)
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        # Converta diretamente para o schema
        return EmployeeInfo.from_orm(db_employee)

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
            "status": 201
        }
    

#     @router.get("/users/{user_id}", response_model=UserSchema)
# async def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(UsersModel).filter(UsersModel.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Cria uma instância de UserSchema com os dados necessários do user
#     user_data = UserSchema(
#         id=user.id,
#         name=user.name,
#         email=user.email,  # Exemplo: apenas campos definidos no UserSchema
#         # Adicione os campos relevantes para o schema
#     )

#     return user_data
