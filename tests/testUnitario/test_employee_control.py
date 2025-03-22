import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi import HTTPException
from App.utils.common_schemas_Enum import Genero
from App.services.employee_services.employee_control import EmployeeControl
from App.schemas.employee_schemas import EmployeeInfo

@pytest.mark.asyncio
async def test_get_employee_info_success():
    service = EmployeeControl()

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

    with patch.object(service, 'async_get_employee', wraps=service.async_get_employee):
        result = await service.get_employee_info(db=mock_db, employee_id=1)

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
async def test_get_employee_info_fail_EmployeTypeInclude():
    service = EmployeeControl()

    # Cria o mock do employee retornado
    mock_employee = MagicMock()
    mock_employee.id = 1
    mock_employee.name = "João"
    mock_employee.email = "João@inatel.br"
    mock_employee.is_active = True
    mock_employee.user_type = "employee"
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

    with patch.object(service, 'async_get_employee', wraps=service.async_get_employee):
        result = await service.get_employee_info(db=mock_db, employee_id=1)

        assert isinstance(result, EmployeeInfo)
        assert result.id == 1
        assert result.name == "João"
        assert result.email == "João@inatel.br"
        assert result.is_active is True
        assert not hasattr(result, "user_type")
        assert result.genero == Genero.masculino
        assert result.cpf == "12345678901"
        assert result.salario == 1000.0
        assert result.endereco == "Rua A, 123"
        assert result.telefone == "123456789"

@pytest.mark.asyncio
async def test_get_employee_info_fail_passwordInclude():
    service = EmployeeControl()

    # Cria o mock do employee retornado
    mock_employee = MagicMock()
    mock_employee.id = 1
    mock_employee.name = "João"
    mock_employee.email = "João@inatel.br"
    mock_employee.hashed_password = "12345678901"
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

    with patch.object(service, 'async_get_employee', wraps=service.async_get_employee):
        result = await service.get_employee_info(db=mock_db, employee_id=1)

        assert isinstance(result, EmployeeInfo)
        assert result.id == 1
        assert result.name == "João"
        assert result.email == "João@inatel.br"
        assert result.is_active is True
        assert not hasattr(result, "hashed_password")
        assert result.genero == Genero.masculino
        assert result.cpf == "12345678901"
        assert result.salario == 1000.0
        assert result.endereco == "Rua A, 123"
        assert result.telefone == "123456789"

