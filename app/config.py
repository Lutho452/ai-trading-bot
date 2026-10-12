from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ai-trading-bot"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "sqlite:///./trading.db"
    BINANCE_API_KEY: str = ""
    BINANCE_API_SECRET: str = ""
    ALPHA_VANTAGE_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
