from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from ..services.pedido_service import PedidoService

# Criação do blueprint para as rotas de pedidos
pedido_bp = Blueprint('pedido', __name__)

# Instância do serviço de pedidos
pedido_service = PedidoService()

@pedido_bp.route('/pedidos', methods=['GET'])
@cross_origin()
def listar_pedidos():
    """
    Lista todos os pedidos.
    
    Returns:
        JSON: Lista de pedidos ou erro
    """
    try:
        pedidos = pedido_service.listar_todos()
        return jsonify([pedido.to_dict() for pedido in pedidos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@pedido_bp.route('/pedidos/<int:pedido_id>', methods=['GET'])
@cross_origin()
def buscar_pedido_por_id(pedido_id):
    """
    Busca um pedido por ID.
    
    Args:
        pedido_id (int): ID do pedido
        
    Returns:
        JSON: Dados do pedido ou erro
    """
    try:
        pedido = pedido_service.buscar_por_id(pedido_id)
        if pedido:
            return jsonify(pedido.to_dict()), 200
        else:
            return jsonify({'erro': 'Pedido não encontrado'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@pedido_bp.route('/pedidos/cliente/<int:cliente_id>', methods=['GET'])
@cross_origin()
def buscar_pedidos_por_cliente(cliente_id):
    """
    Busca pedidos por ID do cliente.
    
    Args:
        cliente_id (int): ID do cliente
        
    Returns:
        JSON: Lista de pedidos encontrados ou erro
    """
    try:
        pedidos = pedido_service.buscar_por_cliente_id(cliente_id)
        return jsonify([pedido.to_dict() for pedido in pedidos]), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@pedido_bp.route('/pedidos/contar', methods=['GET'])
@cross_origin()
def contar_pedidos():
    """
    Conta o número total de pedidos.
    
    Returns:
        JSON: Número total de pedidos ou erro
    """
    try:
        total = pedido_service.contar_pedidos()
        return jsonify({'total': total}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@pedido_bp.route('/pedidos', methods=['POST'])
@cross_origin()
def criar_pedido():
    """
    Cria um novo pedido.
    
    Returns:
        JSON: Dados do pedido criado ou erro
    """
    try:
        if not request.is_json:
            return jsonify({'erro': 'Content-Type deve ser application/json'}), 400
        
        if not request.json:
            return jsonify({'erro': 'Dados JSON são obrigatórios'}), 400
        
        pedido = pedido_service.salvar(request.json)
        return jsonify(pedido.to_dict()), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@pedido_bp.route('/pedidos/<int:pedido_id>/status', methods=['PUT'])
@cross_origin()
def atualizar_status_pedido(pedido_id):
    """
    Atualiza o status de um pedido.
    
    Args:
        pedido_id (int): ID do pedido
        
    Returns:
        JSON: Dados do pedido atualizado ou erro
    """
    try:
        if not request.is_json:
            return jsonify({'erro': 'Content-Type deve ser application/json'}), 400
        
        if not request.json or 'status' not in request.json:
            return jsonify({'erro': 'Status é obrigatório'}), 400
        
        pedido = pedido_service.atualizar_status(pedido_id, request.json['status'])
        return jsonify(pedido.to_dict()), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@pedido_bp.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
@cross_origin()
def deletar_pedido(pedido_id):
    """
    Deleta um pedido por ID.
    
    Args:
        pedido_id (int): ID do pedido a ser deletado
        
    Returns:
        JSON: Confirmação de exclusão ou erro
    """
    try:
        sucesso = pedido_service.deletar(pedido_id)
        if sucesso:
            return '', 204
        else:
            return jsonify({'erro': 'Pedido não encontrado'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

