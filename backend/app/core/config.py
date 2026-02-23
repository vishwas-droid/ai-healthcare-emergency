from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Emergency Healthcare Platform"
    database_url: str = Field(default="sqlite:///./healthcare.db", alias="DATABASE_URL")
    cors_origins_raw: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173,https://ai-healthcare-emergency.vercel.app",
        alias="CORS_ORIGINS",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]


settings = Settings()
