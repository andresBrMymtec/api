from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Tuple


class ChatRequest(BaseModel):
    id_usuario: int
    id_cliente: int
    id_sesion: str
    esDux: bool
    esFux: bool
    esDuxGT: bool
    esDuxim: bool
    versionSistema: str
    input: str
    chatHistory: Optional[List[Tuple[str, str]]]
    filtros: Optional[Dict[str, str]]


class ChatResponse(BaseModel):
    status: int
    response: str
