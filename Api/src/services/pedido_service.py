from typing import List, Optional, Dict, Any
from ..models.pedido import Pedido, ItemPedido
from ..models.pedido_repository import PedidoRepositoryInterface, PedidoRepository
from ..services.cliente_service import ClienteService
from ..services.produto_service import ProdutoService
from ..models.cliente_repository import ClienteRepository
from ..models.produto_repository import ProdutoRepository

class PedidoService:
    """
    Serviço para gerenciar a lógica de negócios relacionada a pedidos.
    """
    
    def __init__(self, pedido_repository: PedidoRepositoryInterface = None, 
                 cliente_service: ClienteService = None, 
                 produto_service: ProdutoService = None):
        """
        Inicializa o serviço de pedidos.
        
        Args:
            pedido_repository (PedidoRepositoryInterface): Repositório de pedidos
            cliente_service (ClienteService): Serviço de clientes
            produto_service (ProdutoService): Serviço de produtos
        """
        self.pedido_repository = pedido_repository or PedidoRepository()
        # Evita dependências circulares criando os serviços apenas quando necessário
        self._cliente_service = cliente_service
        self._produto_service = produto_service
    
    @property
    def cliente_service(self):
        """Lazy loading do cliente service."""
        if self._cliente_service is None:
            from ..models.cliente_repository import ClienteRepository
            from ..models.cliente import db
            self._cliente_service = ClienteService(ClienteRepository(db))
        return self._cliente_service
    
    @property
    def produto_service(self):
        """Lazy loading do produto service."""
        if self._produto_service is None:
            self._produto_service = ProdutoService()
        return self._produto_service
    
    def listar_todos(self) -> List[Pedido]:
        """
        Lista todos os pedidos.
        
        Returns:
            List[Pedido]: Lista com todos os pedidos
        """
        return self.pedido_repository.find_all()
    
    def buscar_por_id(self, pedido_id: int) -> Optional[Pedido]:
        """
        Busca um pedido por ID.
        
        Args:
            pedido_id (int): ID do pedido
            
        Returns:
            Optional[Pedido]: Pedido encontrado ou None
            
        Raises:
            ValueError: Se o ID for inválido
        """
        if not isinstance(pedido_id, int) or pedido_id <= 0:
            raise ValueError("ID do pedido deve ser um número positivo")
        
        return self.pedido_repository.find_by_id(pedido_id)
    
    def buscar_por_cliente_id(self, cliente_id: int) -> List[Pedido]:
        """
        Busca pedidos por ID do cliente.
        
        Args:
            cliente_id (int): ID do cliente
            
        Returns:
            List[Pedido]: Lista de pedidos encontrados
            
        Raises:
            ValueError: Se o ID do cliente for inválido
        """
        if not isinstance(cliente_id, int) or cliente_id <= 0:
            raise ValueError("ID do cliente deve ser um número positivo")
        
        return self.pedido_repository.find_by_cliente_id(cliente_id)
    
    def salvar(self, pedido_data: Dict[str, Any]) -> Pedido:
        """
        Salva um novo pedido.
        
        Args:
            pedido_data (Dict[str, Any]): Dados do pedido
            
        Returns:
            Pedido: Pedido salvo
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        self._validar_dados_pedido(pedido_data)
        
        # Verifica se o cliente existe
        cliente = self.cliente_service.buscar_por_id(pedido_data['cliente_id'])
        if not cliente:
            raise ValueError("Cliente não encontrado")
        
        # Cria o pedido
        pedido = Pedido.from_dict(pedido_data)
        
        # Processa os itens do pedido
        if 'itens' in pedido_data and pedido_data['itens']:
            total = 0.0
            for item_data in pedido_data['itens']:
                self._validar_dados_item_pedido(item_data)
                
                # Verifica se o produto existe e tem estoque suficiente
                produto = self.produto_service.buscar_por_id(item_data['produto_id'])
                if not produto:
                    raise ValueError(f"Produto {item_data['produto_id']} não encontrado")
                
                if produto.estoque < item_data['quantidade']:
                    raise ValueError(f"Estoque insuficiente para o produto {produto.nome}")
                
                # Usa o preço atual do produto se não fornecido
                preco_unitario = item_data.get('preco_unitario', produto.preco)
                
                # Cria o item do pedido
                item = ItemPedido(
                    pedido_id=None,  # Será definido após salvar o pedido
                    produto_id=item_data['produto_id'],
                    quantidade=item_data['quantidade'],
                    preco_unitario=preco_unitario
                )
                
                pedido.itens.append(item)
                total += item.quantidade * item.preco_unitario
            
            pedido.total = total
        
        return self.pedido_repository.save(pedido)
    
    def atualizar_status(self, pedido_id: int, novo_status: str) -> Pedido:
        """
        Atualiza o status de um pedido.
        
        Args:
            pedido_id (int): ID do pedido
            novo_status (str): Novo status do pedido
            
        Returns:
            Pedido: Pedido atualizado
            
        Raises:
            ValueError: Se o pedido não for encontrado ou status for inválido
        """
        pedido = self.buscar_por_id(pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")
        
        status_validos = ['pendente', 'processando', 'enviado', 'entregue', 'cancelado']
        if novo_status not in status_validos:
            raise ValueError(f"Status inválido. Deve ser um de: {', '.join(status_validos)}")
        
        pedido.status = novo_status
        return self.pedido_repository.save(pedido)
    
    def deletar(self, pedido_id: int) -> bool:
        """
        Deleta um pedido por ID.
        
        Args:
            pedido_id (int): ID do pedido a ser deletado
            
        Returns:
            bool: True se deletado com sucesso, False caso contrário
            
        Raises:
            ValueError: Se o ID for inválido
        """
        if not isinstance(pedido_id, int) or pedido_id <= 0:
            raise ValueError("ID do pedido deve ser um número positivo")
        
        return self.pedido_repository.delete_by_id(pedido_id)
    
    def contar_pedidos(self) -> int:
        """
        Conta o número total de pedidos.
        
        Returns:
            int: Número total de pedidos
        """
        return self.pedido_repository.count()
    
    def _validar_dados_pedido(self, pedido_data: Dict[str, Any]) -> None:
        """
        Valida os dados do pedido.
        
        Args:
            pedido_data (Dict[str, Any]): Dados do pedido
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        if not isinstance(pedido_data, dict):
            raise ValueError("Dados do pedido devem ser um dicionário")
        
        # Validação do cliente_id
        if 'cliente_id' not in pedido_data:
            raise ValueError("ID do cliente é obrigatório")
        
        try:
            cliente_id = int(pedido_data['cliente_id'])
            if cliente_id <= 0:
                raise ValueError("ID do cliente deve ser um número positivo")
        except (ValueError, TypeError):
            raise ValueError("ID do cliente deve ser um número válido")
        
        # Validação do status (opcional)
        if 'status' in pedido_data:
            status_validos = ['pendente', 'processando', 'enviado', 'entregue', 'cancelado']
            if pedido_data['status'] not in status_validos:
                raise ValueError(f"Status inválido. Deve ser um de: {', '.join(status_validos)}")
        
        # Validação dos itens (opcional, mas se fornecido deve ser válido)
        if 'itens' in pedido_data:
            if not isinstance(pedido_data['itens'], list):
                raise ValueError("Itens devem ser uma lista")
            
            if len(pedido_data['itens']) == 0:
                raise ValueError("Pedido deve ter pelo menos um item")
    
    def _validar_dados_item_pedido(self, item_data: Dict[str, Any]) -> None:
        """
        Valida os dados de um item do pedido.
        
        Args:
            item_data (Dict[str, Any]): Dados do item do pedido
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        if not isinstance(item_data, dict):
            raise ValueError("Dados do item devem ser um dicionário")
        
        # Validação do produto_id
        if 'produto_id' not in item_data:
            raise ValueError("ID do produto é obrigatório")
        
        try:
            produto_id = int(item_data['produto_id'])
            if produto_id <= 0:
                raise ValueError("ID do produto deve ser um número positivo")
        except (ValueError, TypeError):
            raise ValueError("ID do produto deve ser um número válido")
        
        # Validação da quantidade
        if 'quantidade' not in item_data:
            raise ValueError("Quantidade é obrigatória")
        
        try:
            quantidade = int(item_data['quantidade'])
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser um número positivo")
        except (ValueError, TypeError):
            raise ValueError("Quantidade deve ser um número inteiro válido")
        
        # Validação do preço unitário (opcional)
        if 'preco_unitario' in item_data:
            try:
                preco = float(item_data['preco_unitario'])
                if preco < 0:
                    raise ValueError("Preço unitário deve ser um valor não negativo")
            except (ValueError, TypeError):
                raise ValueError("Preço unitário deve ser um número válido")

