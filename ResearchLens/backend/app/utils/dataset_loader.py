"""Dataset loading and automatic SQLite seeding utilities."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import List, Dict, Any

from sqlalchemy.orm import Session

from app.models import ResearchPaper

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
JSON_PATH = DATA_DIR / "research_papers.json"
CSV_PATH = DATA_DIR / "research_papers.csv"


def load_records_from_disk() -> List[Dict[str, Any]]:
    """Load synthetic papers from JSON (preferred) or CSV."""
    if JSON_PATH.exists():
        with JSON_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    if CSV_PATH.exists():
        with CSV_PATH.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = []
            for row in reader:
                row["publication_year"] = int(row["publication_year"])
                rows.append(row)
            return rows
    return []


def seed_papers_if_empty(db: Session, force: bool = False) -> int:
    """Populate the research_papers table if empty (or when force=True)."""
    existing_count = db.query(ResearchPaper).count()
    if existing_count > 0 and not force:
        return existing_count

    records = load_records_from_disk()
    if not records:
        return existing_count

    if force and existing_count > 0:
        db.query(ResearchPaper).delete()
        db.commit()

    existing_ids = {r[0] for r in db.query(ResearchPaper.paper_id).all()}
    added = 0
    for rec in records:
        if rec["paper_id"] in existing_ids:
            continue
        paper = ResearchPaper(
            paper_id=rec["paper_id"],
            title=rec["title"],
            abstract=rec["abstract"],
            authors=rec["authors"],
            research_domain=rec["research_domain"],
            keywords=rec["keywords"],
            methodology=rec["methodology"],
            publication_year=int(rec["publication_year"]),
        )
        db.add(paper)
        added += 1

    db.commit()
    return db.query(ResearchPaper).count()
