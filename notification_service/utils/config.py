from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_PASSWORD: str
    SMTP_EMAIL: str
    SAFE_TIME_SECONDS: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()