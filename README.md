# API RESTful de Clientes - Desafio Final

## Descrição

Este projeto implementa uma API RESTful completa para gerenciamento de clientes, desenvolvida como parte do desafio final da pós-graduação em Arquitetura de Software. A aplicação segue o padrão arquitetural MVC, implementa todas as operações CRUD e funcionalidades adicionais, utilizando Python com Flask e seguindo as melhores práticas de desenvolvimento e Clean Code.

## Características Principais

- **Arquitetura MVC**: Separação clara de responsabilidades entre Model, View e Controller
- **API RESTful**: Endpoints completos seguindo princípios REST
- **Operações CRUD**: Create, Read, Update, Delete para entidade Cliente
- **Funcionalidades Extras**: Contagem, busca por nome, listagem completa
- **Persistência**: Banco de dados SQLite com SQLAlchemy ORM
- **Testes Abrangentes**: 42 testes automatizados cobrindo todas as camadas
- **Clean Code**: Código limpo seguindo melhores práticas
- **Documentação UML**: Diagramas de classes, componentes e sequência

## Tecnologias Utilizadas

- **Python 3.11**
- **Flask 3.1.1** - Framework web
- **Flask-SQLAlchemy 3.1.1** - ORM para banco de dados
- **Flask-CORS 6.0.0** - Suporte a CORS
- **SQLite** - Banco de dados
- **unittest** - Framework de testes

## Estrutura do Projeto

```
cliente_api/
├── src/
│   ├── models/              # Entidades e repositórios
│   ├── services/            # Lógica de negócios
│   ├── routes/              # Controladores (endpoints)
│   ├── database/            # Banco de dados SQLite
│   └── main.py              # Aplicação principal
├── tests/                   # Testes automatizados
├── venv/                    # Ambiente virtual
└── requirements.txt         # Dependências
```

## Endpoints da API

### Operações CRUD

- `POST /api/clientes` - Criar cliente
- `GET /api/clientes` - Listar todos os clientes
- `GET /api/clientes/{id}` - Buscar cliente por ID
- `PUT /api/clientes/{id}` - Atualizar cliente
- `DELETE /api/clientes/{id}` - Deletar cliente

### Funcionalidades Adicionais

- `GET /api/clientes/nome/{nome}` - Buscar por nome
- `GET /api/clientes/contar` - Contar total de clientes
- `GET /api/health` - Verificação de saúde da API

## Instalação e Execução

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone ou baixe o projeto**
   ```bash
   cd cliente_api
   ```

2. **Ative o ambiente virtual**
   ```bash
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências** (se necessário)
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python src/main.py
   ```

5. **Acesse a API**
   - URL base: `http://localhost:5000`
   - Teste de saúde: `http://localhost:5000/api/health`

## Executando os Testes

Para executar todos os testes automatizados:

```bash
# Ative o ambiente virtual
source venv/bin/activate

# Execute os testes
python -m unittest discover tests/ -v
```

## Exemplos de Uso

### Criar um Cliente

```bash
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva", "email": "joao.silva@email.com"}'
```

### Listar Todos os Clientes

```bash
curl -X GET http://localhost:5000/api/clientes
```

### Buscar Cliente por ID

```bash
curl -X GET http://localhost:5000/api/clientes/1
```

### Atualizar Cliente

```bash
curl -X PUT http://localhost:5000/api/clientes/1 \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva Atualizado", "email": "joao.novo@email.com"}'
```

### Deletar Cliente

```bash
curl -X DELETE http://localhost:5000/api/clientes/1
```

### Buscar por Nome

```bash
curl -X GET http://localhost:5000/api/clientes/nome/João
```

### Contar Clientes

```bash
curl -X GET http://localhost:5000/api/clientes/contar
```

## Validações Implementadas

- **Nome**: Obrigatório, entre 2 e 100 caracteres
- **Email**: Obrigatório, formato válido, máximo 120 caracteres, único no sistema
- **ID**: Deve ser um número positivo para operações de busca/atualização/exclusão

## Tratamento de Erros

A API retorna códigos de status HTTP apropriados:

- `200 OK` - Operação bem-sucedida
- `201 Created` - Recurso criado com sucesso
- `204 No Content` - Exclusão bem-sucedida
- `400 Bad Request` - Dados inválidos
- `404 Not Found` - Recurso não encontrado
- `500 Internal Server Error` - Erro interno

Erros retornam JSON no formato:
```json
{
  "erro": "Descrição do erro"
}
```

## Arquitetura e Design

O projeto implementa o padrão MVC com as seguintes responsabilidades:

- **Model** (`src/models/`): Entidades de dados e repositórios
- **Service** (`src/services/`): Lógica de negócios e validações
- **Controller** (`src/routes/`): Endpoints HTTP e coordenação de requisições

## Diagramas UML

O projeto inclui diagramas UML completos:

- **Diagrama de Classes**: Estrutura das classes e relacionamentos
- **Diagrama de Componentes**: Organização da arquitetura MVC
- **Diagrama de Sequência**: Fluxo das operações CRUD

## Contribuição

Este projeto foi desenvolvido como parte de um desafio acadêmico, seguindo as melhores práticas de:

- Clean Code
- Arquitetura de Software
- Padrões de Design
- Testes Automatizados
- Documentação Técnica

