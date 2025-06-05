from pymongo import AsyncMongoClient
from src.utils.config import Settings

settings: Settings = Settings()

client = AsyncMongoClient(settings.MONGODB_ATLAS_CLUSTER_URI)
COLLECTION = client[settings.DB_NAME][settings.COLLECTION_NAME]


def get_async_db():

    return COLLECTION
