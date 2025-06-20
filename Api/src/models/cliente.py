from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    """
    Modelo da entidade Cliente.
    
    Representa um cliente no sistema com informações básicas
    como ID, nome e email.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, nome, email):
        """
        Construtor da classe Cliente.
        
        Args:
            nome (str): Nome do cliente
            email (str): Email do cliente
        """
        self.nome = nome
        self.email = email

    def __repr__(self):
        """
        Representação string da instância Cliente.
        
        Returns:
            str: Representação do cliente
        """
        return f'<Cliente {self.nome}>'

    def to_dict(self):
        """
        Converte a instância Cliente para um dicionário.
        
        Returns:
            dict: Dicionário com os dados do cliente
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email
        }

    @staticmethod
    def from_dict(data):
        """
        Cria uma instância Cliente a partir de um dicionário.
        
        Args:
            data (dict): Dicionário com os dados do cliente
            
        Returns:
            Cliente: Nova instância de Cliente
        """
        return Cliente(
            nome=data.get('nome'),
            email=data.get('email')
        )

