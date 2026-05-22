from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.ingest import router as ingest_router  
from app.api.routes.analytics import router as analytics_router
from app.api.routes.chat import router as chat_router
from app.api.routes.conversation import router as conversation_router


app = FastAPI(title="Ollive LLM Observability")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversation_router)
app.include_router(chat_router)
app.include_router(analytics_router)
app.include_router(ingest_router)


@app.get("/")
def root():
    return {"message": "Backend running"}