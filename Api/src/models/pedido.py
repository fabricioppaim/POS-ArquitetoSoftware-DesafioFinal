from flask_sqlalchemy import SQLAlchemy
from typing import Dict, Any, Optional
from datetime import datetime

# Importa a instância db do módulo cliente para usar a mesma instância
from .cliente import db

class Pedido(db.Model):
    """
    Modelo para representar um pedido no sistema.
    
    Attributes:
        id (int): Identificador único do pedido
        cliente_id (int): ID do cliente que fez o pedido
        data_pedido (datetime): Data e hora do pedido
        status (str): Status do pedido (pendente, processando, enviado, entregue, cancelado)
        total (float): Valor total do pedido
    """
    
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, nullable=False)
    data_pedido = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='pendente')
    total = db.Column(db.Float, nullable=False, default=0.0)
    
    # Relacionamento com itens do pedido
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, cliente_id: int, status: str = 'pendente', total: float = 0.0):
        """
        Inicializa uma nova instância de Pedido.
        
        Args:
            cliente_id (int): ID do cliente
            status (str): Status do pedido
            total (float): Valor total do pedido
        """
        self.cliente_id = cliente_id
        self.status = status
        self.total = total
        self.data_pedido = datetime.utcnow()
    
    def __repr__(self) -> str:
        """
        Retorna uma representação string do pedido.
        
        Returns:
            str: Representação string do pedido
        """
        return f"<Pedido {self.id} - Cliente {self.cliente_id}>"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o pedido para um dicionário.
        
        Returns:
            Dict[str, Any]: Dicionário com os dados do pedido
        """
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'data_pedido': self.data_pedido.isoformat() if self.data_pedido else None,
            'status': self.status,
            'total': self.total,
            'itens': [item.to_dict() for item in self.itens] if self.itens else []
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pedido':
        """
        Cria uma instância de Pedido a partir de um dicionário.
        
        Args:
            data (Dict[str, Any]): Dicionário com os dados do pedido
            
        Returns:
            Pedido: Nova instância de Pedido
        """
        return cls(
            cliente_id=data.get('cliente_id'),
            status=data.get('status', 'pendente'),
            total=data.get('total', 0.0)
        )

class ItemPedido(db.Model):
    """
    Modelo para representar um item de pedido no sistema.
    
    Attributes:
        id (int): Identificador único do item
        pedido_id (int): ID do pedido ao qual o item pertence
        produto_id (int): ID do produto
        quantidade (int): Quantidade do produto no pedido
        preco_unitario (float): Preço unitário do produto no momento do pedido
    """
    
    __tablename__ = 'itens_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    
    def __init__(self, pedido_id: int, produto_id: int, quantidade: int, preco_unitario: float):
        """
        Inicializa uma nova instância de ItemPedido.
        
        Args:
            pedido_id (int): ID do pedido
            produto_id (int): ID do produto
            quantidade (int): Quantidade do produto
            preco_unitario (float): Preço unitário do produto
        """
        self.pedido_id = pedido_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
    
    def __repr__(self) -> str:
        """
        Retorna uma representação string do item do pedido.
        
        Returns:
            str: Representação string do item do pedido
        """
        return f"<ItemPedido {self.id} - Produto {self.produto_id}>"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o item do pedido para um dicionário.
        
        Returns:
            Dict[str, Any]: Dicionário com os dados do item do pedido
        """
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'produto_id': self.produto_id,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.quantidade * self.preco_unitario
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ItemPedido':
        """
        Cria uma instância de ItemPedido a partir de um dicionário.
        
        Args:
            data (Dict[str, Any]): Dicionário com os dados do item do pedido
            
        Returns:
            ItemPedido: Nova instância de ItemPedido
        """
        return cls(
            pedido_id=data.get('pedido_id'),
            produto_id=data.get('produto_id'),
            quantidade=data.get('quantidade'),
            preco_unitario=data.get('preco_unitario')
        )

