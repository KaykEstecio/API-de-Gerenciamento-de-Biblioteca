from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

# --- Tabela de Associação (Muitos-para-Muitos com Atributos Extras) ---
class OrderItem(SQLModel, table=True):
    order_id: Optional[int] = Field(default=None, foreign_key="order.id", primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key="book.id", primary_key=True)
    quantity: int = 1
    item_price: float # Preço no momento da compra (snapshot)

    # Relacionamentos para facilitar o acesso e satisfazer o SQLAlchemy
    order: "Order" = Relationship(back_populates="items")
    book: "Book" = Relationship(back_populates="order_items")

# --- Usuário ---
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    orders: List["Order"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

# --- Livro ---
class BookBase(SQLModel):
    title: str = Field(index=True)
    author: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_items: List[OrderItem] = Relationship(back_populates="book") # Para relação M:N, mas na prática acessamos via Link se precisar

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int

# --- Pedido ---
class OrderBase(SQLModel):
    status: str = "pending" # pending, paid, shipped, cancelled

class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(foreign_key="user.id")
    
    user: Optional[User] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")    # Para acessar livros diretamente poderia usar: books: List[Book] = Relationship(link_model=OrderItem)
    # Mas como OrderItem tem 'quantity', é melhor acessar items.

class OrderItemRead(SQLModel):
    book_id: int
    quantity: int
    item_price: float
    book: BookRead

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItemRead]
