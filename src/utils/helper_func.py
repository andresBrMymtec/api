from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import AIMessage, HumanMessage
from typing import List, Tuple
from src.utils.config import Settings

settings: Settings = Settings()


def format_docs(docs):
    formatted = []
    for doc in docs:
        # Combinar contenido y metadata
        doc_str = f"Contenido: {doc.page_content}\nMetadatos: {doc.metadata}"
        formatted.append(doc_str)
    return "\n\n".join(formatted)


def _format_chat_history(chat_history: List[Tuple[str, str]]):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer


def pdf_a_documentos(file_path: str, nombre: str, url: str, programa: str) -> List:

    documents = []
    pdf_loader = PyPDFLoader(file_path)

    book_docs = pdf_loader.load()

    for doc in book_docs:

        doc.metadata = {"fuente": nombre, "contenido": "tags",
                        "url": f"{url}/{nombre}", "programa": programa}

        documents.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.DIMENSIONS, chunk_overlap=128)

    docs = text_splitter.split_documents(documents)

    return docs
