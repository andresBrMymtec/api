# from src.rag.vector_store import get_store
# from src.utils.config import Settings
# from langchain_core.prompts import PromptTemplate
# from src.rag.llm import OpenAiModels
# from langchain.chains.query_constructor.base import AttributeInfo
# from langchain.retrievers import SelfQueryRetriever


# settings: Settings = Settings()


# mongo_retriever = get_store().as_retriever(
#     search_kwargs={'pre_filter': {'esDux': True}})
# open_ai_model = OpenAiModels(model_ai="gpt-4.1-nano")

# llm = open_ai_model.get_llm()

# Configuración del vector store


# Información de los campos de metadatos
# metadata_field_info = [
#     AttributeInfo(
#         name="fuente",
#         description="El nombre del archivo del instructivo",
#         type="string",
#     ),
#     AttributeInfo(
#         name="contenido",
#         description="Lista de palabras clave de lo que encontraremos en el documento",
#         type="string",
#     ),
#     AttributeInfo(
#         name="url",
#         description="La url o link del documento original",
#         type="string",
#     ),
#     AttributeInfo(
#         name="sistema",
#         description="sistema el que pertenece el documento. Puede ser Dux, DuxGT, Duxim, Fux.",
#         type="string",
#     )
# ]

# Contenido de los documentos
# document_contents = "Intructivos operativos de Dux3 para atencion al cliente"


# mongo_sq_retriever = SelfQueryRetriever.from_llm(
#     llm=llm,
#     vectorstore=mongo_vector_db.get_store(),
#     document_contents=document_contents,
#     metadata_field_info=metadata_field_info,
#     verbose=True
# )

# faiss_vector_db: VectorStore = VectorStore(store="faiss")

# faiss_retriever = faiss_vector_db.get_store().as_retriever()


# CUSTOM_QUERY_PROMPT = PromptTemplate(
#     input_variables=["question"],
#     template="""Como experto en búsqueda semántica, genera 3 variaciones únicas de la siguiente pregunta para recuperar documentos relevantes de una base de datos vectorial.

#     Contexto clave:
#     - Los documentos tienen metadatos que incluyen: **nombre del documento**, **contenido** y **url**
#     - Las consultas deben ser útiles para buscar tanto en metadatos como en el contenido interno
#     - Prioriza diversidad lingüística y conceptual en las variaciones

#     Estrategias recomendadas:
#     1. Usa sinónimos y términos técnicos equivalentes
#     2. Varía entre enfoques generales y específicos
#     3. Combina aspectos de nombre, descripción y objetivos en diferentes proporciones
#     4. Incluye posibles abreviaciones o acrónimos relevantes
#     5. Crea versiones que expliciten aspectos implícitos de la pregunta original

#     Pregunta original: {question}
#     """
# )
