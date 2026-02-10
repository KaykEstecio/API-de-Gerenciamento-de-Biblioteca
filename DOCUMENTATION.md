# 📘 Documentação Técnica - BookMarket

## Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Modelos de Dados](#modelos-de-dados)
4. [API Reference](#api-reference)
5. [Autenticação e Segurança](#autenticação-e-segurança)
6. [Fluxos de Negócio](#fluxos-de-negócio)
7. [Guia de Desenvolvimento](#guia-de-desenvolvimento)
8. [Deploy e Produção](#deploy-e-produção)

---

## Visão Geral

### Propósito

BookMarket é uma plataforma completa de e-commerce especializada em livros, desenvolvida com tecnologias modernas e seguindo as melhores práticas de desenvolvimento web. O sistema oferece uma experiência premium tanto para usuários finais quanto para administradores.

### Características Principais

- **Backend Robusto**: API RESTful construída com FastAPI
- **Autenticação Segura**: JWT com tokens expiráveis e senhas hasheadas
- **Interface Moderna**: UI responsiva com Glassmorphism e animações fluídas
- **Gestão Completa**: Painel administrativo para controle total do catálogo
- **Testes Automatizados**: Cobertura de 100% dos endpoints críticos

### Stack Tecnológico

```mermaid
graph TB
    A[Frontend - Vanilla JS] --> B[FastAPI Backend]
    B --> C[SQLModel ORM]
    C --> D[PostgreSQL]
    B --> E[JWT Auth]
    B --> F[Background Tasks]
    G[Docker] --> B
    G --> D
```

---

## Arquitetura do Sistema

### Estrutura em Camadas

```
┌─────────────────────────────────────┐
│         Frontend Layer              │
│  (HTML, CSS, Vanilla JavaScript)    │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │
│  - Routers (auth, books, orders)    │
│  - Middleware (CORS, Auth)          │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│       Business Logic Layer          │
│  - Security (JWT, Bcrypt)           │
│  - Validation (Pydantic)            │
│  - Background Tasks                 │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│       Data Access Layer             │
│  - SQLModel ORM                     │
│  - Database Sessions                │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│       Database Layer                │
│  - PostgreSQL (Produção)            │
│  - SQLite (Desenvolvimento)         │
└─────────────────────────────────────┘
```

### Componentes Principais

#### 1. Core (`app/core/`)

**`config.py`**
- Gerenciamento de configurações via variáveis de ambiente
- Classe `Settings` com validação Pydantic
- Configurações de JWT, CORS e banco de dados

**`security.py`**
- Criação e validação de tokens JWT
- Hashing de senhas com Bcrypt
- Funções de autenticação

**`database.py`**
- Configuração do SQLModel engine
- Gerenciamento de sessões de banco de dados
- Criação automática de tabelas

**`deps.py`**
- Dependências reutilizáveis do FastAPI
- `get_current_user`: Extrai usuário do token JWT
- `get_current_active_superuser`: Valida permissões de admin

**`utils.py`**
- Funções utilitárias
- Simulação de envio de emails (background tasks)

#### 2. Routers (`app/routers/`)

**`auth.py`**
- Registro de novos usuários
- Login e geração de tokens
- Recuperação de dados do usuário atual

**`books.py`**
- CRUD completo de livros
- Listagem pública
- Operações administrativas (criar, editar, excluir)

**`orders.py`**
- Criação de pedidos
- Listagem de pedidos do usuário
- Processamento de pagamentos
- Controle de estoque automático

#### 3. Frontend (`frontend/`)

**`index.html`**
- Estrutura semântica
- Seções: Auth, Catálogo, Pedidos, Admin
- Modal de pagamento

**`style.css`**
- Design system com variáveis CSS
- Glassmorphism e animações
- Responsividade mobile-first

**`app.js`**
- Gerenciamento de estado (token, usuário)
- Comunicação com API (fetch)
- Manipulação do DOM
- Navegação SPA

---

## Modelos de Dados

### Diagrama de Entidades

```mermaid
erDiagram
    User ||--o{ Order : creates
    Order ||--|{ OrderItem : contains
    Book ||--o{ OrderItem : "is in"
    
    User {
        int id PK
        string email UK
        string full_name
        string hashed_password
        boolean is_active
        boolean is_superuser
    }
    
    Book {
        int id PK
        string title
        string author
        string description
        float price
        int stock_quantity
    }
    
    Order {
        int id PK
        int user_id FK
        datetime created_at
        string status
    }
    
    OrderItem {
        int id PK
        int order_id FK
        int book_id FK
        int quantity
        float item_price
    }
```

### Schemas Pydantic

#### User

```python
# UserBase - Campos comuns
- email: EmailStr
- full_name: str

# UserCreate - Criação
+ password: str

# UserRead - Leitura
+ id: int
+ is_active: bool
+ is_superuser: bool
```

#### Book

```python
# BookBase
- title: str
- author: str
- description: str | None
- price: float
- stock_quantity: int

# BookCreate - Herda BookBase
# BookRead - Herda BookBase
+ id: int
```

#### Order

```python
# OrderBase
- status: str = "pending"

# OrderCreate
- items: List[OrderItemCreate]

# OrderRead
+ id: int
+ created_at: datetime
+ items: List[OrderItemRead]
```

---

## API Reference

### Base URL

- **Desenvolvimento**: `http://127.0.0.1:8000/api/v1`
- **Produção**: `http://localhost:8000/api/v1`

### Autenticação

Todas as rotas protegidas requerem header:
```
Authorization: Bearer <token_jwt>
```

### Endpoints

#### 🔐 Autenticação

##### POST `/auth/register`

Registra um novo usuário.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "senha123",
  "full_name": "Nome Completo"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Nome Completo",
  "is_active": true,
  "is_superuser": false
}
```

##### POST `/auth/token`

Realiza login e retorna token JWT.

**Request Body (form-data):**
```
username: user@example.com
password: senha123
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

##### GET `/auth/me`

Retorna dados do usuário autenticado.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Nome Completo",
  "is_active": true,
  "is_superuser": false
}
```

---

#### 📚 Livros

##### GET `/books/`

Lista todos os livros disponíveis.

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "1984",
    "author": "George Orwell",
    "description": "Clássico distópico",
    "price": 45.90,
    "stock_quantity": 15
  }
]
```

##### GET `/books/{id}`

Retorna detalhes de um livro específico.

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "1984",
  "author": "George Orwell",
  "description": "Clássico distópico",
  "price": 45.90,
  "stock_quantity": 15
}
```

##### POST `/books/` 🔒 Admin

Cria um novo livro.

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "title": "Novo Livro",
  "author": "Autor",
  "description": "Descrição",
  "price": 29.90,
  "stock_quantity": 10
}
```

**Response:** `200 OK`

##### PATCH `/books/{id}` 🔒 Admin

Atualiza um livro existente.

**Headers:** `Authorization: Bearer <admin_token>`

**Request Body:**
```json
{
  "price": 39.90,
  "stock_quantity": 20
}
```

**Response:** `200 OK`

##### DELETE `/books/{id}` 🔒 Admin

Remove um livro do catálogo.

**Headers:** `Authorization: Bearer <admin_token>`

**Response:** `200 OK`
```json
{
  "ok": true
}
```

---

#### 🛒 Pedidos

##### POST `/orders/` 🔒

Cria um novo pedido.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "items": [
    {
      "book_id": 1,
      "quantity": 2
    }
  ]
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "created_at": "2026-02-09T22:00:00",
  "status": "pending",
  "items": [
    {
      "book_id": 1,
      "quantity": 2,
      "item_price": 45.90,
      "book": {
        "id": 1,
        "title": "1984",
        "author": "George Orwell"
      }
    }
  ]
}
```

**Regras de Negócio:**
- Verifica estoque disponível antes de criar
- Deduz quantidade do estoque automaticamente
- Retorna erro 400 se estoque insuficiente

##### GET `/orders/` 🔒

Lista todos os pedidos do usuário autenticado.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "created_at": "2026-02-09T22:00:00",
    "status": "pending",
    "items": [...]
  }
]
```

##### POST `/orders/{id}/pay` 🔒

Processa o pagamento de um pedido.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "status": "paid",
  "created_at": "2026-02-09T22:00:00",
  "items": [...]
}
```

**Regras de Negócio:**
- Apenas pedidos com status "pending" podem ser pagos
- Altera status para "paid"
- Envia email de confirmação (background task)

---

## Autenticação e Segurança

### Fluxo de Autenticação JWT

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API
    participant DB as Database
    
    U->>F: Insere credenciais
    F->>A: POST /auth/token
    A->>DB: Busca usuário por email
    DB-->>A: Retorna usuário
    A->>A: Verifica senha (bcrypt)
    A->>A: Gera token JWT
    A-->>F: Retorna token
    F->>F: Armazena em localStorage
    F->>A: GET /books/ (Header: Bearer token)
    A->>A: Valida token
    A-->>F: Retorna dados
```

### Implementação de Segurança

#### Hashing de Senhas

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Criar hash
hashed = pwd_context.hash("senha123")

# Verificar senha
is_valid = pwd_context.verify("senha123", hashed)
```

#### Geração de Token JWT

```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

#### Validação de Token

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload.get("sub"))
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=401)
        return user
    except JWTError:
        raise HTTPException(status_code=401)
```

### Controle de Acesso

#### Rotas Públicas
- `GET /books/`
- `GET /books/{id}`
- `POST /auth/register`
- `POST /auth/token`

#### Rotas Autenticadas
- `GET /auth/me`
- `POST /orders/`
- `GET /orders/`
- `POST /orders/{id}/pay`

#### Rotas Administrativas
- `POST /books/`
- `PATCH /books/{id}`
- `DELETE /books/{id}`

---

## Fluxos de Negócio

### 1. Cadastro e Login

```mermaid
graph TD
    A[Usuário acessa site] --> B{Tem conta?}
    B -->|Não| C[Clica em Cadastro]
    B -->|Sim| D[Faz Login]
    C --> E[Preenche formulário]
    E --> F[POST /auth/register]
    F --> G[Conta criada]
    G --> D
    D --> H[POST /auth/token]
    H --> I[Recebe JWT]
    I --> J[Armazena token]
    J --> K[Redireciona para Dashboard]
```

### 2. Compra de Livro

```mermaid
graph TD
    A[Usuário navega catálogo] --> B[Seleciona livro]
    B --> C{Estoque disponível?}
    C -->|Não| D[Botão desabilitado]
    C -->|Sim| E[Clica em Comprar]
    E --> F[POST /orders/]
    F --> G{Estoque suficiente?}
    G -->|Não| H[Erro 400]
    G -->|Sim| I[Cria pedido]
    I --> J[Deduz estoque]
    J --> K[Retorna pedido criado]
    K --> L[Exibe em Meus Pedidos]
```

### 3. Pagamento

```mermaid
graph TD
    A[Usuário vê pedido pendente] --> B[Clica em Pagar]
    B --> C[Abre modal de pagamento]
    C --> D[Seleciona método]
    D --> E[Confirma pagamento]
    E --> F[POST /orders/id/pay]
    F --> G[Atualiza status para paid]
    G --> H[Envia email confirmação]
    H --> I[Exibe mensagem sucesso]
    I --> J[Atualiza lista de pedidos]
```

### 4. Gestão Administrativa

```mermaid
graph TD
    A[Admin faz login] --> B[Acessa painel admin]
    B --> C{Ação desejada?}
    C -->|Criar| D[Preenche formulário]
    C -->|Editar| E[Clica em editar]
    C -->|Excluir| F[Clica em excluir]
    D --> G[POST /books/]
    E --> H[PATCH /books/id]
    F --> I[DELETE /books/id]
    G --> J[Atualiza tabela]
    H --> J
    I --> J
    J --> K[Atualiza catálogo público]
```

---

## Guia de Desenvolvimento

### Configuração do Ambiente

#### 1. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Database
DATABASE_URL=sqlite:///./bookmarket.db
# Para PostgreSQL: postgresql://user:pass@localhost/dbname

# Security
SECRET_KEY=sua_chave_secreta_super_segura_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:8000","http://127.0.0.1:8000"]
```

#### 2. Instalação de Dependências

```bash
pip install -r requirements.txt
```

**Principais dependências:**
- `fastapi` - Framework web
- `sqlmodel` - ORM
- `python-jose[cryptography]` - JWT
- `passlib[bcrypt]` - Hashing
- `uvicorn[standard]` - Servidor ASGI
- `pytest` - Testes
- `httpx` - Cliente HTTP para testes

### Executando em Desenvolvimento

```bash
# Modo desenvolvimento com reload automático
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Ou use o script principal
python main.py
```

### Executando Testes

```bash
# Todos os testes
pytest

# Com verbosidade
pytest -v

# Com cobertura
pytest --cov=app tests/
```

### Adicionando Novos Endpoints

#### 1. Criar Router

```python
# app/routers/new_feature.py
from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter()

@router.get("/")
def list_items():
    return {"items": []}
```

#### 2. Registrar no Main

```python
# app/main.py
from app.routers import new_feature

app.include_router(
    new_feature.router,
    prefix="/api/v1/new-feature",
    tags=["new-feature"]
)
```

#### 3. Criar Testes

```python
# tests/test_new_feature.py
def test_list_items(client):
    response = client.get("/api/v1/new-feature/")
    assert response.status_code == 200
```

### Boas Práticas

#### Estrutura de Código

✅ **Faça:**
- Use type hints em todas as funções
- Valide dados com Pydantic
- Separe lógica de negócio dos routers
- Use dependências do FastAPI para reutilização

❌ **Evite:**
- Lógica de negócio no frontend
- Senhas em plain text
- Queries SQL diretas (use ORM)
- Endpoints sem autenticação quando necessário

#### Segurança

✅ **Faça:**
- Sempre hash senhas antes de salvar
- Valide tokens em rotas protegidas
- Use HTTPS em produção
- Limite rate de requisições

❌ **Evite:**
- Expor SECRET_KEY no código
- Retornar stack traces em produção
- Aceitar qualquer origem CORS
- Armazenar tokens em cookies sem httpOnly

---

## Deploy e Produção

### Docker

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/bookmarket
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=bookmarket
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Checklist de Produção

- [ ] Configurar variáveis de ambiente seguras
- [ ] Usar PostgreSQL em vez de SQLite
- [ ] Habilitar HTTPS (certificado SSL)
- [ ] Configurar CORS para domínios específicos
- [ ] Implementar rate limiting
- [ ] Configurar logging adequado
- [ ] Fazer backup regular do banco de dados
- [ ] Monitorar performance e erros
- [ ] Implementar health checks
- [ ] Configurar CI/CD

### Monitoramento

#### Health Check Endpoint

```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }
```

#### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.get("/books/")
def list_books():
    logger.info("Listing all books")
    # ...
```

---

## Conclusão

Esta documentação cobre os aspectos técnicos essenciais do BookMarket. Para dúvidas adicionais:

- **Swagger UI**: `/docs` - Documentação interativa da API
- **ReDoc**: `/redoc` - Documentação alternativa
- **Código-fonte**: Consulte os comentários inline no código

**Desenvolvido com ❤️ seguindo as melhores práticas de desenvolvimento web.**
