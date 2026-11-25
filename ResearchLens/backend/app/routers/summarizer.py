"""Unit V: AI Summarizer & ROUGE Evaluation API Router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AnalysisLog
from app.schemas import EvaluateSummaryRequest, SummarizeRequest
from app.services.evaluation_service import evaluate_rouge
from app.services.summarization_service import get_summarizer_status, summarize_text

router = APIRouter(prefix="/api/summarize", tags=["AI Summarizer"])


@router.get("/status")
def summarizer_status():
    return get_summarizer_status()


@router.post("")
def summarize(req: SummarizeRequest, db: Session = Depends(get_db)):
    try:
        db.add(AnalysisLog(paper_id=req.paper_id, module_name="unit5_summarizer"))
        db.commit()
    except Exception:
        db.rollback()
    return summarize_text(
        text=req.text,
        length=req.length,
        instruction=req.instruction,
        use_hf=req.use_hf,
    )


@router.post("/evaluate")
def summarize_evaluate(req: EvaluateSummaryRequest):
    return evaluate_rouge(req.generated_summary, req.reference_summary)
