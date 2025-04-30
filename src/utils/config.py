from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SQLALCHEMY_DATABASE_URL: str
    ATLAS_VECTOR_SEARCH_INDEX_NAME: str
    MONGODB_ATLAS_CLUSTER_URI: str
    COLLECTION_NAME: str
    DB_NAME: str
    OPENAI_API_KEY: str
    DIMENSIONS: int

    class Config:
        env_file = ".env"
