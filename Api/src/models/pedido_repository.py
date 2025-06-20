from abc import ABC, abstractmethod
from typing import List, Optional
from .pedido import Pedido, ItemPedido, db

class PedidoRepositoryInterface(ABC):
    """
    Interface para o repositório de pedidos.
    Define os métodos que devem ser implementados por qualquer repositório de pedidos.
    """
    
    @abstractmethod
    def find_all(self) -> List[Pedido]:
        """
        Busca todos os pedidos.
        
        Returns:
            List[Pedido]: Lista com todos os pedidos
        """
        pass
    
    @abstractmethod
    def find_by_id(self, pedido_id: int) -> Optional[Pedido]:
        """
        Busca um pedido por ID.
        
        Args:
            pedido_id (int): ID do pedido
            
        Returns:
            Optional[Pedido]: Pedido encontrado ou None
        """
        pass
    
    @abstractmethod
    def find_by_cliente_id(self, cliente_id: int) -> List[Pedido]:
        """
        Busca pedidos por ID do cliente.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            List[Pedido]: Lista de pedidos encontrados
        """
        pass
    
    @abstractmethod
    def save(self, pedido: Pedido) -> Pedido:
        """
        Salva um pedido no repositório.
        
        Args:
            pedido (Pedido): Pedido a ser salvo
            
        Returns:
            Pedido: Pedido salvo
        """
        pass
    
    @abstractmethod
    def delete_by_id(self, pedido_id: int) -> bool:
        """
        Deleta um pedido por ID.
        
        Args:
            pedido_id (int): ID do pedido a ser deletado
            
        Returns:
            bool: True se deletado com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    def count(self) -> int:
        """
        Conta o número total de pedidos.
        
        Returns:
            int: Número total de pedidos
        """
        pass

class PedidoRepository(PedidoRepositoryInterface):
    """
    Implementação concreta do repositório de pedidos usando SQLAlchemy.
    """
    
    def __init__(self, database=None):
        """
        Inicializa o repositório de pedidos.
        
        Args:
            database: Instância do banco de dados (para injeção de dependência em testes)
        """
        self.db = database or db
    
    def find_all(self) -> List[Pedido]:
        """
        Busca todos os pedidos.
        
        Returns:
            List[Pedido]: Lista com todos os pedidos
        """
        return Pedido.query.all()
    
    def find_by_id(self, pedido_id: int) -> Optional[Pedido]:
        """
        Busca um pedido por ID.
        
        Args:
            pedido_id (int): ID do pedido
            
        Returns:
            Optional[Pedido]: Pedido encontrado ou None
        """
        return Pedido.query.get(pedido_id)
    
    def find_by_cliente_id(self, cliente_id: int) -> List[Pedido]:
        """
        Busca pedidos por ID do cliente.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            List[Pedido]: Lista de pedidos encontrados
        """
        return Pedido.query.filter_by(cliente_id=cliente_id).all()
    
    def save(self, pedido: Pedido) -> Pedido:
        """
        Salva um pedido no repositório.
        
        Args:
            pedido (Pedido): Pedido a ser salvo
            
        Returns:
            Pedido: Pedido salvo
        """
        self.db.session.add(pedido)
        self.db.session.commit()
        return pedido
    
    def delete_by_id(self, pedido_id: int) -> bool:
        """
        Deleta um pedido por ID.
        
        Args:
            pedido_id (int): ID do pedido a ser deletado
            
        Returns:
            bool: True se deletado com sucesso, False caso contrário
        """
        pedido = self.find_by_id(pedido_id)
        if pedido:
            self.db.session.delete(pedido)
            self.db.session.commit()
            return True
        return False
    
    def count(self) -> int:
        """
        Conta o número total de pedidos.
        
        Returns:
            int: Número total de pedidos
        """
        return Pedido.query.count()

