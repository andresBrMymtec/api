from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.utils.config import Settings
import os

settings: Settings = Settings()

# Configuración de la clave API de OpenAI
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


class OpenAiModels:
    def __init__(self, model_ai: str = "o3-mini", embeddings: str = "text-embedding-3-small"):

        self.model = model_ai
        self.llm = ChatOpenAI(model_name=model_ai)
        self.embeddings = OpenAIEmbeddings(model=embeddings, dimensions=1024)

    def get_llm(self):
        return self.llm

    def get_embeddings(self):
        return self.embeddings
