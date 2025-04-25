from fastapi import APIRouter, File, HTTPException, UploadFile


document_router = APIRouter()


@document_router.post("/")
async def add_documents(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=500, detail="Solo se permiten archivos PDF")
    pass


@document_router.patch("/")
async def patch_documents():
    pass


@document_router.delete("/")
async def del_documents():
    pass
