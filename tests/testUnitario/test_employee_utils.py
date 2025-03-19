import pytest
from App.schemas.employee_schemas import Endereco, Telefone
from App.utils.employee_utils import merge_adress, merge_telefone

def test_merge_address_positive():
    # Instanciando a classe Endereco
    employee_address = Endereco(
        rua="Rua dos Bobos",
        numero=0,
        bairro="Bairro Sem Nome",
        cidade="Cidade Oculta",
        estado="Estado do Sul",
        cep="00000-000"
    )
    # Fazendo atribuição do retorno da função merge_adress
    result = merge_adress(employee_address)
    # Verificando se o retorno é o esperado
    assert result == "Rua dos Bobos, 0, Bairro Sem Nome, Cidade Oculta, Estado do Sul"

def test_merge_address_negative():
    # Instanciando a classe Endereco
    employee_address = Endereco(
        rua="Rua dos Bobos",
        numero=0,
        bairro="Bairro Sem Nome",
        cidade="Cidade Oculta",
        estado="Estado do Sul",
        cep="00000-000"
    )
    # Fazendo atribuição do retorno da função merge_adress
    result = merge_adress(employee_address)
    # Verificando se o retorno é o esperado
    assert result != "Rua dos Bobos, 0, Bairro Sem Nome, Cidade Oculta, Estado do Sul, 00000-000"

def test_merge_telefone_positive():
    # Instanciando a classe Telefone
    employee_phone = Telefone(
        ddd="00",
        numero="00000-0000"
    )
    # Fazendo atribuição do retorno da função merge_telefone
    result = merge_telefone(employee_phone)
    # Verificando se o retorno é o esperado
    assert result == "(00) 00000-0000"

def test_merge_telefone_negative():
    # Instanciando a classe Telefone
    employee_phone = Telefone(
        ddd="00",
        numero="00000-0000"
    )
    # Fazendo atribuição do retorno da função merge_telefone
    result = merge_telefone(employee_phone)
    # Verificando se o retorno é o esperado
    assert result != "(00) 0000-0000"