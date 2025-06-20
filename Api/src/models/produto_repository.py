from abc import ABC, abstractmethod
from typing import List, Optional
from .produto import Produto, db

class ProdutoRepositoryInterface(ABC):
    """
    Interface para o repositório de produtos.
    Define os métodos que devem ser implementados por qualquer repositório de produtos.
    """
    
    @abstractmethod
    def find_all(self) -> List[Produto]:
        """
        Busca todos os produtos.
        
        Returns:
            List[Produto]: Lista com todos os produtos
        """
        pass
    
    @abstractmethod
    def find_by_id(self, produto_id: int) -> Optional[Produto]:
        """
        Busca um produto por ID.
        
        Args:
            produto_id (int): ID do produto
            
        Returns:
            Optional[Produto]: Produto encontrado ou None
        """
        pass
    
    @abstractmethod
    def find_by_nome(self, nome: str) -> List[Produto]:
        """
        Busca produtos por nome (busca parcial).
        
        Args:
            nome (str): Nome ou parte do nome do produto
            
        Returns:
            List[Produto]: Lista de produtos encontrados
        """
        pass
    
    @abstractmethod
    def save(self, produto: Produto) -> Produto:
        """
        Salva um produto no repositório.
        
        Args:
            produto (Produto): Produto a ser salvo
            
        Returns:
            Produto: Produto salvo
        """
        pass
    
    @abstractmethod
    def delete_by_id(self, produto_id: int) -> bool:
        """
        Deleta um produto por ID.
        
        Args:
            produto_id (int): ID do produto a ser deletado
            
        Returns:
            bool: True se deletado com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    def count(self) -> int:
        """
        Conta o número total de produtos.
        
        Returns:
            int: Número total de produtos
        """
        pass

class ProdutoRepository(ProdutoRepositoryInterface):
    """
    Implementação concreta do repositório de produtos usando SQLAlchemy.
    """
    
    def __init__(self, database=None):
        """
        Inicializa o repositório de produtos.
        
        Args:
            database: Instância do banco de dados (para injeção de dependência em testes)
        """
        self.db = database or db
    
    def find_all(self) -> List[Produto]:
        """
        Busca todos os produtos.
        
        Returns:
            List[Produto]: Lista com todos os produtos
        """
        return Produto.query.all()
    
    def find_by_id(self, produto_id: int) -> Optional[Produto]:
        """
        Busca um produto por ID.
        
        Args:
            produto_id (int): ID do produto
            
        Returns:
            Optional[Produto]: Produto encontrado ou None
        """
        return Produto.query.get(produto_id)
    
    def find_by_nome(self, nome: str) -> List[Produto]:
        """
        Busca produtos por nome (busca parcial, case-insensitive).
        
        Args:
            nome (str): Nome ou parte do nome do produto
            
        Returns:
            List[Produto]: Lista de produtos encontrados
        """
        return Produto.query.filter(Produto.nome.ilike(f'%{nome}%')).all()
    
    def save(self, produto: Produto) -> Produto:
        """
        Salva um produto no repositório.
        
        Args:
            produto (Produto): Produto a ser salvo
            
        Returns:
            Produto: Produto salvo
        """
        self.db.session.add(produto)
        self.db.session.commit()
        return produto
    
    def delete_by_id(self, produto_id: int) -> bool:
        """
        Deleta um produto por ID.
        
        Args:
            produto_id (int): ID do produto a ser deletado
            
        Returns:
            bool: True se deletado com sucesso, False caso contrário
        """
        produto = self.find_by_id(produto_id)
        if produto:
            self.db.session.delete(produto)
            self.db.session.commit()
            return True
        return False
    
    def count(self) -> int:
        """
        Conta o número total de produtos.
        
        Returns:
            int: Número total de produtos
        """
        return Produto.query.count()

