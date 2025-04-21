# from typing import Annotated
# from requests import Session
# from src.db.schemas import Chats
# from src.db.db_service import add_model
# from src.db.databases import local_session
from src.rag.chat_controller import get_response
from fastapi import APIRouter, Depends, HTTPException
from src.models.chat_model import ChatRequest, ChatResponse

chat_router = APIRouter()


# def get_db():
#     db = local_session()
#     try:
#         yield db
#     finally:
#         db.close()


# db_deps = Annotated[Session, Depends(get_db)]


@chat_router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):

    user_input = request.input
    chat_history = request.chatHistory

    try:
        output = await get_response(user_input, chat_history)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ChatResponse(response=output)

    # chat_model = Chats(
    #     usuario=request.usuario,
    #     id_sesion=request.id_sesion,
    #     pregunta=user_input,
    #     respuesta=output

    # )

    # add_model(db, chat_model)
