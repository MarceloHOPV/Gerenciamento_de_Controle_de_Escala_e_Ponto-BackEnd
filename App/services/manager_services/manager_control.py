from sqlalchemy.orm import Session
from App.schemas import EmployeeCreate, EmployeeUpdate, ManagerCreate
from App.models import EmployeesModel, ManagersModel, UsersModel
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
import logging
from App.utils.employee_utils import merge_adress,merge_telefone

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cadastrar funcionário
async def create_employee(db: Session, employee_data: EmployeeCreate):
    
    # Verificando se o manager é valido
    manager = db.query(ManagersModel).filter(ManagersModel.id == employee_data.manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")

    # Criptografando a senha
    hashed_password = bcrypt_context.hash(employee_data.hashed_password)

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
    return {"id":db_employee.id,"name":db_employee.name , "detail":"Employee created successfully", "status":201}

# Exemplo de front-end pra ajudar a entender o código
# async function createEmployee(employeeData) {
#     const managerId = getLoggedInManagerId(); // Função para pegar o id do manager logado
#     const response = await fetch("/api/create_employee", {
#         method: "POST",
#         headers: {
#             "Content-Type": "application/json"
#         },
#         body: JSON.stringify({
#             ...employeeData,
#             manager_id: managerId
#         })
#     });
#     const data = await response.json();
#     return data;
# }

# Get employee geral
async def get_employee_list(db: Session, this_manager_id: int):
    manager = db.query(ManagersModel).filter(ManagersModel.id == this_manager_id).first()
    if not manager:
          raise HTTPException(status_code=404, detail="Manager not found")
    return manager.employees
     
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

# Funções get by id
def get_employee(db: Session, employee_id: int, this_manager_id: int):
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
    

async def update_employee(db: Session, employee_id: int, update_data: EmployeeUpdate, this_manager_id: int):
    # Resposta pro front end se o employee existe
    db_employee = get_employee(db, employee_id, this_manager_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Atualiza os valores se manager e employee são validos
    
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee
    

async def delete_employee(db: Session, employee_id: int, this_manager_id):
    # Resposta pro front end se o employee existe
    db_employee = get_employee(db, employee_id, this_manager_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Deleta o employee caso encontrado
    db.delete(db_employee)
    db.commit()
    return db_employee


# Função do sistema em geral

async def get_manager_by_id(db: Session, manager_id: int):
    manager = db.query(ManagersModel).filter(ManagersModel.id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    return manager

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