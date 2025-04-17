from langchain_community.vectorstores import FAISS
from typing import Literal
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from src.utils.config import Settings
from src.rag.llm import OpenAiModels


settings: Settings = Settings()
open_ai_model: OpenAiModels = OpenAiModels()
# Conexión a MongoDB Atlas


class VectorStore:

    def __init__(self, store: str):
        self.client = MongoClient(settings.MONGODB_ATLAS_CLUSTER_URI)
        self.MONGODB_COLLECTION = self.client[settings.DB_NAME][settings.COLLECTION_NAME]
        self.store: Literal["mongo", "faiss"] = store

    def ping(self):

        if self.store == 'mongo':
            try:
                self.client.admin.command('ping')
                print("Pinged your deployment. You successfully connected to MongoDB!")
            except Exception as e:
                print(e)

        else:
            print("Faiss no tiene Ping")

    def get_store(self):

        if self.store == 'mongo':
            vector_store = MongoDBAtlasVectorSearch(
                collection=self.MONGODB_COLLECTION,
                embedding=open_ai_model.get_embeddings(),
                index_name=settings.ATLAS_VECTOR_SEARCH_INDEX_NAME,
                relevance_score_fn="cosine",
            )

        elif self.store == 'faiss':
            vector_store = FAISS.load_local(
                "src/faiss-index",
                open_ai_model.get_embeddings(),
                allow_dangerous_deserialization=True)

        return vector_store
