# **Gerenciamento de Controle de Escala e Ponto - BackEnd;**
## Este é o back-end de uma aplicação que gerencia a escala e o controle de ponto dos funcionários da cantina do INATEL. O projeto é desenvolvido com o objetivo de seguir os princípios de engenharia de software, aderindo às boas práticas e aos princípios SOLID para manter um código organizado e fácil de manter.
  
***

## Índice

1. Pré-requisitos
2. Instruções de Configuração
   - Clonar o Repositório
   - Criar e Ativar o Ambiente Virtual
   - Instalar as Dependências
   - Configurar o Banco de Dados PostgreSQL
   - Executar a Aplicação
   - Acessar a Documentação
3. Estrutura do Projeto

##

## 1. Pré-requisitos

- Python 3.9+
- PostgreSQL (para o banco de dados)
- Virtualenv (opcional, mas recomendado para isolar as dependências)

## 2. Instruções de Configuração

### Clone o repositório e navegue até a pasta do projeto:

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DA_PASTA>
python3 -m venv env
source env/bin/activate  # No Windows: env\Scripts\activate
pip install -r requirements.txt
```

### Instale o PostgreSQL, caso ainda não o tenha, e crie um novo banco de dados com o nome controle_de_escala_e_ponto:

```SQL
CREATE DATABASE controle_de_escala_e_ponto;
```

### Configure a URL de conexão no seguinte formato, adaptando para seu ambiente:
```Python
DATABASE_URL='postgresql://postgres:9182@localhost:5432/controle_de_escala_e_ponto'
```

### Inicie o servidor FastAPI com o seguinte comando:
```bash
uvicorn main:app --reload
```

### Após iniciar a aplicação, você pode acessar a documentação interativa:
- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

***

## **Escolha Arquitetural**

### A arquitetura escolhida para este projeto foi baseada no modelo **SOA (Service-Oriented Architecture)**, aplicada ao backend para responder às requisições do front-end em **SPA (Single Page Application)**.

- Para a implementação do **SOA**, foi utilizado o framework **FastAPI** para a criação da API e o banco de dados **PostgreSQL**.
- Para a implementação do **SPA**, foi utilizado o **React**.

##

## **Breve Explicação sobre Princípios de Arquitetura de Software**
### Existem alguns princípios, como Integridade Conceitual, Ocultamento de Informações, Coesão e Acoplamento, que são fundamentais para projetar um sistema sustentável. Vamos entender um pouco mais sobre cada um deles:

#### Integridade Conceitual: Refere-se à prática de seguir um padrão consistente durante o desenvolvimento do software, facilitando a adição de novas funcionalidades e promovendo um entendimento claro de como o sistema é organizado.

#### Ocultamento de Informações: Consiste em tornar públicas apenas as informações essenciais de uma classe ou função, ocultando os detalhes de implementação para quem não precisa interagir diretamente com ela. Isso contribui para a segurança e modularidade do código.

#### Coesão: Esse princípio promove a criação de classes com uma única responsabilidade bem definida, evitando sobrecarregar cada classe com múltiplas tarefas. Isso facilita a manutenção e a organização do código, pois cada classe executa uma função específica.

#### Acoplamento: Ao contrário dos outros conceitos, o acoplamento deve ser minimizado sempre que possível. Ele se refere ao grau de dependência entre as classes. Um acoplamento baixo, ou "fraco", significa que as classes não dependem criticamente umas das outras, permitindo que uma classe seja alterada sem quebrar o funcionamento das demais. Um acoplamento alto, por outro lado, pode tornar o sistema frágil e difícil de modificar.

## **Onde esses princípios são aplicados neste projeto?**

### Integridade Conceitual
- **Nomenclatura Padrão**: As classes seguem padrões de boas práticas em Python, como `crud`, `models`, `schemas`, `api`, `services`, e `utils`. Esses nomes são comuns em aplicações baseadas na Arquitetura Orientada a Serviços (SOA), o que mantém a integridade conceitual do sistema.
- **Estrutura de Pastas**: A estrutura de pastas do projeto garante que cada classe esteja em um local específico, com um `__init__.py` em cada pasta. Isso permite que quem usa o projeto possa importar diretamente o módulo desejado.
- *(Adicionar outros conceitos relevantes)*

### Ocultamento de Informações
- **Uso de `__init__`**: Ao utilizar o `__init__.py`, é possível ocultar detalhes de implementação e permitir a importação direta de métodos sem necessidade de conhecer a estrutura interna.
- **Funções Utilitárias em `utils`**: Colocar funções utilitárias na pasta `utils` permite que apenas as funcionalidades desejadas sejam acessadas, sem necessidade de expor sua lógica interna.
- *(Adicionar outros conceitos relevantes)*

### Coesão
- **Separação de Esquemas (`Schemas`)**: A divisão dos esquemas em diferentes arquivos, como `auth_schemas`, `employee_schemas`, `manager_schemas`, `time_tracking_schemas`, `token_schemas`, e `user_schemas`, garante que cada arquivo seja responsável por uma única parte do sistema. Isso facilita a implementação de novos atributos e a identificação de problemas específicos.
- **Organização da `models`**: Embora a pasta `models` contenha `manager`, `employee` e `user` juntos, isso ocorre porque essas tabelas de usuários são fundamentais e mudam pouco. Agrupá-las em um único lugar facilita seu acesso.
- *(Adicionar outros conceitos relevantes)*

### Acoplamento
- **Divisão de `routers`**: Para reduzir o acoplamento, foram criadas classes de `routers` separadas, evitando que um único `app.FastAPI` concentre todas as requisições. Dessa forma, o problema em um router específico não afeta os demais.
- **Separação de CRUDs**: A divisão das operações de CRUD (Create, Read, Update, Delete) reduz o impacto de falhas em uma operação específica, impedindo que elas comprometam outras partes do sistema.
- **Separação de Serviços em `Services`**: A pasta `services` garante uma divisão clara entre métodos de autenticação e gerenciamento de usuários, o que minimiza a dependência de uma única lógica.
- *(Adicionar outros conceitos relevantes)*

## 

## **Breve Explicação sobre os Princípios SOLID**

Os princípios SOLID são diretrizes que, quando aplicadas, garantem uma arquitetura de software bem estruturada, maximizando a qualidade e a manutenção do sistema. Esses princípios são:

- **S** = Single Responsibility Principle  
- **O** = Open-Closed Principle  
- **L** = Liskov Substitution Principle  
- **I** = Interface Segregation Principle  
- **D** = Dependency Inversion Principle  

A seguir, vamos entender um pouco mais sobre cada um deles:

### Single Responsibility Principle
Um módulo ou classe deve ter uma única responsabilidade, sendo responsável apenas por um grupo específico de funcionalidades e mudando apenas se esse grupo precisar de alterações.

### Open-Closed Principle
É preferível estender funcionalidades de um sistema ao invés de modificar diretamente o código existente.

### Liskov Substitution Principle
Uma classe base deve ser substituível por suas classes derivadas sem a necessidade de alterar propriedades ou comportamentos esperados.

### Interface Segregation Principle
É melhor criar interfaces pequenas e específicas, que permitam aos clientes implementar apenas os métodos que realmente irão utilizar.

### Dependency Inversion Principle
Estabelece que as dependências devem ser com abstrações (interfaces) em vez de implementações concretas, priorizando a flexibilidade e a independência das classes.

## **Onde esses princípios são aplicados neste projeto?**

### Single Responsibility Principle
- **a**: txt
- **b**: txt
- *(Adicionar outros conceitos relevantes)*

### Open-Closed Principle
- **a**: txt
- **b**: txt
- *(Adicionar outros conceitos relevantes)*

### Liskov Substitution Principle
- **a**: txt
- **b**: txt
- *(Adicionar outros conceitos relevantes)*

### Interface Segregation Principle
- **a**: txt
- **b**: txt
- **c**: txt
- *(Adicionar outros conceitos relevantes)*

### Dependency Inversion Principle
- **a**: txt
- **b**: txt
- **c**: txt
- *(Adicionar outros conceitos relevantes)*

## 