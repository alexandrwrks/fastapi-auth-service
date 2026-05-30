from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MAIL_PASSWORD: str
    MAIL_LOGIN: EmailStr

    class Config:
        env_file = ".env"


settings = Settings()
