"""Smart Search API Router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.tfidf import search_papers_tfidf

router = APIRouter(prefix="/api", tags=["Smart Search"])


@router.get("/search")
def smart_search(
    q: str = Query(..., min_length=2, description="Natural language or keyword search query"),
    mode: str = Query("hybrid", description="hybrid | keyword"),
    top_k: int = Query(15, ge=1, le=50),
    db: Session = Depends(get_db),
):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
    return search_papers_tfidf(db, query=q.strip(), mode=mode, top_k=top_k)
