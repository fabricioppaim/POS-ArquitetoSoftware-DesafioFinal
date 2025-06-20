from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.models.cliente import db
from src.models.cliente_repository import ClienteRepository
from src.services.cliente_service import ClienteService

# Criação do blueprint para as rotas de clientes
cliente_bp = Blueprint('cliente', __name__)

# Inicialização do repositório e serviço
cliente_repository = ClienteRepository(db)
cliente_service = ClienteService(cliente_repository)

@cliente_bp.route('/clientes', methods=['GET'])
@cross_origin()
def listar_todos_clientes():
    """
    Lista todos os clientes.
    
    Returns:
        JSON: Lista de todos os clientes
    """
    try:
        clientes = cliente_service.listar_todos()
        return jsonify([cliente.to_dict() for cliente in clientes]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
@cross_origin()
def buscar_cliente_por_id(cliente_id):
    """
    Busca um cliente por ID.
    
    Args:
        cliente_id (int): ID do cliente
        
    Returns:
        JSON: Dados do cliente ou erro
    """
    try:
        cliente = cliente_service.buscar_por_id(cliente_id)
        if cliente:
            return jsonify(cliente.to_dict()), 200
        else:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/nome/<string:nome>', methods=['GET'])
@cross_origin()
def buscar_clientes_por_nome(nome):
    """
    Busca clientes por nome.
    
    Args:
        nome (str): Nome do cliente
        
    Returns:
        JSON: Lista de clientes com o nome especificado
    """
    try:
        clientes = cliente_service.buscar_por_nome(nome)
        return jsonify([cliente.to_dict() for cliente in clientes]), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/contar', methods=['GET'])
@cross_origin()
def contar_clientes():
    """
    Conta o número total de clientes.
    
    Returns:
        JSON: Número total de clientes
    """
    try:
        total = cliente_service.contar_clientes()
        return jsonify({'total': total}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes', methods=['POST'])
@cross_origin()
def criar_cliente():
    """
    Cria um novo cliente.
    
    Returns:
        JSON: Dados do cliente criado ou erro
    """
    try:
        if not request.is_json:
            return jsonify({'erro': 'Content-Type deve ser application/json'}), 400
        
        if not request.json:
            return jsonify({'erro': 'Dados JSON são obrigatórios'}), 400
        
        cliente = cliente_service.salvar(request.json)
        return jsonify(cliente.to_dict()), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
@cross_origin()
def atualizar_cliente(cliente_id):
    """
    Atualiza um cliente existente.
    
    Args:
        cliente_id (int): ID do cliente
        
    Returns:
        JSON: Dados do cliente atualizado ou erro
    """
    try:
        if not request.json:
            return jsonify({'erro': 'Dados JSON são obrigatórios'}), 400
        
        dados_cliente = request.json.copy()
        dados_cliente['id'] = cliente_id
        
        cliente = cliente_service.salvar(dados_cliente)
        return jsonify(cliente.to_dict()), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
@cross_origin()
def deletar_cliente(cliente_id):
    """
    Deleta um cliente por ID.
    
    Args:
        cliente_id (int): ID do cliente
        
    Returns:
        JSON: Confirmação de deleção ou erro
    """
    try:
        sucesso = cliente_service.deletar(cliente_id)
        if sucesso:
            return '', 204
        else:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

