"""ResearchLens FastAPI Application Entrypoint."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, SessionLocal, engine
from app.routers import analyzer, discourse, insights, papers, search, semantic, summarizer
from app.services.nltk_setup import get_nltk_status
from app.utils.dataset_loader import seed_papers_if_empty


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_papers_if_empty(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="ResearchLens API",
    description="NLP-Based Academic Research Paper Analysis, Semantic Search and Summarization Platform (NLPLM Units I–V).",
    version="1.0.0",
    lifespan=lifespan,
)

cors_origins_raw = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
cors_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(papers.router)
app.include_router(search.router)
app.include_router(analyzer.router)
app.include_router(semantic.router)
app.include_router(discourse.router)
app.include_router(summarizer.router)
app.include_router(insights.router)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "ResearchLens Backend",
        "nltk_resources": get_nltk_status(),
    }
