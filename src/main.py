from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.http_error_handler import HttpErrorHandler
from src.routes.chat_routes import chat_router
import src.db.schemas as Schemas
from src.db.databases import engine
from contextlib import asynccontextmanager
import httpx
import asyncio


# async def self_ping():
#     async with httpx.AsyncClient() as client:
#         while True:
#             await asyncio.sleep(180)  # 3 minutos = 180 segundos
#             try:
#                 response = await client.get("https://dux-copilot-testing.onrender.com/")
#                 print(f"Self-ping status: {response.status_code}")
#             except Exception as e:
#                 print(f"Error en self-ping: {str(e)}")


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Iniciar la tarea al iniciar la app
#     asyncio.create_task(self_ping())
#     yield
#     # (Opcional) Código de limpieza al apagar la app


app = FastAPI()

app.title = "DuxCopilot"
app.version = "1.0"

# Schemas.Base.metadata.create_all(bind=engine)


app.add_middleware(HttpErrorHandler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(chat_router, prefix="/chat", tags=["Chats"])


@app.get("/")
def healthcheck():
    return {"status": "ok"}
