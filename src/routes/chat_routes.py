from src.rag.chat_controller import get_response
from fastapi import APIRouter, HTTPException
from src.models.chat_model import ChatRequest, ChatResponse

chat_router = APIRouter()


@chat_router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):

    user_input = request.input
    chat_history = request.chatHistory
    filtros = request.filtros

    if request.esDux and request.esDux:
        lista_or = [{'esDux': True}, {'esFux': True}]
        filtros["$or"] = lista_or
    else:
        if request.esDux:
            filtros['esDux'] = request.esDux
        if request.esFux:
            filtros['esFux'] = request.esFux
    if request.esDuxGT:
        filtros['esDuxGT'] = request.esDuxGT
    if request.esDuxim:
        filtros['esDuxim'] = request.esDuxim

    filtros['versionSistema'] = request.versionSistema
    print(filtros)
    try:
        output = await get_response(user_input, filtros, chat_history)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ChatResponse(status=200, response=output)
