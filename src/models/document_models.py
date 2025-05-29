from typing import Any, List, Optional
from pydantic import BaseModel


class AddDocumentModel(BaseModel):
    fuente: str
    file_id: Optional[int | str] = None
    url: str
    archivo: str
    esDux: bool
    esFux: bool
    esDuxGT: bool
    esDuxim: bool
    versionSistema: str
    area: str
    programa: str


class AddDocumentRTAModel(BaseModel):
    status: int
    ids: List[str]


class UpdateDocumentModel(BaseModel):
    fuente: Optional[str] = None
    file_id: Optional[int | str] = None
    esDux: Optional[bool] = None
    esFux: Optional[bool] = None
    esDuxGT: Optional[bool] = None
    esDuxim: Optional[bool] = None
    versionSistema: Optional[str] = None
    area: Optional[str] = None
    programa: Optional[str] = None
    url: Optional[str] = None
    archivo: Optional[str] = None


class UpdateDocumentRTAModel(BaseModel):
    status: int
    data: str


class DelteDocumentModel(BaseModel):
    fuente: Optional[Any] = None
    id: Optional[Any] = None


class DelDocumentRTAModel(BaseModel):
    status: int
    data: dict
