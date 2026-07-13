from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent import ask_agent
from ai_provider import create_embedding
from db import count_chunks, create_table_if_not_exists, get_connection, insert_chunk, list_chunks
from settings import settings

app = FastAPI(
    title=settings.app_name,
    description="Agente RAG con Azure SQL para el Entregable 5.",
    version="1.0.0",
)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)


class IngestRequest(BaseModel):
    title: str = Field(..., min_length=3)
    source: str = Field(default="manual")
    content: str = Field(..., min_length=10)


@app.get("/")
def read_root() -> dict:
    return {
        "message": settings.app_name,
        "environment": settings.app_env,
        "routes": ["/health", "/knowledge", "/ask", "/ingest", "/docs"],
    }


@app.get("/health")
def health() -> dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM dbo.knowledge_chunks")
        total_chunks = cursor.fetchone()[0]
        conn.close()
        return {
            "status": "ok",
            "database": "connected",
            "knowledge_chunks": total_chunks,
        }
    except Exception as error:
        return {
            "status": "error",
            "database": "not connected",
            "detail": str(error),
        }


@app.get("/knowledge")
def knowledge() -> dict:
    try:
        chunks = list_chunks()
        return {
            "total": len(chunks),
            "items": [
                {
                    "id": chunk["id"],
                    "title": chunk["title"],
                    "source": chunk["source"],
                    "created_at": chunk["created_at"],
                }
                for chunk in chunks
            ],
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.post("/ask")
def ask(request: AskRequest) -> dict:
    try:
        return ask_agent(request.question)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@app.post("/ingest")
def ingest(request: IngestRequest) -> dict:
    try:
        create_table_if_not_exists()
        embedding = create_embedding(request.content)
        embedding_model = (
            settings.embedding_model if settings.llm_provider == "openai" else "demo-embedding"
        )
        insert_chunk(
            title=request.title,
            source=request.source,
            content=request.content,
            embedding=embedding,
            embedding_model=embedding_model,
        )
        return {"status": "inserted", "knowledge_chunks": count_chunks()}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
