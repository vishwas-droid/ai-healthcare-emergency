from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Emergency Healthcare Platform"
    database_url: str = Field(default="sqlite:///./healthcare.db", alias="DATABASE_URL")
    jwt_secret: str = Field(default="CHANGE_ME_NOW", alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_exp_minutes: int = Field(default=180, alias="JWT_EXP_MINUTES")
    encryption_key: str = Field(default="", alias="ENCRYPTION_KEY")
    google_maps_api_key: str = Field(default="", alias="GOOGLE_MAPS_API_KEY")
    ai_service_url: str = Field(default="", alias="AI_SERVICE_URL")
    enable_llm_triage: bool = Field(default=False, alias="ENABLE_LLM_TRIAGE")
    cors_origins_raw: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173,https://ai-healthcare-emergency.vercel.app",
        alias="CORS_ORIGINS",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]


settings = Settings()
