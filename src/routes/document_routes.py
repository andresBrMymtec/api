import os
import base64
import binascii
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from src.utils.config import Settings
from src.utils.helper_func import MD_a_documentos, pdf_a_documentos
from src.db.async_db import get_async_db
from src.rag.vector_store import get_store, get_collection
from src.models.document_models import AddDocumentModel, AddDocumentRTAModel, DelDocumentRTAModel, UpdateDocumentModel, UpdateDocumentRTAModel

vector_store = get_store()
document_router = APIRouter()
settings: Settings = Settings()


# @document_router.post("/")
# def add_documents(request: AddDocumentModel):
#     contenido = request.contenido
#     campos = request.model_dump(exclude={"contenido"})
#     try:
#         b = base64.b64decode(contenido, validate=True)

#     except binascii.Error:
#         raise HTTPException(
#             status_code=500, detail="No es válido el base64")

#     file = f"src/temp/{request.fuente}.pdf"
#     try:
#         with open(file, "wb") as f:
#             f.write(b)

#         docs = pdf_a_documentos(file, campos)

#         ids = vector_store.add_documents(documents=docs)

#         return AddDocumentRTAModel(status=201, ids=ids)

#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Error.{e}")

#     finally:
#         try:
#             os.remove(file)
#         except Exception as e:
#             raise HTTPException(
#                 status_code=500, detail=f"No se pudo eliminar temp.{e}")


# @document_router.patch("/", response_model=UpdateDocumentRTAModel)
# async def patch_documents(request: AddDocumentModel):
#     campos = request.model_dump(exclude_unset=True, exclude={"contenido"})
#     body = request.model_dump(exclude_unset=True)

#     if id is None:
#         raise HTTPException(
#             status_code=500, detail="Debe ingresar un nombre de documento a editar.")

#     db = get_collection()
#     query_filter = {"file_id": id}

#     if 'contenido' in body:
#         contenido = body['contenido']
#         # --------VALIDAR EL BASE64----------
#         try:
#             b = base64.b64decode(contenido, validate=True)
#         except binascii.Error:
#             raise HTTPException(
#                 status_code=500, detail="No es un valido el base64")

#         # --------EXTRAER CAMPOS ORIGINALES----------
#         campos_originales = db.find_one(
#             query_filter, {"_id": False, "embedding": False, "text": False})

#         # --------BORRAR EL DOCUMENTO VIEJO----------
#         try:
#             result = db.delete_many(query_filter)
#         except Exception as e:
#             raise HTTPException(
#                 status_code=500, detail=f"No se pudo eliminar el documento.{e}")
#         if result.deleted_count == 0:
#             raise HTTPException(
#                 status_code=500, detail="No se encontro un documento con ese nombre")

#         # --------SUBIR EL DOCUMENTO NUEVO----------
#         file = f"src/temp/{campos_originales['fuente']}.pdf"
#         try:
#             with open(file, "wb") as f:
#                 f.write(b)

#             docs = pdf_a_documentos(file, campos_originales)

#             vector_store.add_documents(documents=docs)

#         except Exception as e:
#             raise HTTPException(
#                 status_code=500, detail=f"Error.{e}")

#         finally:
#             try:
#                 os.remove(file)
#             except Exception as e:
#                 raise HTTPException(
#                     status_code=500, detail=f"No se pudo eliminar temp.{e}")

#     # --------UPDATE DE CAMPOS----------
#     if campos:
#         update = {'$set': campos}
#         result = db.update_many(query_filter, update)
#         if result.matched_count == 0:
#             raise HTTPException(
#                 status_code=500, detail="No se encontro un documento con ese nombre")

#     return UpdateDocumentRTAModel(status=200, data=f"Se actualizó el documento con id: {id}")


@document_router.delete("/{id}", response_model=DelDocumentRTAModel)
async def del_documents(id: int = None, db=Depends(get_async_db)):
    if id is None:
        raise HTTPException(
            status_code=500, detail="Debe ingresar un id de documento a eliminar.")

    query_filter = {"file_id": id}

    db = get_collection()
    try:
        update = {'$set': {"activo": False}}
        result = await db.update_many(query_filter, update)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"No se pudo eliminar el documento.{e}")
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=500, detail="No se encontro un documento con ese nombre")

    return DelDocumentRTAModel(status=200, data=query_filter)


@document_router.post("/", response_model=AddDocumentRTAModel)
async def add_or_update(request: AddDocumentModel, db=Depends(get_async_db)):
    id: int = request.file_id
    campos: Dict[str, Any] = request.model_dump(
        exclude_unset=True, exclude={"contenido"})
    campos['file_id'] = request.file_id + 1000
    query_filter: Dict[str, str] = {"file_id": id}
    existe = await db.find_one(query_filter)
    contenido: str | None = None if request.contenido.strip() == "" else request.contenido
    print("contenido ", contenido)
    # --------SI EXISTE EL ARTICULO----------
    if existe:
        print("Existe")
        if contenido is not None:
            print("Contenido not None ni empty")
            # --------BORRAR EL DOCUMENTO VIEJO----------
            try:
                result = await db.delete_many(query_filter)
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"No se pudo eliminar el documento.{e}")
            if result.deleted_count == 0:
                raise HTTPException(
                    status_code=500, detail="No se encontro un documento con ese nombre")
            # --------SUBIR EL DOCUMENTO NUEVO----------
            try:
                docs = MD_a_documentos(contenido, campos)
                vector_store.add_documents(documents=docs)
                return AddDocumentRTAModel(status=200, data=f"Se actualizó el documento con id: {id}")

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Error.{e}")
        # --------UPDATE DE CAMPOS----------
        if campos:
            update = {'$set': campos}
            result = await db.update_many(query_filter, update)
            if result.matched_count == 0:
                raise HTTPException(
                    status_code=500, detail="No se encontro un documento con ese nombre")

        return AddDocumentRTAModel(status=200, data=f"Se actualizó el documento con id: {id}")
    # --------SI NO EXISTE EL ARTICULO----------
    try:
        docs = MD_a_documentos(contenido, campos)
        vector_store.add_documents(documents=docs)
        return AddDocumentRTAModel(status=200, data=f"Se agregó el documento con id: {id}")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error.{e}")
