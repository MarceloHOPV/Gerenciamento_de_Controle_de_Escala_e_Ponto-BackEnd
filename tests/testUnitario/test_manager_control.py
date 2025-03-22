import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi import HTTPException
from App.utils.common_schemas_Enum import Genero
from App.services.manager_services.manager_control import ManagerControl
from App.schemas.employee_schemas import EmployeeInfo, EmployeeListItem

@pytest.mark.asyncio
async def test_manager_getemployee_info_success():
    service = ManagerControl()

    # Cria o mock do employee retornado
    mock_employee = MagicMock()
    mock_employee.id = 1
    mock_employee.name = "João"
    mock_employee.email = "João@inatel.br"
    mock_employee.is_active = True
    mock_employee.genero = Genero.masculino
    mock_employee.cpf = "12345678901"
    mock_employee.salario = 1000.0
    mock_employee.endereco = "Rua A, 123"
    mock_employee.telefone = "123456789"

    # Cria um mock de db que retorna o employee
    mock_db = MagicMock()
    (
        mock_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = mock_employee

    with patch.object(service, '_async_get_employee', wraps=service._async_get_employee):
        result = await service._get_employee_info(db=mock_db, employee_id=1, this_manager_id=1)

        assert isinstance(result, EmployeeInfo)
        assert result.id == 1
        assert result.name == "João"
        assert result.email == "João@inatel.br"
        assert result.is_active is True
        assert result.genero == Genero.masculino
        assert result.cpf == "12345678901"
        assert result.salario == 1000.0
        assert result.endereco == "Rua A, 123"
        assert result.telefone == "123456789"

@pytest.mark.asyncio
async def test_manager_getemployee_info_not_found():
    service = ManagerControl()

    # Mock do banco de dados que retorna None
    mock_db = MagicMock()
    (
        mock_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = None

    # Espera que a exceção HTTP 404 seja levantada
    with patch.object(service, '_async_get_employee', wraps=service._async_get_employee):
        with pytest.raises(HTTPException) as exc_info:
            await service._get_employee_info(db=mock_db, employee_id=1, this_manager_id=1)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Manager not found"

@pytest.mark.asyncio
async def test_list_employees_success():
    service = ManagerControl()

    # Cria mocks de funcionários
    mock_employee1 = MagicMock()
    mock_employee1.id = 1
    mock_employee1.name = "João"
    mock_employee1.email = "joao@inatel.br"
    mock_employee1.genero = Genero.masculino
    mock_employee1.cpf = "12345678901"
    mock_employee1.salario = 2000.0
    mock_employee1.endereco = "Rua A"
    mock_employee1.telefone = "123456789"

    mock_employee2 = MagicMock()
    mock_employee2.id = 2
    mock_employee2.name = "Maria"
    mock_employee2.email = "maria@inatel.br"
    mock_employee2.genero = Genero.feminino
    mock_employee2.cpf = "98765432100"
    mock_employee2.salario = 2500.0
    mock_employee2.endereco = "Rua B"
    mock_employee2.telefone = "987654321"

    # Cria mock do manager com a lista de employees
    mock_manager = MagicMock()
    mock_manager.employees = [mock_employee1, mock_employee2]

    # Cria mock do banco de dados
    mock_db = MagicMock()
    (
        mock_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = mock_manager

    # Chama a função real
    result = await service._list_employees(db=mock_db, this_manager_id=1)

    # Verificações
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], EmployeeListItem)
    assert result[0].name == "João"
    assert result[1].name == "Maria"

@pytest.mark.asyncio
async def test_list_employees_manager_not_found():
    service = ManagerControl()

    # Mock do banco que retorna None (manager não existe)
    mock_db = MagicMock()
    (
        mock_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = None

    with pytest.raises(HTTPException) as exc_info:
        await service._list_employees(db=mock_db, this_manager_id=999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Manager not found"
