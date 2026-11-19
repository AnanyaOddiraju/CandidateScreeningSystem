from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str ="AI Screeening Application"
    OPENAI_API_KEY: str
    DATABASE_URL: str
    QDRANT_URL: str ="http://localhost:6333"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173"
    ]
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
    # # Database settings
    # DB_HOST: str
    # DB_PORT: int
    # DB_USER: str
    # DB_PASSWORD: str
    # DB_NAME: str

    # # JWT settings
    # JWT_SECRET_KEY: str
    # JWT_ALGORITHM: str
    # JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int