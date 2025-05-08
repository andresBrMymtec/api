from pydantic import BaseModel, Field
from typing import List, Optional, Tuple


class ChatRequest(BaseModel):
    id_usuario: int
    id_cliente: int
    id_sesion: str
    esDux: bool
    esFux: bool
    esDuxGT: bool
    versionSistema: str
    input: str
    chatHistory: Optional[List[Tuple[str, str]]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    status: int
    response: str
