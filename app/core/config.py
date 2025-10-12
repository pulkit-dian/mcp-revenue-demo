"""Application configuration using Pydantic Settings."""

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    database_name: str
    database_user: str
    database_password: str
    database_host: str
    database_port: int

    # Database Pool Configuration
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # Server Configuration
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @computed_field  # type: ignore[misc]
    @property
    def database_url(self) -> str:
        """Construct database URL from individual components."""
        return (
            f"postgresql+asyncpg://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )


# Create a singleton instance
settings = Settings()
