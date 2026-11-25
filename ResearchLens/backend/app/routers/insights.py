"""Research Insights & Dashboard Analytics API Router."""

from __future__ import annotations

from collections import Counter
from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AnalysisLog, ResearchPaper

router = APIRouter(prefix="/api/insights", tags=["Research Insights"])


@router.get("/overview")
def insights_overview(db: Session = Depends(get_db)):
    total_papers = db.query(func.count(ResearchPaper.id)).scalar() or 0
    total_domains = db.query(func.count(func.distinct(ResearchPaper.research_domain))).scalar() or 0
    total_analyzed = db.query(func.count(AnalysisLog.id)).scalar() or 0

    papers = db.query(ResearchPaper).all()

    kw_counter: Counter = Counter()
    method_counter: Counter = Counter()
    year_counter: Counter = Counter()
    domain_counter: Counter = Counter()
    length_buckets: Dict[str, int] = {"< 60 words": 0, "60–79 words": 0, "80–99 words": 0, "100+ words": 0}

    for p in papers:
        domain_counter[p.research_domain] += 1
        year_counter[p.publication_year] += 1
        method_counter[p.methodology] += 1
        for kw in (p.keywords or "").split(","):
            clean_kw = kw.strip().lower()
            if clean_kw:
                kw_counter[clean_kw] += 1

        wc = len((p.abstract or "").split())
        if wc < 60:
            length_buckets["< 60 words"] += 1
        elif wc < 80:
            length_buckets["60–79 words"] += 1
        elif wc < 100:
            length_buckets["80–99 words"] += 1
        else:
            length_buckets["100+ words"] += 1

    recent_papers = (
        db.query(ResearchPaper)
        .order_by(ResearchPaper.publication_year.desc(), ResearchPaper.paper_id.desc())
        .limit(6)
        .all()
    )

    return {
        "total_papers": total_papers,
        "total_domains": total_domains,
        "total_analyzed_papers": total_analyzed,
        "total_unique_keywords": len(kw_counter),
        "popular_domains": [{"domain": d, "count": c} for d, c in domain_counter.most_common()],
        "year_distribution": [{"year": y, "count": c} for y, c in sorted(year_counter.items())],
        "top_keywords": [{"keyword": k, "count": c} for k, c in kw_counter.most_common(12)],
        "top_methods": [{"methodology": m, "count": c} for m, c in method_counter.most_common(10)],
        "paper_length_distribution": [{"bucket": b, "count": c} for b, c in length_buckets.items()],
        "recent_papers": [
            {
                "paper_id": p.paper_id,
                "title": p.title,
                "authors": p.authors,
                "research_domain": p.research_domain,
                "publication_year": p.publication_year,
                "methodology": p.methodology,
            }
            for p in recent_papers
        ],
    }


@router.get("/domains")
def insights_domains(db: Session = Depends(get_db)):
    rows = (
        db.query(ResearchPaper.research_domain, func.count(ResearchPaper.id))
        .group_by(ResearchPaper.research_domain)
        .order_by(func.count(ResearchPaper.id).desc())
        .all()
    )
    return {"domains": [{"domain": d, "count": c} for d, c in rows]}


@router.get("/keywords")
def insights_keywords(db: Session = Depends(get_db)):
    papers = db.query(ResearchPaper.keywords).all()
    kw_counter: Counter = Counter()
    for (kw_str,) in papers:
        for kw in (kw_str or "").split(","):
            clean = kw.strip().lower()
            if clean:
                kw_counter[clean] += 1
    return {
        "total_unique_keywords": len(kw_counter),
        "keywords": [{"keyword": k, "count": c} for k, c in kw_counter.most_common(25)],
    }
