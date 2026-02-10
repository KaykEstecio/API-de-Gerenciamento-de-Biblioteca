from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.deps import get_current_user, get_current_active_superuser
from app.models import Book, BookCreate, BookRead, User

router = APIRouter()

@router.get("/", response_model=List[BookRead])
def read_books(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: Optional[str] = None
):
    """
    Lista livros com paginação e busca simples por título.
    """
    query = select(Book)
    if search:
        query = query.where(Book.title.contains(search))
    book_list = session.exec(query.offset(offset).limit(limit)).all()
    return book_list

@router.post("/", response_model=BookRead)
def create_book(
    *,
    session: Session = Depends(get_session),
    book_in: BookCreate,
    current_user: User = Depends(get_current_active_superuser),
):
    """
    Cria um novo livro (Apenas Admin).
    """
    book = Book.from_orm(book_in)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@router.get("/{book_id}", response_model=BookRead)
def read_book(
    *,
    session: Session = Depends(get_session),
    book_id: int,
):
    """
    Obtém detalhes de um livro pelo ID.
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book

@router.patch("/{book_id}", response_model=BookRead)
def update_book(
    *,
    session: Session = Depends(get_session),
    book_id: int,
    book_in: BookCreate, # Usando BookCreate para simplificar, mas poderia ser BookUpdate
    current_user: User = Depends(get_current_active_superuser),
):
    """
    Atualiza um livro (Apenas Admin).
    """
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    book_data = book_in.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
        
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.delete("/{book_id}")
def delete_book(
    *,
    session: Session = Depends(get_session),
    book_id: int,
    current_user: User = Depends(get_current_active_superuser),
):
    """
    Remove um livro (Apenas Admin).
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    session.delete(book)
    session.commit()
    return {"ok": True}
