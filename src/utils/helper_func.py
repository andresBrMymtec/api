from fastapi import HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import AIMessage, HumanMessage
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from src.utils.config import Settings
from typing import Dict, List, Tuple
import binascii
import base64

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


def pdf_a_documentos(file_path: str, campos: Dict[str, str | int | bool]) -> List:

    documents = []
    pdf_loader = PyMuPDF4LLMLoader(file_path)

    book_docs = pdf_loader.load()

    for doc in book_docs:

        doc.metadata = campos

        documents.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.DIMENSIONS, chunk_overlap=128)

    docs = text_splitter.split_documents(documents)

    return docs


def validateBase64(archivo):
    try:
        b = base64.b64decode(archivo, validate=True)

    except binascii.Error:
        raise HTTPException(
            status_code=500, detail="No es válido el base64")
