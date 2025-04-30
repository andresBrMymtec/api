from typing import Any, List, Optional
from pydantic import BaseModel, Base64Str


class AddDocumentModel(BaseModel):
    fuente: str
    url: str
    programa: str
    archivo: str


class AddDocumentRTAModel(BaseModel):
    status: int
    ids: List[str]


class UpdateDocumentModel(BaseModel):
    fuente: Optional[str] = None
    file_id: Optional[int] = None
    programa: Optional[str] = None
    contenido: Optional[str] = None
    url: Optional[str] = None
    archivo: Optional[str] = None


class DelteDocumentModel(BaseModel):
    fuente: Optional[Any] = None
    id: Optional[Any] = None


class DelDocumentRTAModel(BaseModel):
    status: int
    data: dict
