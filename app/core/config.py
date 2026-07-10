from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    HOST: str
    PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    SEMANTIC_THRESHOLD: float = 0.94
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()