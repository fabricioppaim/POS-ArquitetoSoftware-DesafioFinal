from typing import List, Optional, Dict, Any
from ..models.produto import Produto
from ..models.produto_repository import ProdutoRepositoryInterface, ProdutoRepository

class ProdutoService:
    """
    Serviço para gerenciar a lógica de negócios relacionada a produtos.
    """
    
    def __init__(self, produto_repository: ProdutoRepositoryInterface = None):
        """
        Inicializa o serviço de produtos.
        
        Args:
            produto_repository (ProdutoRepositoryInterface): Repositório de produtos
        """
        self.produto_repository = produto_repository or ProdutoRepository()
    
    def listar_todos(self) -> List[Produto]:
        """
        Lista todos os produtos.
        
        Returns:
            List[Produto]: Lista com todos os produtos
        """
        return self.produto_repository.find_all()
    
    def buscar_por_id(self, produto_id: int) -> Optional[Produto]:
        """
        Busca um produto por ID.
        
        Args:
            produto_id (int): ID do produto
            
        Returns:
            Optional[Produto]: Produto encontrado ou None
            
        Raises:
            ValueError: Se o ID for inválido
        """
        if not isinstance(produto_id, int) or produto_id <= 0:
            raise ValueError("ID do produto deve ser um número positivo")
        
        return self.produto_repository.find_by_id(produto_id)
    
    def buscar_por_nome(self, nome: str) -> List[Produto]:
        """
        Busca produtos por nome.
        
        Args:
            nome (str): Nome ou parte do nome do produto
            
        Returns:
            List[Produto]: Lista de produtos encontrados
            
        Raises:
            ValueError: Se o nome for vazio
        """
        if not nome or not nome.strip():
            raise ValueError("Nome não pode ser vazio")
        
        return self.produto_repository.find_by_nome(nome.strip())
    
    def salvar(self, produto_data: Dict[str, Any]) -> Produto:
        """
        Salva um novo produto ou atualiza um existente.
        
        Args:
            produto_data (Dict[str, Any]): Dados do produto
            
        Returns:
            Produto: Produto salvo
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        self._validar_dados_produto(produto_data)
        
        # Verifica se é uma atualização (tem ID) ou criação (sem ID)
        if 'id' in produto_data and produto_data['id']:
            produto = self.produto_repository.find_by_id(produto_data['id'])
            if not produto:
                raise ValueError("Produto não encontrado para atualização")
            
            # Atualiza os campos
            produto.nome = produto_data['nome'].strip()
            produto.descricao = produto_data.get('descricao', '').strip()
            produto.preco = float(produto_data['preco'])
            produto.estoque = int(produto_data['estoque'])
        else:
            # Cria novo produto
            produto = Produto.from_dict(produto_data)
        
        return self.produto_repository.save(produto)
    
    def deletar(self, produto_id: int) -> bool:
        """
        Deleta um produto por ID.
        
        Args:
            produto_id (int): ID do produto a ser deletado
            
        Returns:
            bool: True se deletado com sucesso, False caso contrário
            
        Raises:
            ValueError: Se o ID for inválido
        """
        if not isinstance(produto_id, int) or produto_id <= 0:
            raise ValueError("ID do produto deve ser um número positivo")
        
        return self.produto_repository.delete_by_id(produto_id)
    
    def contar_produtos(self) -> int:
        """
        Conta o número total de produtos.
        
        Returns:
            int: Número total de produtos
        """
        return self.produto_repository.count()
    
    def _validar_dados_produto(self, produto_data: Dict[str, Any]) -> None:
        """
        Valida os dados do produto.
        
        Args:
            produto_data (Dict[str, Any]): Dados do produto
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        if not isinstance(produto_data, dict):
            raise ValueError("Dados do produto devem ser um dicionário")
        
        # Validação do nome
        if 'nome' not in produto_data or not produto_data['nome']:
            raise ValueError("Nome é obrigatório")
        
        nome = produto_data['nome'].strip()
        if len(nome) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        
        if len(nome) > 100:
            raise ValueError("Nome deve ter no máximo 100 caracteres")
        
        # Validação do preço
        if 'preco' not in produto_data:
            raise ValueError("Preço é obrigatório")
        
        try:
            preco = float(produto_data['preco'])
            if preco < 0:
                raise ValueError("Preço deve ser um valor positivo")
        except (ValueError, TypeError):
            raise ValueError("Preço deve ser um número válido")
        
        # Validação do estoque
        if 'estoque' not in produto_data:
            raise ValueError("Estoque é obrigatório")
        
        try:
            estoque = int(produto_data['estoque'])
            if estoque < 0:
                raise ValueError("Estoque deve ser um valor não negativo")
        except (ValueError, TypeError):
            raise ValueError("Estoque deve ser um número inteiro válido")
        
        # Validação da descrição (opcional)
        if 'descricao' in produto_data and produto_data['descricao']:
            descricao = produto_data['descricao'].strip()
            if len(descricao) > 500:
                raise ValueError("Descrição deve ter no máximo 500 caracteres")

