import unittest
import sys
import os

# Adiciona o diretório raiz do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.cliente import Cliente

class TestCliente(unittest.TestCase):
    """
    Testes unitários para a classe Cliente.
    """
    
    def setUp(self):
        """
        Configuração inicial para cada teste.
        """
        self.cliente_data = {
            'nome': 'João Silva',
            'email': 'joao.silva@email.com'
        }
    
    def test_cliente_creation(self):
        """
        Testa a criação de uma instância de Cliente.
        """
        cliente = Cliente(
            nome=self.cliente_data['nome'],
            email=self.cliente_data['email']
        )
        
        self.assertEqual(cliente.nome, self.cliente_data['nome'])
        self.assertEqual(cliente.email, self.cliente_data['email'])
        self.assertIsNone(cliente.id)  # ID é None antes de salvar no banco
    
    def test_cliente_repr(self):
        """
        Testa a representação string do Cliente.
        """
        cliente = Cliente(
            nome=self.cliente_data['nome'],
            email=self.cliente_data['email']
        )
        
        expected_repr = f"<Cliente {self.cliente_data['nome']}>"
        self.assertEqual(repr(cliente), expected_repr)
    
    def test_cliente_to_dict(self):
        """
        Testa a conversão do Cliente para dicionário.
        """
        cliente = Cliente(
            nome=self.cliente_data['nome'],
            email=self.cliente_data['email']
        )
        cliente.id = 1  # Simula um ID atribuído pelo banco
        
        expected_dict = {
            'id': 1,
            'nome': self.cliente_data['nome'],
            'email': self.cliente_data['email']
        }
        
        self.assertEqual(cliente.to_dict(), expected_dict)
    
    def test_cliente_from_dict(self):
        """
        Testa a criação de Cliente a partir de dicionário.
        """
        cliente = Cliente.from_dict(self.cliente_data)
        
        self.assertEqual(cliente.nome, self.cliente_data['nome'])
        self.assertEqual(cliente.email, self.cliente_data['email'])
        self.assertIsNone(cliente.id)
    
    def test_cliente_from_dict_with_missing_data(self):
        """
        Testa a criação de Cliente com dados faltando.
        """
        incomplete_data = {'nome': 'João Silva'}
        cliente = Cliente.from_dict(incomplete_data)
        
        self.assertEqual(cliente.nome, 'João Silva')
        self.assertIsNone(cliente.email)

if __name__ == '__main__':
    unittest.main()

