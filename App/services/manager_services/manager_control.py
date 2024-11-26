from sqlalchemy.orm import Session
from App.schemas import EmployeeCreate, EmployeeUpdate, ManagerCreate, EmployeeInfo, EmployeeListItem, EmployeeSalary, WorkScheduleSchema, WorkScheduleEntry
from App.models import EmployeesModel, ManagersModel, UsersModel, TimePunches, WorkSchedule
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
import logging
from App.utils.common_schemas_Enum import Hora
from App.utils.employee_utils import merge_adress,merge_telefone
from App.utils.Interfaces.EmployeeGeter import EmployeeGeter
from typing import List
from abc import ABC, abstractmethod
from datetime import time

class ManagerControl(EmployeeGeter):
    def __init__(self):
        pass

    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Cadastrar funcionário
    async def _employee_register(self, db: Session, employee_data: EmployeeCreate):
        
        # Verificando se o manager é valido
        manager = db.query(ManagersModel).filter(ManagersModel.id == employee_data.manager_id).first()
        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")

        employee = db.query(EmployeesModel).filter(EmployeesModel.email == employee_data.email).first()
        if employee:
            raise HTTPException(status_code=404, detail="Already exists a employee with this email")

        # Criptografando a senha
        hashed_password = self.bcrypt_context.hash(employee_data.hashed_password)

        # Criando o dicionário de dados do employee e colocando a senha criptografada
        db_employee = EmployeesModel(
            name=employee_data.name,
            email=employee_data.email,
            is_active=True,
            user_type="employee",
            genero=employee_data.genero,
            cpf=employee_data.cpf,
            salario=employee_data.salario,         # Acessando 'rua' de endereco
            endereco=merge_adress(employee_data.endereco),          # Acessando 'ddd' de telefone
            telefone=merge_telefone(employee_data.telefone),    # Acessando 'numero' de telefone
            manager_id=employee_data.manager_id,
            hashed_password=hashed_password
        )

        # Comitando o employee no banco de dados
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return {"id":db_employee.id,
                "name":db_employee.name , 
                "detail":"Employee created successfully", 
                "status":201}
    
    def get_employee(self, db: Session, employee_id: int, this_manager_id: int):
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
    
    async def _async_get_employee(self, db: Session, employee_id: int, this_manager_id: int):
            return self.get_employee(db, employee_id, this_manager_id)
    
    async def _get_employee_info(self, db: Session, employee_id: int, this_manager_id: int) -> EmployeeInfo:
        db_employee = await self._async_get_employee(db, employee_id, this_manager_id)
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        # Converta diretamente para o schema
        return EmployeeInfo.from_orm(db_employee)

    async def _list_employees(self, db: Session, this_manager_id: int) -> List[EmployeeListItem]:
        manager = db.query(ManagersModel).filter(ManagersModel.id == this_manager_id).first()
        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")
        # Converte cada funcionário do ORM para o schema
        employees = [
            EmployeeListItem.from_orm(employee) for employee in manager.employees
        ]
        return employees

    async def _update_employee(self, db: Session, employee_id: int, update_data: EmployeeUpdate, this_manager_id: int):
        # Resposta pro front end se o employee existe
        db_employee = await self._async_get_employee(db, employee_id, this_manager_id)
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        # Atualiza os valores se manager e employee são validos
        
        for key, value in update_data.dict(exclude_unset=True).items():
            if key == "endereco":  # Converte o endereço usando merge_adress
                value = merge_adress(value)
            elif key == "telefone":  # Converte o telefone usando merge_telefone
                value = merge_telefone(value)
            setattr(db_employee, key, value)  # Atualiza o campo no objeto ORM

        # Commit das alterações no banco de dados
        db.commit()
        db.refresh(db_employee)
        return {"id":db_employee.id,
                "name":db_employee.name ,
                "detail":"Employee updated successfully",
                "status":200}
        
    async def _delete_employee(self, db: Session, employee_id: int, this_manager_id):
        # Resposta pro front end se o employee existe
        db_employee = self.get_employee(db, employee_id, this_manager_id)
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        # Deleta o employee caso encontrado
        db.delete(db_employee)
        db.commit()
        return db_employee
    
    async def _get_salary_list(self, db: Session, this_manager_id: int)-> List[EmployeeSalary]:
        manager = db.query(ManagersModel).filter(ManagersModel.id == this_manager_id).first()
        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")
        # Converte cada funcionário do ORM para o schema
        employees_salary = [
            EmployeeSalary.from_orm(employee) for employee in manager.employees
        ]
        return employees_salary

    async def _get_punches_employee(self, db: Session, employee_id: int, this_manager_id: int):
    # Verificar se o employee existe
        db_employee = self.get_employee(db, employee_id, this_manager_id)
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        # Consultar os pontos batidos
        punches = db.query(TimePunches).filter(TimePunches.employee_id == employee_id).all()
        
        if not punches:
            raise HTTPException(status_code=404, detail="No punches found for this employee")
        
        return punches

    async def _post_work_schedule(self, db: Session, work_schedule_data: WorkScheduleEntry, employee_id: int, this_manager_id: int):
        # Verificar se o funcionário existe
        db_employee = await self._async_get_employee(db, employee_id, this_manager_id)

        # Converter os horários para datetime.time
        start_time = time(work_schedule_data.start_time.hora, work_schedule_data.start_time.minuto)
        end_time = time(work_schedule_data.end_time.hora, work_schedule_data.end_time.minuto)

        # Verificar se o horário de trabalho já existe
        db_work_schedule = (
            db.query(WorkSchedule)
            .filter(
                WorkSchedule.employee_id == employee_id,
                WorkSchedule.day_of_week == work_schedule_data.day_of_week,
                WorkSchedule.start_time == start_time,
            )
            .first()
        )

        if db_work_schedule:
            # Atualizar o horário existente
            db_work_schedule.end_time = end_time
            db.commit()
            db.refresh(db_work_schedule)
            status_code = 200  # Código para atualização
        else:
            # Criar um novo horário de trabalho
            db_work_schedule = WorkSchedule(
                employee_id=employee_id,
                day_of_week=work_schedule_data.day_of_week,
                start_time=start_time,
                end_time=end_time,
            )
            db.add(db_work_schedule)
            db.commit()
            db.refresh(db_work_schedule)
            status_code = 201  # Código para criação

        # Retornar resposta com o código de status apropriado
        return {
            "status_code": status_code,
            "message": "Work schedule created" if status_code == 201 else "Work schedule updated",
            "work_schedule": WorkScheduleEntry(
                day_of_week=db_work_schedule.day_of_week,
                start_time={"hora": db_work_schedule.start_time.hour, "minuto": db_work_schedule.start_time.minute},
                end_time={"hora": db_work_schedule.end_time.hour, "minuto": db_work_schedule.end_time.minute},
            ),
        }

    async def _get_work_schedule_list(self, db: Session, employee_id: int, this_manager_id: int) -> WorkScheduleSchema:
        # Verificar se o funcionário existe e pertence ao manager
        db_employee = await self._async_get_employee(db, employee_id, this_manager_id)

        # Recuperar todos os horários do funcionário
        db_work_schedules = (
            db.query(WorkSchedule)
            .filter(WorkSchedule.employee_id == employee_id)
            .all()
        )

        # Verificar se há horários cadastrados
        if not db_work_schedules:
            raise HTTPException(status_code=404, detail="No work schedules found for this employee")

        # Converter para o schema WorkScheduleSchema
        work_schedule_entries = [
            WorkScheduleEntry(
                day_of_week=work_schedule.day_of_week,
                start_time=Hora(
                    hora=work_schedule.start_time.hour,
                    minuto=work_schedule.start_time.minute
                ),
                end_time=Hora(
                    hora=work_schedule.end_time.hour,
                    minuto=work_schedule.end_time.minute
                )
            )
            for work_schedule in db_work_schedules
        ]

        return WorkScheduleSchema(data_hora=work_schedule_entries)

    # Função do sistema em geral

    async def _get_manager_by_id(self, db: Session, manager_id: int):
        manager = db.query(ManagersModel).filter(ManagersModel.id == manager_id).first()
        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")
        return manager

    async def _manager_register(self, manager_data: ManagerCreate, db: Session):
            # Verifica se já existe um gerente com o mesmo email para evitar duplicatas
            existing_manager = db.query(ManagersModel).filter(ManagersModel.email == manager_data.email).first()
            if existing_manager:
                raise HTTPException(status_code=404, detail="Already exists a manager with this email")

            # Cria uma nova instância de ManagersModel
            db_manager = ManagersModel(
                name=manager_data.name,
                email=manager_data.email,
                hashed_password=self.bcrypt_context.hash(manager_data.hashed_password),
                is_active=True,
                user_type="managers"
            )

            # Adiciona e comita o novo gerente ao banco de dados
            db.add(db_manager)
            db.commit()
            db.refresh(db_manager)
            return db_manager  