from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "BookMarket API"
    API_V1_STR: str = "/api/v1"
    
    # Configurações de Banco de Dados
    DATABASE_URL: str = "sqlite:///./bookmarket.db"
    
    # Configurações de Segurança (JWT)
    # IMPORTANTE: Em produção, gere uma chave segura e mantenha em segredo!
    SECRET_KEY: str = "uma_chave_super_secreta_e_segura_para_desenvolvimento"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
