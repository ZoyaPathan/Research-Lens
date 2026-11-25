"""Unit IV: Discourse and Pragmatic Analysis API Router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AnalysisLog
from app.schemas import ConversationRequest, DiscourseAnalyzeRequest
from app.services.discourse_service import analyze_conversation_pragmatics, analyze_discourse_text

router = APIRouter(prefix="/api/discourse", tags=["Discourse & Pragmatics"])


@router.post("/analyze")
def discourse_analyze(req: DiscourseAnalyzeRequest, db: Session = Depends(get_db)):
    try:
        db.add(AnalysisLog(paper_id=req.paper_id, module_name="unit4_discourse"))
        db.commit()
    except Exception:
        db.rollback()
    return analyze_discourse_text(req.text)


@router.post("/conversation")
def discourse_conversation(req: ConversationRequest):
    return analyze_conversation_pragmatics(req.conversation)
