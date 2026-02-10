from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# connects_args check_same_thread é necessário apenas para SQLite
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(
    settings.DATABASE_URL, 
    echo=True, # Loga queries SQL no terminal (bom para debug)
    connect_args=connect_args
)

def get_session():
    """Dependência para obter uma sessão do banco de dados."""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Cria as tabelas no banco de dados com base nos modelos."""
    SQLModel.metadata.create_all(engine)
