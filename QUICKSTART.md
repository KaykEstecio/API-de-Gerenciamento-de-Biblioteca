# 🚀 Guia de Início Rápido - BookMarket

## Para Desenvolvedores

### Pré-requisitos

- Python 3.9+
- Git
- (Opcional) Docker e Docker Compose

### Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/KaykEstecio/API-de-Gerenciamento-de-Biblioteca.git
cd API-de-Gerenciamento-de-Biblioteca

# 2. Crie o ambiente virtual
python -m venv .venv

# 3. Ative o ambiente (Windows)
.venv\Scripts\Activate.ps1

# 4. Instale dependências
pip install -r requirements.txt

# 5. Execute o servidor
python main.py
```

Acesse: http://127.0.0.1:8000

### Primeiro Acesso

1. **Crie uma conta** na tela de cadastro
2. **Faça login** com suas credenciais
3. **Explore o catálogo** de livros
4. **Faça um pedido** clicando em "Comprar Agora"
5. **Pague o pedido** em "Meus Pedidos"

### Acesso Administrativo

Para testar funcionalidades de admin, use:

```
Email: admin@bookmarket.com
Senha: admin123
```

Com essa conta você terá acesso ao **Painel Administrativo** onde pode:
- Criar novos livros
- Editar livros existentes
- Excluir livros
- Gerenciar estoque

---

## Para Usuários Finais

### Como Comprar um Livro

1. **Navegue pelo catálogo** na página inicial
2. **Use a busca** para encontrar livros específicos
3. **Verifique o estoque** (badge verde = disponível)
4. **Clique em "Comprar Agora"** no livro desejado
5. **Vá para "Meus Pedidos"** para ver seu pedido
6. **Clique em "Pagar"** e escolha o método de pagamento
7. **Confirme** e pronto! 🎉

### Métodos de Pagamento

- 💳 **Cartão de Crédito**
- 📱 **PIX**
- 📄 **Boleto Bancário**

### Dicas

- 🔍 Use a **busca em tempo real** para filtrar livros
- 📦 Verifique o **status do estoque** antes de comprar
- 📋 Acompanhe seus **pedidos pendentes** na aba "Meus Pedidos"
- 🎨 Aproveite a **interface premium** com animações suaves

---

## Troubleshooting

### Erro ao iniciar o servidor

**Problema**: `ModuleNotFoundError`

**Solução**:
```bash
pip install -r requirements.txt
```

### Erro de autenticação

**Problema**: Token inválido ou expirado

**Solução**:
1. Faça logout
2. Faça login novamente
3. O token será renovado automaticamente

### Livro não aparece no catálogo

**Problema**: Livro criado mas não visível

**Solução**:
1. Verifique se você está logado como admin
2. Atualize a página (F5)
3. Verifique o console do navegador para erros

### Erro ao fazer pedido

**Problema**: "Estoque insuficiente"

**Solução**:
- O livro está esgotado ou com estoque baixo
- Escolha outro livro ou aguarde reposição

---

## Recursos Adicionais

- 📖 [Documentação Técnica Completa](./DOCUMENTATION.md)
- 🔗 [API Swagger](http://127.0.0.1:8000/docs)
- 📝 [README Principal](./README.md)

---

**Desenvolvido com ❤️ para demonstrar as melhores práticas de desenvolvimento web moderno.**
