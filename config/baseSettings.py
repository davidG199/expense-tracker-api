from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # JWT Configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"  # Valor por defecto
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # PostgreSQL Configuration
    POSTGRES_USER: str = "expense_user"
    POSTGRES_PASSWORD: str = "expense_password_123"
    POSTGRES_DB: str = "expense_tracker_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str
    
    # API Configuration (opcional)
    APP_NAME: str = "Expense Tracker API"
    DEBUG: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",  # Lee desde .env automáticamente
        env_file_encoding="utf-8",
        case_sensitive=True  # Las variables deben coincidir en mayúsculas
    )

# Instancia única
settings = Settings() # type: ignore