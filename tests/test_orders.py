from fastapi.testclient import TestClient

def get_auth_token(client: TestClient, email: str = "order@example.com") -> dict:
    # Helper para registrar e logar
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "pass", "is_superuser": True} # Superuser para criar livros
    )
    resp = client.post(
        "/api/v1/auth/token",
        data={"username": email, "password": "pass"}
    )
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}

def test_create_order(client: TestClient):
    headers = get_auth_token(client)
    
    # 1. Criar Livro
    resp_book = client.post(
        "/api/v1/books/",
        json={"title": "Test Book", "author": "Me", "price": 50.0, "stock_quantity": 10},
        headers=headers
    )
    book_id = resp_book.json()["id"]
    
    # 2. Criar Pedido (comprando 2)
    resp_order = client.post(
        "/api/v1/orders/",
        json={"items": [{"book_id": book_id, "quantity": 2}]},
        headers=headers
    )
    assert resp_order.status_code == 200
    data = resp_order.json()
    assert data["status"] == "pending"
    
    # 3. Verificar Estoque (deve ser 8)
    resp_book_after = client.get(f"/api/v1/books/{book_id}")
    assert resp_book_after.json()["stock_quantity"] == 8

def test_create_order_insufficient_stock(client: TestClient):
    headers = get_auth_token(client, email="stock@example.com")
    
    # 1. Criar Livro com estoque 1
    resp_book = client.post(
        "/api/v1/books/",
        json={"title": "Rare Book", "author": "Me", "price": 100.0, "stock_quantity": 1},
        headers=headers
    )
    book_id = resp_book.json()["id"]
    
    # 2. Tentar comprar 2
    resp_order = client.post(
        "/api/v1/orders/",
        json={"items": [{"book_id": book_id, "quantity": 2}]},
        headers=headers
    )
    assert resp_order.status_code == 400
    assert "Estoque insuficiente" in resp_order.json()["detail"]
