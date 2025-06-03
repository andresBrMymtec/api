from typing import List, Tuple
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from src.rag.vector_store import get_store

from src.utils.helper_func import format_docs, _format_chat_history
from src.rag.llm import OpenAiModels

llm: OpenAiModels = OpenAiModels(model_ai='gpt-4.1-mini', temp=0.1)

template = """
[CONTEXTO]
Eres un asistente de Atención al Cliente altamente preciso y obediente. 
SOLO debes responder usando la información del contexto proporcionado, nunca con conocimientos propios. 
Las preguntas están relacionadas exclusivamente con los sistemas Dux o Fux.
Las preguntas estan basadas en un Software de comercio internacional que se encarga de la gestión de operaciones como importaciones, exportaciones, despachos de aduana y todo lo relacioado al comercio exterior.


[IMPORTANTE!!! - INSTRUCCIONES OBLIGATORIAS]
1. NUNCA respondas con información que no esté en el contexto.
2. SIEMPRE interpretá y explicá la información para que el usuario la entienda claramente.
3. SI la respuesta incluye pasos, enumeralos de forma clara.
4. SI hay ambigüedad (por ejemplo, no se especifica si el procedimiento es para exportación o importación), pedí aclaración ANTES de responder.
5. SI NO encontrás la respuesta en el contexto, decí que no la encontrás y pedí reformular la pregunta. NO inventes ni completes con conocimientos propios, y no menciones funtes ni urls.
6. SIEMPRE al final de la respuesta incluí las fuentes utilizando exactamente este formato:
   - Cada documento citado debe tener su nombre entre los tags <FUENTE></FUENTE>.
   - El ID correspondiente, del metadato 'file_id' entre los tags <ID></ID>.
   - NUNCA uses la palabra "Fuente:" antes de los tags.
   - NO omitas esta parte si usás información de los documentos.


[EJEMPLO CORRECTO DE FUENTES]
<FUENTE>SISTEMA DUX - INSTRUCTIVO PSAD.pdf</FUENTE> <ID>1</ID>


[TU TAREA]
Leé el contexto, usá solo la información allí contenida, y seguí las reglas anteriores de forma estricta.

[Historial de Chat]:
{chat_history}

[Contexto]:
{data}

[Pregunta]: {input}
"""

prompt = ChatPromptTemplate.from_template(template)


async def get_response(input: str, filtros: dict, chat_history: List[Tuple[str, str]] = None):
    if chat_history is None:
        chat_history = []

    retriever = get_store().as_retriever(
        search_kwargs={'k': 5, 'pre_filter': filtros})
    docs_salida = []

    def extraer_doc(input):
        docs = retriever.invoke(input)
        [docs_salida.append(d) for d in docs]
        return format_docs(docs)

    chain = (
        {
            "data":  RunnableLambda(lambda x: extraer_doc(x["input"])),
            "input": lambda x: x["input"],
            "chat_history": lambda x: _format_chat_history(x["chat_history"]),
        }
        # | RunnableLambda(lambda x: (print("➡️ Payload to prompt:", x), x)[1])
        | prompt
        | llm.get_llm()
        | StrOutputParser()
    )
    try:
        rta = await chain.ainvoke({"input": input, "chat_history": chat_history})
    except Exception as e:
        print(e)
    return rta, docs_salida
