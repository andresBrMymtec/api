from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.http_error_handler import HttpErrorHandler
from src.routes.chat_routes import chat_router
from src.routes.document_routes import document_router
import src.db.schemas as Schemas
from src.db.databases import engine


app = FastAPI()

app.title = "DuxCopilot"
app.version = "1.0"

API_V = '/api/v1'
# Schemas.Base.metadata.create_all(bind=engine)


app.add_middleware(HttpErrorHandler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix=f"{API_V}/chat", tags=["Chats"])
app.include_router(
    document_router, prefix=f"{API_V}/docs", tags=["Documentos"])


@app.get("/")
def healthcheck():
    return {"status": "ok"}
