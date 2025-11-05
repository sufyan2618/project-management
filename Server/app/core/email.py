from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from app.core.config import settings
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False if settings.MAIL_PORT == 465 else True,
    MAIL_SSL_TLS=True if settings.MAIL_PORT == 465 else False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fn = FastMail(conf)