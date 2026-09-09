from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.query import router as query_router
from app.core.config import settings
from app.services.retrieval import Retriever


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.retriever = Retriever(
        Path("data/documents"),
        Path(settings.vector_store_path),
    )
    yield


app = FastAPI(
    title="StudyMate API",
    description="Grounded retrieval API for the StudyMate graduation project.",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(query_router)