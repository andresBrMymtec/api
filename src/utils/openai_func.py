from openai import OpenAI
client = OpenAI()

prompt_pdf: str = "Estos documentos son instructivos de una plataforma enfocada el comercio exterior llamada DUX\n" \
                  "Necesito que interpretes el documento y me hagas una lista de palabras o conceptos que aparecen en el instructivo que den conocimiento del contenido.\n" \
                  "Los documentos contienen un encabezado y una tabla para seguimiento de versiones que hay que desestimarlos.\n" \
                  "No necesariamente tienen que ser palabras sueltas. Pueden ser frases cortas. Como maximo 15 elementos en la lista. \n" \
                  "Estos conceptos o palabras clave son para ponerlos en un campo de metadatos de cada docuemento ya que estos se van a utilizar para una aplicacion RAG.\n" \
                  "La respuesta debe ser EXACTAMENTE lo solicitado. Solo una lista se palabras separadas por comas."


def gpt_tags(path: str) -> str:
    print("-----Cargado archivo: ", path, "-----\n\n")
    file = client.files.create(
        file=open(path, "rb"),
        purpose="user_data"
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_id": file.id,
                    },
                    {
                        "type": "input_text",
                        "text": prompt_pdf,
                    },
                ]
            }
        ],
        temperature=0.3
    )
    return response.output_text
