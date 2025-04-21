from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    minio_access_key: str
    minio_secret_key: str
    qdrant_host: str
    qdrant_port: int = 6333
    embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:latest"
    qdrant_collection: str = "UNIFAGOC"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()