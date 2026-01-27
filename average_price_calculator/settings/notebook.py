"""Notebook settings configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class NotebookSettings(BaseSettings):
    """Notebook specific settings."""

    name: str = "average_price_calculator"

    model_config = SettingsConfigDict(
        env_prefix="APP_NB_",
        case_sensitive=False,
    )
