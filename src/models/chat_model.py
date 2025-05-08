from pydantic import BaseModel, Field
from typing import List, Optional, Tuple


class ChatRequest(BaseModel):
    id_usuario: int
    id_sesion: str
    chatHistory: Optional[List[Tuple[str, str]]] = Field(default_factory=list)
    input: str


class ChatResponse(BaseModel):
    status: int
    response: str
