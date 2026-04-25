from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Database URL (e.g., PostgreSQL, MySQL, SQLite)
    DATABASE_URL: str

    # Claude
    ANTHROPIC_API_KEY: str

    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
