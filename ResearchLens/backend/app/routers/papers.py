"""Papers and Domains API Router."""

from __future__ import annotations

import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ResearchPaper
from app.schemas import PaginatedPapersOut, PaperOut

router = APIRouter(prefix="/api", tags=["Papers"])


def _to_paper_out(p: ResearchPaper) -> PaperOut:
    kw_list = [k.strip() for k in (p.keywords or "").split(",") if k.strip()]
    return PaperOut(
        paper_id=p.paper_id,
        title=p.title,
        abstract=p.abstract,
        authors=p.authors,
        research_domain=p.research_domain,
        keywords=p.keywords,
        keywords_list=kw_list,
        methodology=p.methodology,
        publication_year=p.publication_year,
    )


@router.get("/papers", response_model=PaginatedPapersOut)
def list_papers(
    search: Optional[str] = Query(None, description="Filter by title or keyword"),
    domain: Optional[str] = Query(None, description="Filter by research domain"),
    year: Optional[int] = Query(None, description="Filter by publication year"),
    sort: str = Query("year_desc", description="year_desc | year_asc | title_asc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(ResearchPaper)

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            (ResearchPaper.title.ilike(term))
            | (ResearchPaper.keywords.ilike(term))
            | (ResearchPaper.authors.ilike(term))
        )
    if domain and domain.strip() and domain != "All":
        query = query.filter(ResearchPaper.research_domain == domain.strip())
    if year:
        query = query.filter(ResearchPaper.publication_year == year)

    if sort == "year_asc":
        query = query.order_by(ResearchPaper.publication_year.asc(), ResearchPaper.paper_id.asc())
    elif sort == "title_asc":
        query = query.order_by(ResearchPaper.title.asc())
    else:
        query = query.order_by(ResearchPaper.publication_year.desc(), ResearchPaper.paper_id.asc())

    total = query.count()
    total_pages = max(1, math.ceil(total / page_size))
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedPapersOut(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=[_to_paper_out(p) for p in items],
    )


@router.get("/papers/{paper_id}", response_model=PaperOut)
def get_paper(paper_id: str, db: Session = Depends(get_db)):
    paper = db.query(ResearchPaper).filter(ResearchPaper.paper_id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail=f"Paper '{paper_id}' not found.")
    return _to_paper_out(paper)


@router.get("/domains")
def list_domains(db: Session = Depends(get_db)):
    rows = (
        db.query(ResearchPaper.research_domain, func.count(ResearchPaper.id))
        .group_by(ResearchPaper.research_domain)
        .order_by(func.count(ResearchPaper.id).desc())
        .all()
    )
    years = (
        db.query(ResearchPaper.publication_year)
        .distinct()
        .order_by(ResearchPaper.publication_year.desc())
        .all()
    )
    return {
        "domains": [{"domain": d, "count": c} for d, c in rows],
        "years": [y[0] for y in years],
    }
