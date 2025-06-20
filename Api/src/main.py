import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.cliente import db
from src.models.produto import Produto
from src.models.pedido import Pedido, ItemPedido
from src.routes.cliente import cliente_bp
from src.routes.produto import produto_bp
from src.routes.pedido import pedido_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configuração do CORS para permitir requisições de qualquer origem
CORS(app)

# Registro dos blueprints para as rotas
app.register_blueprint(cliente_bp, url_prefix='/api')
app.register_blueprint(produto_bp, url_prefix='/api')
app.register_blueprint(pedido_bp, url_prefix='/api')

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Criação das tabelas do banco de dados
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
    Serve arquivos estáticos e a página index.html.
    
    Args:
        path (str): Caminho do arquivo solicitado
        
    Returns:
        Response: Arquivo solicitado ou index.html
    """
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificação de saúde da API.
    
    Returns:
        JSON: Status da API
    """
    return {'status': 'OK', 'message': 'API Multi-domínio (Clientes, Produtos, Pedidos) está funcionando'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
