from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    FRONTEND_URL: str
    ADZUNA_APP_ID: str
    ADZUNA_APP_KEY: str
    ADZUNA_COUNTRY: str = "de"

    class Config:
        env_file = ".env"

settings = Settings()