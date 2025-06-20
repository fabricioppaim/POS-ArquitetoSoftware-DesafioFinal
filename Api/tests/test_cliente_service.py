import unittest
from unittest.mock import Mock
import sys
import os

# Adiciona o diretório raiz do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.cliente import Cliente
from src.services.cliente_service import ClienteService

class TestClienteService(unittest.TestCase):
    """
    Testes unitários para a classe ClienteService.
    """
    
    def setUp(self):
        """
        Configuração inicial para cada teste.
        """
        self.mock_repository = Mock()
        self.service = ClienteService(self.mock_repository)
        
        # Mock de clientes para testes
        self.cliente1 = Cliente('João Silva', 'joao.silva@email.com')
        self.cliente1.id = 1
        
        self.cliente2 = Cliente('Maria Santos', 'maria.santos@email.com')
        self.cliente2.id = 2
        
        self.valid_cliente_data = {
            'nome': 'Pedro Costa',
            'email': 'pedro.costa@email.com'
        }
    
    def test_listar_todos(self):
        """
        Testa a listagem de todos os clientes.
        """
        self.mock_repository.find_all.return_value = [self.cliente1, self.cliente2]
        
        result = self.service.listar_todos()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], self.cliente1)
        self.assertEqual(result[1], self.cliente2)
        self.mock_repository.find_all.assert_called_once()
    
    def test_buscar_por_id_valid(self):
        """
        Testa a busca por ID válido.
        """
        self.mock_repository.find_by_id.return_value = self.cliente1
        
        result = self.service.buscar_por_id(1)
        
        self.assertEqual(result, self.cliente1)
        self.mock_repository.find_by_id.assert_called_once_with(1)
    
    def test_buscar_por_id_invalid(self):
        """
        Testa a busca por ID inválido.
        """
        with self.assertRaises(ValueError) as context:
            self.service.buscar_por_id(0)
        
        self.assertEqual(str(context.exception), "ID do cliente deve ser um número positivo")
        self.mock_repository.find_by_id.assert_not_called()
    
    def test_buscar_por_nome_valid(self):
        """
        Testa a busca por nome válido.
        """
        self.mock_repository.find_by_nome.return_value = [self.cliente1]
        
        result = self.service.buscar_por_nome('João')
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.cliente1)
        self.mock_repository.find_by_nome.assert_called_once_with('João')
    
    def test_buscar_por_nome_empty(self):
        """
        Testa a busca por nome vazio.
        """
        with self.assertRaises(ValueError) as context:
            self.service.buscar_por_nome('')
        
        self.assertEqual(str(context.exception), "Nome não pode ser vazio")
        self.mock_repository.find_by_nome.assert_not_called()
    
    def test_salvar_new_cliente_valid(self):
        """
        Testa o salvamento de novo cliente com dados válidos.
        """
        self.mock_repository.find_all.return_value = []
        self.mock_repository.save.return_value = self.cliente1
        
        result = self.service.salvar(self.valid_cliente_data)
        
        self.assertEqual(result, self.cliente1)
        self.mock_repository.save.assert_called_once()
    
    def test_salvar_cliente_invalid_data(self):
        """
        Testa o salvamento com dados inválidos.
        """
        invalid_data = {'nome': '', 'email': 'test@email.com'}
        
        with self.assertRaises(ValueError) as context:
            self.service.salvar(invalid_data)
        
        self.assertEqual(str(context.exception), "Nome é obrigatório")
        self.mock_repository.save.assert_not_called()
    
    def test_salvar_cliente_invalid_email(self):
        """
        Testa o salvamento com email inválido.
        """
        invalid_data = {'nome': 'João', 'email': 'email_invalido'}
        
        with self.assertRaises(ValueError) as context:
            self.service.salvar(invalid_data)
        
        self.assertEqual(str(context.exception), "Email deve ter um formato válido")
        self.mock_repository.save.assert_not_called()
    
    def test_salvar_cliente_duplicate_email(self):
        """
        Testa o salvamento com email duplicado.
        """
        existing_cliente = Cliente('Outro Cliente', 'pedro.costa@email.com')
        self.mock_repository.find_all.return_value = [existing_cliente]
        
        with self.assertRaises(ValueError) as context:
            self.service.salvar(self.valid_cliente_data)
        
        self.assertEqual(str(context.exception), "Já existe um cliente com este email")
        self.mock_repository.save.assert_not_called()
    
    def test_deletar_valid_id(self):
        """
        Testa a exclusão com ID válido.
        """
        self.mock_repository.delete_by_id.return_value = True
        
        result = self.service.deletar(1)
        
        self.assertTrue(result)
        self.mock_repository.delete_by_id.assert_called_once_with(1)
    
    def test_deletar_invalid_id(self):
        """
        Testa a exclusão com ID inválido.
        """
        with self.assertRaises(ValueError) as context:
            self.service.deletar(0)
        
        self.assertEqual(str(context.exception), "ID do cliente deve ser um número positivo")
        self.mock_repository.delete_by_id.assert_not_called()
    
    def test_contar_clientes(self):
        """
        Testa a contagem de clientes.
        """
        self.mock_repository.count.return_value = 10
        
        result = self.service.contar_clientes()
        
        self.assertEqual(result, 10)
        self.mock_repository.count.assert_called_once()
    
    def test_validar_dados_cliente_nome_muito_curto(self):
        """
        Testa validação com nome muito curto.
        """
        invalid_data = {'nome': 'A', 'email': 'test@email.com'}
        
        with self.assertRaises(ValueError) as context:
            self.service.salvar(invalid_data)
        
        self.assertEqual(str(context.exception), "Nome deve ter pelo menos 2 caracteres")
    
    def test_validar_dados_cliente_nome_muito_longo(self):
        """
        Testa validação com nome muito longo.
        """
        invalid_data = {'nome': 'A' * 101, 'email': 'test@email.com'}
        
        with self.assertRaises(ValueError) as context:
            self.service.salvar(invalid_data)
        
        self.assertEqual(str(context.exception), "Nome deve ter no máximo 100 caracteres")
    
    def test_validar_dados_cliente_email_muito_longo(self):
        """
        Testa validação com email muito longo.
        """
        invalid_data = {'nome': 'João', 'email': 'A' * 121}
        
        with self.assertRaises(ValueError) as context:
            self.service.salvar(invalid_data)
        
        self.assertEqual(str(context.exception), "Email deve ter no máximo 120 caracteres")

if __name__ == '__main__':
    unittest.main()

