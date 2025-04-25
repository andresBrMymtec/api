from pydantic import BaseModel


class AddDocModel(BaseModel):
    nombre: str
    sistema: int


class ModifiDocModel(BaseModel):
    algo: str
