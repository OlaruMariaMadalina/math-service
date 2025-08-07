from pydantic import ConfigDict
from pydantic_settings import BaseSettings


# Application configuration loaded from environment
class Settings(BaseSettings):
    app_name: str = "Math API"
    db_url: str = "sqlite:///data/math.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    API_BASE: str = "http://localhost:8000"

    # Load environment variables from .env file
    model_config = ConfigDict(env_file=".env")


# Instantiate settings object
settings = Settings()
