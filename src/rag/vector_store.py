from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from src.utils.config import Settings
from src.rag.llm import OpenAiModels

settings: Settings = Settings()
open_ai_model: OpenAiModels = OpenAiModels()
# Conexión a MongoDB Atlas


class MongoVectorStore:

    def __init__(self):
        self.client = MongoClient(settings.MONGODB_ATLAS_CLUSTER_URI)
        self.MONGODB_COLLECTION = self.client[settings.DB_NAME][settings.COLLECTION_NAME]

    def ping(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def get_store(self):
        vector_store = MongoDBAtlasVectorSearch(
            collection=self.MONGODB_COLLECTION,
            embedding=open_ai_model.get_embeddings(),
            index_name=settings.ATLAS_VECTOR_SEARCH_INDEX_NAME,
            relevance_score_fn="cosine",
        )
        return vector_store
