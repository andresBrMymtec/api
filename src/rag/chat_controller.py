from typing import List, Tuple
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from src.rag.retriever import faiss_retriever as retriever
# from src.rag.retriever import mq_retriever as retriever
from src.utils.helper_func import format_docs, _format_chat_history
from src.rag.llm import OpenAiModels

llm: OpenAiModels = OpenAiModels(model_ai='gpt-4.1-mini', temp=1)
# llm: OpenAiModels = OpenAiModels(model_ai='gpt-4.1-nano')
# llm: OpenAiModels = OpenAiModels(model_ai='gpt-4o-mini')
# llm: OpenAiModels = OpenAiModels(model_ai='o3-mini')
# llm: OpenAiModels = OpenAiModels(model_ai='o4-mini')

template = """
Eres un asistente Atencion al Cliente. Las preguntas estan referidas siempre al sistema Dux.
No debes responder NADA de tu propio conocimiento.
Utiliza el siguiente contexto (contenido y metadatos) e historial de chat para responder la pregunta. Interpreta el contexo para que el usuario comprenda.
Cuando respondas quiero que digas de que fuente obtuviste la informacion y provee la url del documento (obtenidos de los metadatos del contexto).

Historial de Chat:
{chat_history}

Contexto:
{data}

Pregunta: {input}

Si no encuentras la respuesta en los documentos, di que no lo encuentras y pide reformular la pregunta y no menciones funtes ni urls.

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


async def get_response(input: str, chat_history: List[Tuple[str, str]] = None):
    if chat_history is None:
        chat_history = []

    rta = await chain.ainvoke({"input": input, "chat_history": chat_history})

    return rta
