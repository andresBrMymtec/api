from pydantic import BaseModel
from typing import List
from src.utils.config import Settings
from mistralai import DocumentURLChunk, Mistral, TextChunk
import json
from pathlib import Path

settings: Settings = Settings()

api_key = settings.MISTRAL_API_KEY
client = Mistral(api_key=api_key)

prompt_pdf: str = "Estos documentos son instructivos de una plataforma enfocada el comercio exterior llamada DUX\n" \
                  "Necesito que interpretes el docuemento y me hagas una lista de palabras o conceptos que aparecen en el instructivo que den conocimiento del contenido.\n" \
                  "Los documentos contienen un encabezado y una tabla para seguimiento de versiones que hay que desestimarlos.\n" \
                  "No necesariamente tienen que ser palabras sueltas. Pueden ser frases cortas. Como maximo 15 elementos en la lista. \n" \
                  "Estos conceptos o palabras clave son para ponerlos en un campo de metadatos de cada docuemento ya que estos se van a utilizar para una aplicacion RAG.\n"


class Tags(BaseModel):
    tags: List[str]


def load_and_extract(file_dir: str) -> dict:

    pdf = Path(file_dir)
    print("-----Cargado archivo: ", file_dir, "-----")
    uploaded_file = client.files.upload(
        file={
            "file_name": pdf.stem,
            "content": pdf.read_bytes(),
        },
        purpose="ocr",
    )

    signed_url = client.files.get_signed_url(
        file_id=uploaded_file.id, expiry=1)
    print("OK")

    print("-----Procesando: ", file_dir, "-----")

    chat_response = client.chat.parse(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": [
                    DocumentURLChunk(document_url=signed_url.url),
                    TextChunk(
                        text=(prompt_pdf)
                    ),
                ],
            }
        ],
        response_format=Tags,
        temperature=0.5,
    )

    # print(chat_response.choices[0].message.content)
    response_dict = json.loads(chat_response.choices[0].message.content)
    print("-----Finalizado: ", file_dir, "-----")

    return response_dict
