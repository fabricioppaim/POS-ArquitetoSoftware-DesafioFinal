from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.cliente import Cliente

class ClienteRepositoryInterface(ABC):
    """
    Interface para o repositório de clientes.
    
    Define o contrato para operações de persistência
    relacionadas à entidade Cliente.
    """
    
    @abstractmethod
    def find_all(self) -> List[Cliente]:
        """
        Busca todos os clientes.
        
        Returns:
            List[Cliente]: Lista de todos os clientes
        """
        pass
    
    @abstractmethod
    def find_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """
        Busca um cliente por ID.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            Optional[Cliente]: Cliente encontrado ou None
        """
        pass
    
    @abstractmethod
    def find_by_nome(self, nome: str) -> List[Cliente]:
        """
        Busca clientes por nome.
        
        Args:
            nome (str): Nome do cliente
            
        Returns:
            List[Cliente]: Lista de clientes com o nome especificado
        """
        pass
    
    @abstractmethod
    def save(self, cliente: Cliente) -> Cliente:
        """
        Salva um cliente.
        
        Args:
            cliente (Cliente): Cliente a ser salvo
            
        Returns:
            Cliente: Cliente salvo
        """
        pass
    
    @abstractmethod
    def delete_by_id(self, cliente_id: int) -> bool:
        """
        Deleta um cliente por ID.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            bool: True se deletado com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    def count(self) -> int:
        """
        Conta o número total de clientes.
        
        Returns:
            int: Número total de clientes
        """
        pass


class ClienteRepository(ClienteRepositoryInterface):
    """
    Implementação concreta do repositório de clientes.
    
    Utiliza SQLAlchemy para interagir com o banco de dados.
    """
    
    def __init__(self, db):
        """
        Construtor do repositório.
        
        Args:
            db: Instância do SQLAlchemy
        """
        self.db = db
    
    def find_all(self) -> List[Cliente]:
        """
        Busca todos os clientes.
        
        Returns:
            List[Cliente]: Lista de todos os clientes
        """
        return Cliente.query.all()
    
    def find_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """
        Busca um cliente por ID.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            Optional[Cliente]: Cliente encontrado ou None
        """
        return Cliente.query.get(cliente_id)
    
    def find_by_nome(self, nome: str) -> List[Cliente]:
        """
        Busca clientes por nome.
        
        Args:
            nome (str): Nome do cliente
            
        Returns:
            List[Cliente]: Lista de clientes com o nome especificado
        """
        return Cliente.query.filter(Cliente.nome.ilike(f'%{nome}%')).all()
    
    def save(self, cliente: Cliente) -> Cliente:
        """
        Salva um cliente.
        
        Args:
            cliente (Cliente): Cliente a ser salvo
            
        Returns:
            Cliente: Cliente salvo
        """
        self.db.session.add(cliente)
        self.db.session.commit()
        return cliente
    
    def delete_by_id(self, cliente_id: int) -> bool:
        """
        Deleta um cliente por ID.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            bool: True se deletado com sucesso, False caso contrário
        """
        cliente = self.find_by_id(cliente_id)
        if cliente:
            self.db.session.delete(cliente)
            self.db.session.commit()
            return True
        return False
    
    def count(self) -> int:
        """
        Conta o número total de clientes.
        
        Returns:
            int: Número total de clientes
        """
        return Cliente.query.count()

