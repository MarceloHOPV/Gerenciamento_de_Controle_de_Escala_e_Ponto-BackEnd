from App.schemas import employee_schemas
from App.utils import common_schemas_Enum

def merge_adress(employee_adress: employee_schemas.Endereco) -> str:
    return f"{employee_adress.rua}, {employee_adress.numero}, {employee_adress.bairro}, {employee_adress.cidade}, {employee_adress.estado}"

def merge_telefone(telefone: employee_schemas.Telefone) -> str:
    return f"({telefone.ddd}) {telefone.numero}"
