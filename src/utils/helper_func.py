from langchain_core.messages import AIMessage, HumanMessage
from typing import List, Tuple

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