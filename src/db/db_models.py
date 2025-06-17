from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel


class ChatAudit(BaseModel):
    id_usuario: int
    pregunta: str
    historial: List[Any]
    filtros: Dict[str, Any]
    documentos: List[Any]
    respuesta: str
    fecha: datetime = datetime.now()
