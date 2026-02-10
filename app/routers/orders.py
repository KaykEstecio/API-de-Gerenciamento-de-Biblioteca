from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session, select
from pydantic import BaseModel

from app.core.utils import send_email_log
from app.core.database import get_session
from app.core.deps import get_current_user
from app.models import Order, OrderItem, OrderRead, User, Book

router = APIRouter()

# Schema de entrada para criação de pedido
class OrderItemInput(BaseModel):
    book_id: int
    quantity: int

class OrderCreateRequest(BaseModel):
    items: List[OrderItemInput]

@router.post("/", response_model=OrderRead)
def create_order(
    *,
    session: Session = Depends(get_session),
    order_in: OrderCreateRequest,
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks
):
    """
    Cria um pedido. Verifica estoque, deduz quantidades e gera itens do pedido.
    """
    if not order_in.items:
        raise HTTPException(status_code=400, detail="Pedido deve conter pelo menos um item")

    # 1. Criar o pedido (status pendente)
    order = Order(user_id=current_user.id, status="pending")
    session.add(order)
    
    # Precisamos commitar o Order antes para ter items? Depende se usamos list append.
    # Vamos validar tudo antes de commitar qualquer coisa para atomicidade.
    
    # Mas para adicionar OrderItem com order_id, precisamos do order. 
    # Session SQLModel gerencia isso se adicionarmos aos relacionamentos.

    total_value = 0.0

    for item_in in order_in.items:
        book = session.get(Book, item_in.book_id)
        if not book:
            raise HTTPException(status_code=404, detail=f"Livro {item_in.book_id} não encontrado")
        
        if book.stock_quantity < item_in.quantity:
             raise HTTPException(
                status_code=400, 
                detail=f"Estoque insuficiente para o livro '{book.title}'. Restam apenas {book.stock_quantity}."
            )
        
        # Deduzir estoque
        book.stock_quantity -= item_in.quantity
        session.add(book)
        
        # Criar item do pedido
        order_item = OrderItem(
            order=order, # Link automatico sqlmodel
            book=book,   # Link automatico sqlmodel
            quantity=item_in.quantity,
            item_price=book.price
        )
        session.add(order_item)
        total_value += book.price * item_in.quantity
    
    session.commit()
    session.refresh(order)

    # Notificar usuário
    background_tasks.add_task(
        send_email_log,
        current_user.email,
        f"Confirmação de Pedido #{order.id}",
        f"Seu pedido no valor de R$ {total_value:.2f} foi recebido e está aguardando pagamento."
    )

    return order

@router.get("/", response_model=List[OrderRead])
def read_orders(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Lista os pedidos do usuário atual.
    """
    return current_user.orders

@router.post("/{order_id}/pay", response_model=OrderRead)
def pay_order(
    *,
    session: Session = Depends(get_session),
    order_id: int,
    current_user: User = Depends(get_current_user),
):
    """
    Simula o pagamento de um pedido.
    """
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado")
        
    if order.status == "paid":
        raise HTTPException(status_code=400, detail="Pedido já está pago")
        
    order.status = "paid"
    session.add(order)
    session.commit()
    session.refresh(order)
    return order
