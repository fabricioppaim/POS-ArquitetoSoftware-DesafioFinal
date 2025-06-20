from typing import List, Optional
from src.models.cliente import Cliente
from src.models.cliente_repository import ClienteRepositoryInterface

class ClienteService:
    """
    Serviço para operações de negócio relacionadas a clientes.
    
    Esta classe contém a lógica de negócios da aplicação,
    atuando como uma camada intermediária entre o controller
    e o repository.
    """
    
    def __init__(self, cliente_repository: ClienteRepositoryInterface):
        """
        Construtor do serviço de clientes.
        
        Args:
            cliente_repository (ClienteRepositoryInterface): Repositório de clientes
        """
        self.cliente_repository = cliente_repository
    
    def listar_todos(self) -> List[Cliente]:
        """
        Lista todos os clientes.
        
        Returns:
            List[Cliente]: Lista de todos os clientes
        """
        return self.cliente_repository.find_all()
    
    def buscar_por_id(self, cliente_id: int) -> Optional[Cliente]:
        """
        Busca um cliente por ID.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            Optional[Cliente]: Cliente encontrado ou None
            
        Raises:
            ValueError: Se o ID for inválido
        """
        if cliente_id <= 0:
            raise ValueError("ID do cliente deve ser um número positivo")
        
        return self.cliente_repository.find_by_id(cliente_id)
    
    def buscar_por_nome(self, nome: str) -> List[Cliente]:
        """
        Busca clientes por nome.
        
        Args:
            nome (str): Nome do cliente
            
        Returns:
            List[Cliente]: Lista de clientes com o nome especificado
            
        Raises:
            ValueError: Se o nome for inválido
        """
        if not nome or not nome.strip():
            raise ValueError("Nome não pode ser vazio")
        
        return self.cliente_repository.find_by_nome(nome.strip())
    
    def salvar(self, cliente_data: dict) -> Cliente:
        """
        Salva um cliente.
        
        Args:
            cliente_data (dict): Dados do cliente
            
        Returns:
            Cliente: Cliente salvo
            
        Raises:
            ValueError: Se os dados do cliente forem inválidos
        """
        self._validar_dados_cliente(cliente_data)
        
        # Verifica se já existe um cliente com o mesmo email
        if 'id' not in cliente_data:
            clientes_existentes = self.cliente_repository.find_all()
            for cliente in clientes_existentes:
                if cliente.email == cliente_data['email']:
                    raise ValueError("Já existe um cliente com este email")
        
        if 'id' in cliente_data and cliente_data['id']:
            # Atualização
            cliente_existente = self.cliente_repository.find_by_id(cliente_data['id'])
            if not cliente_existente:
                raise ValueError("Cliente não encontrado para atualização")
            
            cliente_existente.nome = cliente_data['nome']
            cliente_existente.email = cliente_data['email']
            return self.cliente_repository.save(cliente_existente)
        else:
            # Criação
            cliente = Cliente.from_dict(cliente_data)
            return self.cliente_repository.save(cliente)
    
    def deletar(self, cliente_id: int) -> bool:
        """
        Deleta um cliente por ID.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            bool: True se deletado com sucesso, False caso contrário
            
        Raises:
            ValueError: Se o ID for inválido
        """
        if cliente_id <= 0:
            raise ValueError("ID do cliente deve ser um número positivo")
        
        return self.cliente_repository.delete_by_id(cliente_id)
    
    def contar_clientes(self) -> int:
        """
        Conta o número total de clientes.
        
        Returns:
            int: Número total de clientes
        """
        return self.cliente_repository.count()
    
    def _validar_dados_cliente(self, cliente_data: dict) -> None:
        """
        Valida os dados do cliente.
        
        Args:
            cliente_data (dict): Dados do cliente
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        if not isinstance(cliente_data, dict):
            raise ValueError("Dados do cliente devem ser um dicionário")
        
        if 'nome' not in cliente_data or not cliente_data['nome']:
            raise ValueError("Nome é obrigatório")
        
        if 'email' not in cliente_data or not cliente_data['email']:
            raise ValueError("Email é obrigatório")
        
        nome = cliente_data['nome'].strip()
        email = cliente_data['email'].strip()
        
        if len(nome) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        
        if len(nome) > 100:
            raise ValueError("Nome deve ter no máximo 100 caracteres")
        
        if len(email) > 120:
            raise ValueError("Email deve ter no máximo 120 caracteres")
        
        if '@' not in email or '.' not in email:
            raise ValueError("Email deve ter um formato válido")

