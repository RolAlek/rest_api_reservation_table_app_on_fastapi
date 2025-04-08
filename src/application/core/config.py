from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class DatabaseSettings(BaseSettings):
    user: str
    password: str
    name: str

    driver: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: int = 5432
    echo: bool = False

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class APISettings(BaseSettings):
    title: str
    host: str
    port: int
    debug: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="allow",
    )

    api: APISettings
    db: DatabaseSettings
