"""Unit I (Paper Analyzer) & Unit II (NLP Lab) API Router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AnalysisLog, ResearchPaper
from app.schemas import NgramRequest, TextRequest, TfidfRequest, WordNetRequest
from app.services.keyword_extraction import extract_information
from app.services.ngram import analyze_ngram_language_model
from app.services.pos_tagger import pos_tag_text
from app.services.preprocessing import analyze_text_unit1
from app.services.tfidf import compute_tfidf_for_text
from app.services.wordnet_service import analyze_wordnet

router = APIRouter(prefix="/api", tags=["NLP Analyzer & Lab"])


def _log_analysis(db: Session, paper_id: str | None, module_name: str) -> None:
    try:
        db.add(AnalysisLog(paper_id=paper_id, module_name=module_name))
        db.commit()
    except Exception:
        db.rollback()


@router.post("/analyze")
def analyze_unit1(req: TextRequest, db: Session = Depends(get_db)):
    result = analyze_text_unit1(req.text)
    _log_analysis(db, req.paper_id, "unit1_analyzer")
    return result


@router.post("/nlp/pos-tag")
def nlp_pos_tag(req: TextRequest, db: Session = Depends(get_db)):
    result = pos_tag_text(req.text)
    _log_analysis(db, req.paper_id, "unit2_pos_tag")
    return result


@router.post("/nlp/tfidf")
def nlp_tfidf(req: TfidfRequest, db: Session = Depends(get_db)):
    text = (req.text or "").strip()
    if not text and req.paper_id:
        paper = db.query(ResearchPaper).filter(ResearchPaper.paper_id == req.paper_id).first()
        if not paper:
            raise HTTPException(status_code=404, detail=f"Paper '{req.paper_id}' not found.")
        text = f"{paper.title}. {paper.abstract}"
    if not text:
        raise HTTPException(status_code=400, detail="Provide either 'text' or a valid 'paper_id'.")
    _log_analysis(db, req.paper_id, "unit2_tfidf")
    return compute_tfidf_for_text(db, target_text=text, top_k=req.top_k)


@router.post("/nlp/ngrams")
def nlp_ngrams(req: NgramRequest, db: Session = Depends(get_db)):
    return analyze_ngram_language_model(db, context=req.context, custom_text=req.text, n=req.n)


@router.post("/nlp/extract")
def nlp_extract(req: TextRequest, db: Session = Depends(get_db)):
    _log_analysis(db, req.paper_id, "unit2_extract")
    return extract_information(req.text)


@router.post("/nlp/wordnet")
def nlp_wordnet(req: WordNetRequest):
    return analyze_wordnet(word=req.word, sentence=req.sentence, compare_word=req.compare_word)
