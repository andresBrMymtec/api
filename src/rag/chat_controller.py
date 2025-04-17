from typing import List, Tuple
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from src.rag.retriever import faiss_retriever as retriever
from src.utils.helper_func import format_docs, _format_chat_history
from src.rag.llm import OpenAiModels

llm: OpenAiModels = OpenAiModels()

template = """
Eres un asistente Atencion al Cliente de una aplicacion llamada Dux.
No debes responder NADA de tu propio conocimiento.
Utiliza el siguiente contexto y historial de chat para responder la pregunta. Interpreta el contexo para que el usuario comprenda.
Cuando respondas quiero que digas de que fuente obtuviste la informacion y provee la url del documento (obtenidos de los metadatos del contexto).
Si no encuentras la respuesta en los documentos, di que no lo encuentras y pide reformular la pregunta y no menciones funtes ni urls.
Si no sabes la respuesta, di simplemente que no lo sabes.

Historial de Chat:
{chat_history}

Contexto:
{data}

Pregunta: {input}


Si no encuentras la respuesta en los documentos, di que no lo encuentras y pide reformular la pregunta y no menciones funtes ni urls.
Si no sabes la respuesta, di simplemente que no lo sabes.
"""
prompt = ChatPromptTemplate.from_template(template)


chain = (
    {
        "data":  RunnableLambda(lambda x: retriever.invoke(x["input"])) | format_docs,
        "input": lambda x: x["input"],
        "chat_history": lambda x: _format_chat_history(x["chat_history"]),
    }
    # | RunnableLambda(lambda x: (print("➡️ Payload to prompt:", x), x)[1])
    | prompt
    | llm.get_llm()
    | StrOutputParser()
)


def get_response(input: str, chat_history: List[Tuple[str, str]] = []):

    rta = chain.invoke({"input": input, "chat_history": chat_history})

    return rta
