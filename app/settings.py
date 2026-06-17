from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_NAME: str = "pomodoro"

    CACHE_HOST: str = "0.0.0.0"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

    JWT_SECRET_KEY: str = "secret_key"
    JWT_ENCODE_ALGORITHM: str = "HS256"

    BROKER_URL: str = "localhost:9092"
    EMAIL_TOPIC: str = "email_topic"
    EMAIL_CALLBACK_TOPIC: str = "callback_email_topic"

    @property
    def db_url(self):
        return (
            f"{self.DB_DRIVER}://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )