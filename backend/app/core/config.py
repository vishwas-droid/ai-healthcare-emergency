from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Emergency Healthcare Platform"
    database_url: str = Field(default="sqlite:///./healthcare.db", alias="DATABASE_URL")
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


settings = Settings()
