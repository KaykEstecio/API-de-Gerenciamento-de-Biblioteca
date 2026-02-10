from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.routers import auth, books, orders
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Servir arquivos estáticos (CSS, JS)
# Assume que a pasta 'frontend' está na raiz do projeto
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Evento de inicialização para criar as tabelas
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Incluindo Rotas
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(books.router, prefix=f"{settings.API_V1_STR}/books", tags=["books"])
app.include_router(orders.router, prefix=f"{settings.API_V1_STR}/orders", tags=["orders"])

@app.get("/")
def read_index():
    return FileResponse("frontend/index.html")

