from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "StudyMate API"
    ollama_base_url: str | None = None
    ollama_model: str | None = None
    vector_store_path: str = "data/vector_store/index.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()