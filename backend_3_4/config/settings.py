from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    GROK_API_KEY: str = ""

    POSTGRES_HOST: str = "localhost"

    POSTGRES_PORT: int = 5432

    POSTGRES_DB: str = "knowledge_db"

    POSTGRES_USER: str = "postgres"

    POSTGRES_PASSWORD: str = ""

    CHROMA_PATH: str = "./chroma_db"

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    model_config = SettingsConfigDict(

        env_file=".env",

        extra="ignore"

    )


settings = Settings()