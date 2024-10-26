from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    POSTGRES_USER_TEST: str
    POSTGRES_PASSWORD_TEST: str
    POSTGRES_DB_TEST: str
    POSTGRES_HOST_TEST: str
    POSTGRES_PORT_TEST: str

    @property
    def DATABASE_URL(self):
        return (f"postgresql+asyncpg://"
                f"{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/"
                f"{self.POSTGRES_DB}")

    @property
    def TEST_DATABASE_URL(self):
        return (f"postgresql+asyncpg://"
                f"{self.POSTGRES_USER_TEST}:"
                f"{self.POSTGRES_PASSWORD_TEST}@"
                f"{self.POSTGRES_HOST_TEST}:"
                f"{self.POSTGRES_PORT}/"
                f"{self.POSTGRES_DB_TEST}")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()