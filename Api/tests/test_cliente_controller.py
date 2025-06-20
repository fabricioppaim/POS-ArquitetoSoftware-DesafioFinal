import unittest
import json
import sys
import os

# Adiciona o diretório raiz do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app
from src.models.cliente import db

class TestClienteController(unittest.TestCase):
    """
    Testes de integração para o controller de clientes.
    """
    
    def setUp(self):
        """
        Configuração inicial para cada teste.
        """
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        with app.app_context():
            db.drop_all()
    
    def test_health_check(self):
        """
        Testa o endpoint de verificação de saúde.
        """
        response = self.app.get('/api/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'OK')
        self.assertIn('API de Clientes', data['message'])
    
    def test_create_cliente_valid(self):
        """
        Testa a criação de cliente com dados válidos.
        """
        cliente_data = {
            'nome': 'João Silva',
            'email': 'joao.silva@email.com'
        }
        
        response = self.app.post('/api/clientes',
                                data=json.dumps(cliente_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['nome'], cliente_data['nome'])
        self.assertEqual(data['email'], cliente_data['email'])
        self.assertIsNotNone(data['id'])
    
    def test_create_cliente_invalid_data(self):
        """
        Testa a criação de cliente com dados inválidos.
        """
        cliente_data = {
            'nome': '',
            'email': 'joao.silva@email.com'
        }
        
        response = self.app.post('/api/clientes',
                                data=json.dumps(cliente_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('erro', data)
    
    def test_create_cliente_no_json(self):
        """
        Testa a criação de cliente sem dados JSON.
        """
        response = self.app.post('/api/clientes')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['erro'], 'Content-Type deve ser application/json')
    
    def test_get_all_clientes_empty(self):
        """
        Testa a listagem de clientes quando não há nenhum.
        """
        response = self.app.get('/api/clientes')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)
    
    def test_get_all_clientes_with_data(self):
        """
        Testa a listagem de clientes com dados.
        """
        # Cria dois clientes
        cliente1_data = {'nome': 'João Silva', 'email': 'joao.silva@email.com'}
        cliente2_data = {'nome': 'Maria Santos', 'email': 'maria.santos@email.com'}
        
        self.app.post('/api/clientes',
                     data=json.dumps(cliente1_data),
                     content_type='application/json')
        self.app.post('/api/clientes',
                     data=json.dumps(cliente2_data),
                     content_type='application/json')
        
        response = self.app.get('/api/clientes')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
    
    def test_get_cliente_by_id_existing(self):
        """
        Testa a busca de cliente por ID existente.
        """
        # Cria um cliente
        cliente_data = {'nome': 'João Silva', 'email': 'joao.silva@email.com'}
        create_response = self.app.post('/api/clientes',
                                       data=json.dumps(cliente_data),
                                       content_type='application/json')
        created_cliente = json.loads(create_response.data)
        
        response = self.app.get(f'/api/clientes/{created_cliente["id"]}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], created_cliente['id'])
        self.assertEqual(data['nome'], cliente_data['nome'])
    
    def test_get_cliente_by_id_non_existing(self):
        """
        Testa a busca de cliente por ID inexistente.
        """
        response = self.app.get('/api/clientes/999')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['erro'], 'Cliente não encontrado')
    
    def test_get_cliente_by_nome(self):
        """
        Testa a busca de cliente por nome.
        """
        # Cria um cliente
        cliente_data = {'nome': 'João Silva', 'email': 'joao.silva@email.com'}
        self.app.post('/api/clientes',
                     data=json.dumps(cliente_data),
                     content_type='application/json')
        
        response = self.app.get('/api/clientes/nome/João')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nome'], cliente_data['nome'])
    
    def test_count_clientes(self):
        """
        Testa a contagem de clientes.
        """
        # Cria dois clientes
        cliente1_data = {'nome': 'João Silva', 'email': 'joao.silva@email.com'}
        cliente2_data = {'nome': 'Maria Santos', 'email': 'maria.santos@email.com'}
        
        self.app.post('/api/clientes',
                     data=json.dumps(cliente1_data),
                     content_type='application/json')
        self.app.post('/api/clientes',
                     data=json.dumps(cliente2_data),
                     content_type='application/json')
        
        response = self.app.get('/api/clientes/contar')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total'], 2)
    
    def test_update_cliente_existing(self):
        """
        Testa a atualização de cliente existente.
        """
        # Cria um cliente
        cliente_data = {'nome': 'João Silva', 'email': 'joao.silva@email.com'}
        create_response = self.app.post('/api/clientes',
                                       data=json.dumps(cliente_data),
                                       content_type='application/json')
        created_cliente = json.loads(create_response.data)
        
        # Atualiza o cliente
        updated_data = {'nome': 'João Silva Atualizado', 'email': 'joao.novo@email.com'}
        response = self.app.put(f'/api/clientes/{created_cliente["id"]}',
                               data=json.dumps(updated_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['nome'], updated_data['nome'])
        self.assertEqual(data['email'], updated_data['email'])
    
    def test_update_cliente_non_existing(self):
        """
        Testa a atualização de cliente inexistente.
        """
        updated_data = {'nome': 'João Silva', 'email': 'joao@email.com'}
        response = self.app.put('/api/clientes/999',
                               data=json.dumps(updated_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('erro', data)
    
    def test_delete_cliente_existing(self):
        """
        Testa a exclusão de cliente existente.
        """
        # Cria um cliente
        cliente_data = {'nome': 'João Silva', 'email': 'joao.silva@email.com'}
        create_response = self.app.post('/api/clientes',
                                       data=json.dumps(cliente_data),
                                       content_type='application/json')
        created_cliente = json.loads(create_response.data)
        
        # Deleta o cliente
        response = self.app.delete(f'/api/clientes/{created_cliente["id"]}')
        
        self.assertEqual(response.status_code, 204)
        
        # Verifica se foi deletado
        get_response = self.app.get(f'/api/clientes/{created_cliente["id"]}')
        self.assertEqual(get_response.status_code, 404)
    
    def test_delete_cliente_non_existing(self):
        """
        Testa a exclusão de cliente inexistente.
        """
        response = self.app.delete('/api/clientes/999')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['erro'], 'Cliente não encontrado')

if __name__ == '__main__':
    unittest.main()

