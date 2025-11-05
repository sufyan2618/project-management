from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 600
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    CLIENT_URL: str = "http://localhost:5173"
    MAIL_FROM: Optional[str] = None
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()