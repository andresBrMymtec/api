from langchain_community.vectorstores import FAISS
from typing import Literal
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from src.utils.config import Settings
from src.rag.llm import OpenAiModels


settings: Settings = Settings()
open_ai_model: OpenAiModels = OpenAiModels()
# Conexión a MongoDB Atlas

client = MongoClient(settings.MONGODB_ATLAS_CLUSTER_URI)
MONGODB_COLLECTION = client[settings.DB_NAME][settings.COLLECTION_NAME]

vector_store = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=open_ai_model.get_embeddings(),
    index_name=settings.ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)


def get_store():
    return vector_store


def get_collection():
    return MONGODB_COLLECTION
