from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from ..services.produto_service import ProdutoService

# Criação do blueprint para as rotas de produtos
produto_bp = Blueprint('produto', __name__)

# Instância do serviço de produtos
produto_service = ProdutoService()

@produto_bp.route('/produtos', methods=['GET'])
@cross_origin()
def listar_produtos():
    """
    Lista todos os produtos.
    
    Returns:
        JSON: Lista de produtos ou erro
    """
    try:
        produtos = produto_service.listar_todos()
        return jsonify([produto.to_dict() for produto in produtos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['GET'])
@cross_origin()
def buscar_produto_por_id(produto_id):
    """
    Busca um produto por ID.
    
    Args:
        produto_id (int): ID do produto
        
    Returns:
        JSON: Dados do produto ou erro
    """
    try:
        produto = produto_service.buscar_por_id(produto_id)
        if produto:
            return jsonify(produto.to_dict()), 200
        else:
            return jsonify({'erro': 'Produto não encontrado'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/nome/<string:nome>', methods=['GET'])
@cross_origin()
def buscar_produtos_por_nome(nome):
    """
    Busca produtos por nome.
    
    Args:
        nome (str): Nome ou parte do nome do produto
        
    Returns:
        JSON: Lista de produtos encontrados ou erro
    """
    try:
        produtos = produto_service.buscar_por_nome(nome)
        return jsonify([produto.to_dict() for produto in produtos]), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/contar', methods=['GET'])
@cross_origin()
def contar_produtos():
    """
    Conta o número total de produtos.
    
    Returns:
        JSON: Número total de produtos ou erro
    """
    try:
        total = produto_service.contar_produtos()
        return jsonify({'total': total}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos', methods=['POST'])
@cross_origin()
def criar_produto():
    """
    Cria um novo produto.
    
    Returns:
        JSON: Dados do produto criado ou erro
    """
    try:
        if not request.is_json:
            return jsonify({'erro': 'Content-Type deve ser application/json'}), 400
        
        if not request.json:
            return jsonify({'erro': 'Dados JSON são obrigatórios'}), 400
        
        produto = produto_service.salvar(request.json)
        return jsonify(produto.to_dict()), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['PUT'])
@cross_origin()
def atualizar_produto(produto_id):
    """
    Atualiza um produto existente.
    
    Args:
        produto_id (int): ID do produto a ser atualizado
        
    Returns:
        JSON: Dados do produto atualizado ou erro
    """
    try:
        if not request.is_json:
            return jsonify({'erro': 'Content-Type deve ser application/json'}), 400
        
        if not request.json:
            return jsonify({'erro': 'Dados JSON são obrigatórios'}), 400
        
        # Adiciona o ID aos dados para atualização
        produto_data = request.json.copy()
        produto_data['id'] = produto_id
        
        produto = produto_service.salvar(produto_data)
        return jsonify(produto.to_dict()), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@produto_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
@cross_origin()
def deletar_produto(produto_id):
    """
    Deleta um produto por ID.
    
    Args:
        produto_id (int): ID do produto a ser deletado
        
    Returns:
        JSON: Confirmação de exclusão ou erro
    """
    try:
        sucesso = produto_service.deletar(produto_id)
        if sucesso:
            return '', 204
        else:
            return jsonify({'erro': 'Produto não encontrado'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

