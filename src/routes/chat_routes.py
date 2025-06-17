from src.rag.chat_controller import get_response
from fastapi import APIRouter, HTTPException
from src.models.chat_model import ChatRequest, ChatResponse
from src.db.db_models import ChatAudit
from src.db.audit_db import get_collection

chat_router = APIRouter()

chat_col = get_collection()


@chat_router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):

    user_input = request.input
    chat_history = request.chatHistory
    # filtros = request.filtros
    filtros = {}
    if request.esDux or request.esFux or request.esDuxGT or request.esDuxim:
        lista_or = [{'esDux': True}, {'esFux': True},
                    {'esDuxGT': True}, {'esDuxim': True}]
        filtros["$or"] = lista_or
    # else:
    #     if request.esDux:
    #         filtros['esDux'] = request.esDux
    #     if request.esFux:
    #         filtros['esFux'] = request.esFux
    # if request.esDuxGT:
    #     filtros['esDuxGT'] = request.esDuxGT
    # if request.esDuxim:
    #     filtros['esDuxim'] = request.esDuxim

    # meno o igual a los ultimos nrs
    filtros['versionSistema'] = {"$lte": request.versionSistema}
    filtros['activo'] = True

    print(filtros)
    try:
        output, docs = await get_response(user_input, filtros, chat_history)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    registro: ChatAudit = ChatAudit(id_usuario=request.id_usuario,
                                    pregunta=user_input,
                                    historial=chat_history,
                                    filtros=filtros,
                                    documentos=docs,
                                    respuesta=output)
    try:
        await chat_col.insert_one(registro.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ChatResponse(status=200, response=output)
