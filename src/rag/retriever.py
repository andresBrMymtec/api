from src.rag.vector_store import VectorStore
from src.rag.llm import OpenAiModels
from src.utils.config import Settings
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers import SelfQueryRetriever

settings: Settings = Settings()

open_ai_model = OpenAiModels()

# Configuración del vector store

# mongo_vector_db: VectorStore = VectorStore(store="mongo")

# # Información de los campos de metadatos
# metadata_field_info = [
#     AttributeInfo(
#         name="fuente",
#         description="El nombre del archivo del instructivo",
#         type="string",
#     ),
#     AttributeInfo(
#         name="objetivo",
#         description="El objetivo del instructivo y contenido",
#         type="string",
#     ),
#     AttributeInfo(
#         name="url",
#         description="La url o link del documento original",
#         type="string",
#     ),
#     AttributeInfo(
#         name="descripcion",
#         description="Breve descripcion del contenido del instructivo",
#         type="string",
#     )
# ]

# # Contenido de los documentos
# document_contents = "Intructivos operativos de Dux3 para atencion al cliente"

# mongo_retriever = SelfQueryRetriever.from_llm(
#     llm=open_ai_model.get_llm(),
#     vectorstore=mongo_vector_db.get_store(),
#     document_contents=document_contents,
#     metadata_field_info=metadata_field_info,
#     verbose=True
# )
faiss_vector_db: VectorStore = VectorStore(store="faiss")


faiss_retriever = faiss_vector_db.get_store().as_retriever()
