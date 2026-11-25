"""SQLAlchemy ORM models for ResearchLens."""

from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class ResearchPaper(Base):
    """Academic research paper record stored in SQLite."""

    __tablename__ = "research_papers"

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(String(32), unique=True, index=True, nullable=False)
    title = Column(String(512), nullable=False, index=True)
    abstract = Column(Text, nullable=False)
    authors = Column(String(512), nullable=False)
    research_domain = Column(String(128), nullable=False, index=True)
    keywords = Column(Text, nullable=False)
    methodology = Column(String(256), nullable=False)
    publication_year = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class AnalysisLog(Base):
    """Tracks papers and texts analyzed through ResearchLens NLP modules."""

    __tablename__ = "analysis_logs"

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(String(32), nullable=True, index=True)
    module_name = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
