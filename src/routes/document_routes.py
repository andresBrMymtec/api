import os
import base64
import binascii
from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from pymongo import AsyncMongoClient
from src.utils.config import Settings
from src.utils.helper_func import pdf_a_documentos
from src.rag.vector_store import get_store, get_collection
from src.models.document_models import AddDocumentModel, AddDocumentRTAModel, DelDocumentRTAModel, UpdateDocumentModel, UpdateDocumentRTAModel

vector_store = get_store()
document_router = APIRouter()
settings: Settings = Settings()


@document_router.post("/")
def add_documents(request: AddDocumentModel):
    archivo = request.archivo
    campos = request.model_dump(exclude={"archivo"})
    try:
        b = base64.b64decode(archivo, validate=True)

    except binascii.Error:
        raise HTTPException(
            status_code=500, detail="No es válido el base64")

    file = f"src/temp/{request.fuente}.pdf"
    try:
        with open(file, "wb") as f:
            f.write(b)

        docs = pdf_a_documentos(file, campos)

        ids = vector_store.add_documents(documents=docs)

        return AddDocumentRTAModel(status=201, ids=ids)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error.{e}")

    finally:
        try:
            os.remove(file)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"No se pudo eliminar temp.{e}")


@document_router.delete("/{id}", response_model=DelDocumentRTAModel)
async def del_documents(id: int = None):
    if int is None:
        raise HTTPException(
            status_code=500, detail="Debe ingresar un nombre de documento a eliminar.")

    query_filter = {"file_id": id}

    docs = get_collection()
    try:
        result = docs.delete_many(query_filter)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"No se pudo eliminar el documento.{e}")
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=500, detail="No se encontro un documento con ese nombre")

    return DelDocumentRTAModel(status=200, data=query_filter)


@document_router.patch("/{id}", response_model=UpdateDocumentRTAModel)
async def patch_documents(request: UpdateDocumentModel, id: int):
    campos = request.model_dump(exclude_unset=True, exclude={"archivo"})
    body = request.model_dump(exclude_unset=True)

    if id is None:
        raise HTTPException(
            status_code=500, detail="Debe ingresar un nombre de documento a editar.")

    db = get_collection()
    query_filter = {"file_id": id}

    if 'archivo' in body:
        archivo = body['archivo']
        # --------VALIDAR EL BASE64----------
        try:
            b = base64.b64decode(archivo, validate=True)
        except binascii.Error:
            raise HTTPException(
                status_code=500, detail="No es un valido el base64")

        # --------EXTRAER CAMPOS ORIGINALES----------
        campos_originales = db.find_one(
            query_filter, {"_id": False, "embedding": False, "text": False})

        # --------BORRAR EL DOCUMENTO VIEJO----------
        try:
            result = db.delete_many(query_filter)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"No se pudo eliminar el documento.{e}")
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=500, detail="No se encontro un documento con ese nombre")

        # --------SUBIR EL DOCUMENTO NUEVO----------
        file = f"src/temp/{campos_originales['fuente']}.pdf"
        try:
            with open(file, "wb") as f:
                f.write(b)

            docs = pdf_a_documentos(file, campos_originales)

            vector_store.add_documents(documents=docs)

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error.{e}")

        finally:
            try:
                os.remove(file)
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"No se pudo eliminar temp.{e}")

    # --------UPDATE DE CAMPOS----------
    if campos:
        update = {'$set': campos}
        result = db.update_many(query_filter, update)
        if result.matched_count == 0:
            raise HTTPException(
                status_code=500, detail="No se encontro un documento con ese nombre")

    return UpdateDocumentRTAModel(status=200, data=f"Se actualizó el documento con id: {id}")
