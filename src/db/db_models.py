from pydantic import BaseModel


class CrearRegistroModel(BaseModel):
    usuario: str
    id_sesion: int
    pregunta: str
    respuesta: str
