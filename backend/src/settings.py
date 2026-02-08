import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Application settings
    app_name: str = "Todo Backend API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # CORS settings
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    class Config:
        env_file = ".env"

settings = Settings()