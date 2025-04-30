from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.utils.config import Settings
import os

settings: Settings = Settings()

# Configuración de la clave API de OpenAI
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


class OpenAiModels:
    def __init__(self, model_ai: str | None = None, temp: float | None = None, embeddings: str = "text-embedding-3-small"):

        self.model = model_ai
        self.embeddings = embeddings
        self.temp = temp

    def get_llm(self):
        if self.temp is None:
            return ChatOpenAI(model_name=self.model)

        return ChatOpenAI(model_name=self.model, temperature=self.temp)

    def get_embeddings(self):
        return OpenAIEmbeddings(model=self.embeddings, dimensions=settings.DIMENSIONS)
