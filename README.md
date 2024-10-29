# **Gerenciamento de Controle de Escala e Ponto - BackEnd;**
## Este é o back-end de uma aplicação que gerencia a escala e o controle de ponto dos funcionários da cantina do INATEL. O projeto é desenvolvido com o objetivo de seguir os princípios de engenharia de software, aderindo às boas práticas e aos princípios SOLID para manter um código organizado e fácil de manter.

## 

## **Breve Explicação sobre Princípios de Arquitetura de Software**
Existem alguns princípios, como Integridade Conceitual, Ocultamento de Informações, Coesão e Acoplamento, que são fundamentais para projetar um sistema sustentável. Vamos entender um pouco mais sobre cada um deles:

### Integridade Conceitual: Refere-se à prática de seguir um padrão consistente durante o desenvolvimento do software, facilitando a adição de novas funcionalidades e promovendo um entendimento claro de como o sistema é organizado.

### Ocultamento de Informações: Consiste em tornar públicas apenas as informações essenciais de uma classe ou função, ocultando os detalhes de implementação para quem não precisa interagir diretamente com ela. Isso contribui para a segurança e modularidade do código.

### Coesão: Esse princípio promove a criação de classes com uma única responsabilidade bem definida, evitando sobrecarregar cada classe com múltiplas tarefas. Isso facilita a manutenção e a organização do código, pois cada classe executa uma função específica.

### Acoplamento: Ao contrário dos outros conceitos, o acoplamento deve ser minimizado sempre que possível. Ele se refere ao grau de dependência entre as classes. Um acoplamento baixo, ou "fraco", significa que as classes não dependem criticamente umas das outras, permitindo que uma classe seja alterada sem quebrar o funcionamento das demais. Um acoplamento alto, por outro lado, pode tornar o sistema frágil e difícil de modificar.

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

## **Breve Explicação sobre os princípios SOLID**
Os princípios SOLID
