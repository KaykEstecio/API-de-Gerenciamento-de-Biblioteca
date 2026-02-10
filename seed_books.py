"""
Script para popular o banco de dados com livros de exemplo.
Execute: python seed_books.py
"""
import requests

API_URL = "http://127.0.0.1:8000/api/v1"

# Primeiro, criar um usuário admin
def create_admin():
    admin_data = {
        "email": "admin@bookmarket.com",
        "password": "admin123",
        "full_name": "Administrador",
        "is_active": True,
        "is_superuser": True
    }
    
    try:
        response = requests.post(f"{API_URL}/auth/register", json=admin_data)
        if response.status_code == 200:
            print("✅ Admin criado com sucesso!")
        else:
            print("ℹ️  Admin já existe ou erro ao criar")
    except Exception as e:
        print(f"⚠️  Erro ao criar admin: {e}")

# Fazer login como admin
def get_admin_token():
    login_data = {
        "username": "admin@bookmarket.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{API_URL}/auth/token", data=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Login realizado com sucesso!")
            return token
        else:
            print("❌ Erro ao fazer login")
            return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

# Livros para adicionar
BOOKS = [
    {
        "title": "1984",
        "author": "George Orwell",
        "description": "Um clássico distópico sobre vigilância e totalitarismo.",
        "price": 45.90,
        "stock_quantity": 15
    },
    {
        "title": "O Senhor dos Anéis: A Sociedade do Anel",
        "author": "J.R.R. Tolkien",
        "description": "A épica jornada de Frodo para destruir o Um Anel.",
        "price": 89.90,
        "stock_quantity": 8
    },
    {
        "title": "Harry Potter e a Pedra Filosofal",
        "author": "J.K. Rowling",
        "description": "O início da jornada mágica de Harry Potter.",
        "price": 39.90,
        "stock_quantity": 20
    },
    {
        "title": "O Pequeno Príncipe",
        "author": "Antoine de Saint-Exupéry",
        "description": "Uma fábula poética sobre amor, amizade e perda.",
        "price": 29.90,
        "stock_quantity": 25
    },
    {
        "title": "Dom Casmurro",
        "author": "Machado de Assis",
        "description": "Um dos maiores clássicos da literatura brasileira.",
        "price": 34.90,
        "stock_quantity": 12
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "description": "Manual essencial para escrever código limpo e manutenível.",
        "price": 79.90,
        "stock_quantity": 10
    },
    {
        "title": "O Hobbit",
        "author": "J.R.R. Tolkien",
        "description": "A aventura de Bilbo Bolseiro na Terra Média.",
        "price": 54.90,
        "stock_quantity": 2
    },
    {
        "title": "Sapiens: Uma Breve História da Humanidade",
        "author": "Yuval Noah Harari",
        "description": "Uma jornada fascinante pela história da espécie humana.",
        "price": 64.90,
        "stock_quantity": 18
    },
    {
        "title": "A Revolução dos Bichos",
        "author": "George Orwell",
        "description": "Uma sátira política sobre poder e corrupção.",
        "price": 32.90,
        "stock_quantity": 0
    },
    {
        "title": "O Código Da Vinci",
        "author": "Dan Brown",
        "description": "Um thriller envolvente sobre mistérios religiosos.",
        "price": 49.90,
        "stock_quantity": 7
    }
]

def add_books(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n📚 Adicionando livros ao catálogo...\n")
    
    for book in BOOKS:
        try:
            response = requests.post(f"{API_URL}/books/", json=book, headers=headers)
            if response.status_code == 200:
                print(f"✅ '{book['title']}' adicionado com sucesso!")
            else:
                print(f"⚠️  Erro ao adicionar '{book['title']}': {response.text}")
        except Exception as e:
            print(f"❌ Erro ao adicionar '{book['title']}': {e}")
    
    print("\n🎉 Processo concluído!")

if __name__ == "__main__":
    print("🚀 Iniciando população do banco de dados...\n")
    
    # Criar admin
    create_admin()
    
    # Fazer login
    token = get_admin_token()
    
    if token:
        # Adicionar livros
        add_books(token)
    else:
        print("❌ Não foi possível obter o token. Verifique se o servidor está rodando.")
