import unittest
from unittest.mock import Mock, MagicMock
import sys
import os

# Adiciona o diretório raiz do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.cliente import Cliente
from src.models.cliente_repository import ClienteRepository

class TestClienteRepository(unittest.TestCase):
    """
    Testes unitários para a classe ClienteRepository.
    """
    
    def setUp(self):
        """
        Configuração inicial para cada teste.
        """
        self.mock_db = Mock()
        self.repository = ClienteRepository(self.mock_db)
        
        # Mock de clientes para testes
        self.cliente1 = Cliente('João Silva', 'joao.silva@email.com')
        self.cliente1.id = 1
        
        self.cliente2 = Cliente('Maria Santos', 'maria.santos@email.com')
        self.cliente2.id = 2
    
    def test_find_all(self):
        """
        Testa a busca de todos os clientes.
        """
        # Mock do retorno da query
        Cliente.query = Mock()
        Cliente.query.all.return_value = [self.cliente1, self.cliente2]
        
        result = self.repository.find_all()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], self.cliente1)
        self.assertEqual(result[1], self.cliente2)
        Cliente.query.all.assert_called_once()
    
    def test_find_by_id_existing(self):
        """
        Testa a busca por ID de cliente existente.
        """
        # Mock do retorno da query
        Cliente.query = Mock()
        Cliente.query.get.return_value = self.cliente1
        
        result = self.repository.find_by_id(1)
        
        self.assertEqual(result, self.cliente1)
        Cliente.query.get.assert_called_once_with(1)
    
    def test_find_by_id_non_existing(self):
        """
        Testa a busca por ID de cliente inexistente.
        """
        # Mock do retorno da query
        Cliente.query = Mock()
        Cliente.query.get.return_value = None
        
        result = self.repository.find_by_id(999)
        
        self.assertIsNone(result)
        Cliente.query.get.assert_called_once_with(999)
    
    def test_find_by_nome(self):
        """
        Testa a busca por nome.
        """
        # Mock do retorno da query
        Cliente.query = Mock()
        mock_filter = Mock()
        Cliente.query.filter.return_value = mock_filter
        mock_filter.all.return_value = [self.cliente1]
        
        result = self.repository.find_by_nome('João')
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.cliente1)
        Cliente.query.filter.assert_called_once()
        mock_filter.all.assert_called_once()
    
    def test_save_new_cliente(self):
        """
        Testa o salvamento de um novo cliente.
        """
        new_cliente = Cliente('Pedro Costa', 'pedro.costa@email.com')
        
        result = self.repository.save(new_cliente)
        
        self.mock_db.session.add.assert_called_once_with(new_cliente)
        self.mock_db.session.commit.assert_called_once()
        self.assertEqual(result, new_cliente)
    
    def test_delete_by_id_existing(self):
        """
        Testa a exclusão de cliente existente.
        """
        # Mock do find_by_id
        self.repository.find_by_id = Mock(return_value=self.cliente1)
        
        result = self.repository.delete_by_id(1)
        
        self.assertTrue(result)
        self.mock_db.session.delete.assert_called_once_with(self.cliente1)
        self.mock_db.session.commit.assert_called_once()
    
    def test_delete_by_id_non_existing(self):
        """
        Testa a exclusão de cliente inexistente.
        """
        # Mock do find_by_id
        self.repository.find_by_id = Mock(return_value=None)
        
        result = self.repository.delete_by_id(999)
        
        self.assertFalse(result)
        self.mock_db.session.delete.assert_not_called()
        self.mock_db.session.commit.assert_not_called()
    
    def test_count(self):
        """
        Testa a contagem de clientes.
        """
        # Mock do retorno da query
        Cliente.query = Mock()
        Cliente.query.count.return_value = 5
        
        result = self.repository.count()
        
        self.assertEqual(result, 5)
        Cliente.query.count.assert_called_once()

if __name__ == '__main__':
    unittest.main()

