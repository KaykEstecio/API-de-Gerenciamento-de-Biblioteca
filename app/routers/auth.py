from typing import Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core import security
from app.core.utils import send_email_log
from app.core.database import get_session
from app.core.deps import get_current_user
from app.models import User, UserCreate, UserRead

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(
    *,
    session: Session = Depends(get_session),
    user_in: UserCreate,
    background_tasks: BackgroundTasks
) -> Any:
    """
    Cria um novo usuário.
    """
    user = session.exec(
        select(User).where(User.email == user_in.email)
    ).first()
    
    if user:
        raise HTTPException(
            status_code=400,
            detail="O usuário com este email já existe no sistema.",
        )
        
    user_data = user_in.model_dump(exclude={"password"})
    hashed_password = security.get_password_hash(user_in.password)
    user_obj = User(**user_data, hashed_password=hashed_password)
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)

    # Envia email de boas-vindas em background
    background_tasks.add_task(
        send_email_log, 
        user_obj.email, 
        "Bem-vindo ao BookMarket!", 
        "Sua conta foi criada com sucesso."
    )

    return user_obj

@router.post("/token")
def login_for_access_token(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = session.exec(
        select(User).where(User.email == form_data.username)
    ).first()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
        
    access_token_expires = security.settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=None
        ),
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Retorna os dados do usuário logado.
    """
    return current_user
