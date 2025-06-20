from flask_sqlalchemy import SQLAlchemy
from typing import Dict, Any, Optional

# Importa a instância db do módulo cliente para usar a mesma instância
from .cliente import db

class Produto(db.Model):
    """
    Modelo para representar um produto no sistema.
    
    Attributes:
        id (int): Identificador único do produto
        nome (str): Nome do produto
        descricao (str): Descrição detalhada do produto
        preco (float): Preço do produto
        estoque (int): Quantidade em estoque
    """
    
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)
    
    def __init__(self, nome: str, descricao: str = None, preco: float = 0.0, estoque: int = 0):
        """
        Inicializa uma nova instância de Produto.
        
        Args:
            nome (str): Nome do produto
            descricao (str, optional): Descrição do produto
            preco (float): Preço do produto
            estoque (int): Quantidade em estoque
        """
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
    
    def __repr__(self) -> str:
        """
        Retorna uma representação string do produto.
        
        Returns:
            str: Representação string do produto
        """
        return f"<Produto {self.nome}>"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o produto para um dicionário.
        
        Returns:
            Dict[str, Any]: Dicionário com os dados do produto
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'estoque': self.estoque
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Produto':
        """
        Cria uma instância de Produto a partir de um dicionário.
        
        Args:
            data (Dict[str, Any]): Dicionário com os dados do produto
            
        Returns:
            Produto: Nova instância de Produto
        """
        return cls(
            nome=data.get('nome'),
            descricao=data.get('descricao'),
            preco=data.get('preco', 0.0),
            estoque=data.get('estoque', 0)
        )

