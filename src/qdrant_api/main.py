
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from api.routes import router as api_router


app = FastAPI(
    version="0.0.1",
    title="UNIFAGOC - RAG Stack API",
    description="RAG Lecture API and AI Platform for the Computer Science course at UNIFAGOC - Ubá MG"
)

app.include_router(api_router)