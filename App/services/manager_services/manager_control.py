from sqlalchemy.orm import Session
from App.schemas import EmployeeCreate, EmployeeUpdate, ManagerCreate, EmployeeInfo, EmployeeListItem, EmployeeSalary
from App.models import EmployeesModel, ManagersModel, UsersModel, TimePunches
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
import logging
from App.utils.employee_utils import merge_adress,merge_telefone
from App.utils.Interfaces.EmployeeGeter import EmployeeGeter
from typing import List
from abc import ABC, abstractmethod

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