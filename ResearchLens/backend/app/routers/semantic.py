"""Unit III: Semantic Analysis API Router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AnalysisLog
from app.schemas import SemanticAnalyzeRequest, SemanticSimilarityRequest
from app.services.semantic_service import analyze_semantics, compute_sentence_similarity

router = APIRouter(prefix="/api/semantic", tags=["Semantic Analysis"])


@router.post("/similarity")
def semantic_similarity(req: SemanticSimilarityRequest):
    return compute_sentence_similarity(req.sentence1, req.sentence2, method=req.method)


@router.post("/analyze")
def semantic_analyze(req: SemanticAnalyzeRequest, db: Session = Depends(get_db)):
    try:
        db.add(AnalysisLog(paper_id=req.paper_id, module_name="unit3_semantic"))
        db.commit()
    except Exception:
        db.rollback()
    return analyze_semantics(req.text, target_word=req.target_word)
