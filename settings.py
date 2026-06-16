from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str
    DB_DRIVER: str = "postgresql+psycopg2"
    DB_NAME: str = "pomodoro"

    CACHE_HOST: str = "0.0.0.0"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

    JWT_SECRET_KEY: str = "secret_key"
    JWT_ENCODE_ALGORITHM: str = "HS256"

    @property
    def db_url(self) -> str:
        return (
            f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )