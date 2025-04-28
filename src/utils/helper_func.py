from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.messages import AIMessage, HumanMessage
from openai_func import gpt_tags
from typing import List, Tuple
import os


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


def pdf_a_documento(doc_folder, doc_files_dir, url):
    documents = []

    for folder in doc_folder:

        doc_files = [f for f in os.listdir(
            os.path.join(doc_files_dir, folder))]

        for book_file in doc_files:

            file_path = os.path.join(doc_files_dir, folder, book_file)

            pdf_loader = PyPDFLoader(file_path)

            book_docs = pdf_loader.load()

            contenido = gpt_tags(file_path)

            for doc in book_docs:

                doc.metadata = {"fuente": book_file, "contenido": contenido,
                                "url": f"{url}/{book_file}", "sistema": folder}

                documents.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512, chunk_overlap=128)

    docs = text_splitter.split_documents(documents)

    return docs
