from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Groq
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    groq_fallback_model: str = "llama-3.1-8b-instant"

    # Database
    database_url: str = "postgresql://alinairam@localhost/hcp_crm"

    # Frontend
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()