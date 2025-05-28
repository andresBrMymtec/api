from pymongo import AsyncMongoClient
from src.utils.config import Settings

settings: Settings = Settings()

audit_client = AsyncMongoClient(settings.AUDITORIA_MONGODB)
AUDIT_COLLECTION = audit_client[settings.AUDITORIA_DB_NAME][settings.AUDITORIA_COLLECTION_NAME]


def get_collection():
    return AUDIT_COLLECTION
