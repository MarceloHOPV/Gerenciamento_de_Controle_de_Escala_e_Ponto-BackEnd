from pydantic import BaseModel
from typing import Optional
#**********************************Modelos*****************************************#

#*********************User**********************************#
class User(BaseModel):
    name: str
    cpf: str
    email: str
    hashed_password: str
    is_active: bool

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    hashed_password: Optional[str]
    is_active: Optional[bool]

#*********************Manager********************************#


# Análise dos Princípios SOLID
# Single Responsibility Principle (SRP) - Princípio da Responsabilidade Única:
# Como está sendo aplicado: Cada classe no seu código (User, Employee, Manager, BancoHora, Cronograma, etc.) tem uma responsabilidade clara e única. User define dados de usuário, Employee e Manager estendem User para especializá-los, e BancoHora e Cronograma possuem finalidades específicas.
# Dica para aprimorar: Verifique se cada classe encapsula apenas informações pertinentes a ela. Se User, Employee ou Manager tiverem lógica de negócios ou métodos de manipulação de dados, considere separar essa lógica em serviços específicos.

# Open/Closed Principle (OCP) - Princípio Aberto/Fechado:
# Como está sendo aplicado: Seu código já demonstra abertura para extensões (por exemplo, Employee e Manager herdam de User), mas ao mesmo tempo, mantém as classes fechadas para modificações.
# Dica para aprimorar: Se você precisar adicionar mais tipos de usuários no futuro, considere uma abordagem usando interfaces ou classes abstratas para manter a extensão mais flexível. Assim, você poderá adicionar novos tipos sem modificar as classes existentes.

# Liskov Substitution Principle (LSP) - Princípio da Substituição de Liskov:
# Como está sendo aplicado: Suas classes Employee e Manager podem substituir User sem impactar o sistema, pois ambas herdam e estendem User de forma coesa. Isso está em linha com o princípio de Liskov.
# Dica para aprimorar: Mantenha a relação de herança entre Employee e Manager com User simples e coesa, garantindo que qualquer função que espera um User funcione bem com Employee e Manager.

# Interface Segregation Principle (ISP) - Princípio da Segregação de Interface:
# Como está sendo aplicado: No seu caso, os schemas são bem segmentados e não forçam o uso de campos desnecessários. Por exemplo, Employee e Manager têm atributos adicionais específicos sem interferir nos dados básicos de User.
# Dica para aprimorar: Caso o projeto cresça e sejam necessários novos tipos de dados para os usuários, você pode considerar dividir os schemas ou criar mais camadas de especialização, especialmente se cada tipo de usuário tiver campos ou métodos distintos.

# Dependency Inversion Principle (DIP) - Princípio da Inversão de Dependência:
# Como está sendo aplicado: Não há dependências explícitas em classes de serviços ou repositórios, o que é positivo. No entanto, é comum que serviços de negócios (que manipulam dados dos schemas) interajam com os modelos através de classes de serviço ou repositório.
# Dica para aprimorar: Considere adicionar camadas de abstração para o acesso a dados (por exemplo, uma classe de repositório que trate a comunicação com o banco de dados) e para operações específicas do domínio, mantendo o código desacoplado.
