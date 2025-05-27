from fastapi import APIRouter, HTTPException
from src.utils.helper_func import pdf_a_documentos
from src.rag.vector_store import get_store, get_collection
from src.models.document_models import AddDocumentModel, AddDocumentRTAModel, DelDocumentRTAModel, UpdateDocumentModel
import base64
import binascii

vector_store = get_store()
document_router = APIRouter()


@document_router.post("/")
async def add_documents(request: AddDocumentModel):
    request = request.model_dump()

    try:
        b = base64.b64decode(request["archivo"], validate=True)

    except binascii.Error:
        raise HTTPException(
            status_code=500, detail="No es un valido el base64")

    try:

        with open("src/temp/file.pdf", "wb") as f:
            f.write(b)

        docs = pdf_a_documentos(
            'src/temp/file.pdf', request['fuente'], request['url'], request['programa'])

        ids = vector_store.add_documents(documents=docs)

        return AddDocumentRTAModel(status=201, ids=ids)

    except:
        raise HTTPException(
            status_code=500, detail="Algo salio mal")


@document_router.delete("/{id}")
async def del_documents(nombre: str = None):
    if nombre is None:
        raise HTTPException(
            status_code=500, detail="Debe ingresar un nombre de documento a eliminar.")

    query_filter = {"fuente": nombre}

    docs = get_collection()
    result = docs.delete_many(query_filter)
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=500, detail="No se encontro un documento con ese nombre")

    return DelDocumentRTAModel(status=200, data=query_filter)


@document_router.patch("/{id}")
async def patch_documents(request: UpdateDocumentModel, id: str = None):
    request = request.model_dump(exclude_unset=True)
    if id is None:
        raise HTTPException(
            status_code=500, detail="Debe ingresar un nombre de documento a editar.")

    if hasattr(request, 'archivo'):
        try:
            b = base64.b64decode(request["archivo"], validate=True)
        except binascii.Error:
            raise HTTPException(
                status_code=500, detail="No es un valido el base64")

    request = request.model_dump(exclude_unset=True)
    query_filter = {"fuente": id}
    update = {'$set': request}
    docs = get_collection()
    result = docs.update_many(query_filter, update)
    if result.matched_count == 0:
        raise HTTPException(
            status_code=500, detail="No se encontro un documento con ese nombre")

    return DelDocumentRTAModel(status=200, data=request)
