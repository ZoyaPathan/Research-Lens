"""Pydantic schemas for request validation and API responses."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PaperOut(BaseModel):
    paper_id: str
    title: str
    abstract: str
    authors: str
    research_domain: str
    keywords: str
    keywords_list: List[str] = []
    methodology: str
    publication_year: int

    class Config:
        from_attributes = True


class PaginatedPapersOut(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[PaperOut]


class TextRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=15000, description="Input abstract or text to analyze")
    paper_id: Optional[str] = Field(None, description="Optional paper_id if analyzing an existing paper")


class TfidfRequest(BaseModel):
    text: Optional[str] = Field(None, description="Optional custom text to score against the corpus")
    paper_id: Optional[str] = Field(None, description="Optional paper_id to analyze")
    top_k: int = Field(10, ge=3, le=30)


class NgramRequest(BaseModel):
    text: Optional[str] = Field(None, description="Optional seed/context text for N-gram probability")
    context: Optional[str] = Field(None, description="Preceding 1-2 words to predict next word")
    n: int = Field(2, ge=1, le=3)


class WordNetRequest(BaseModel):
    word: str = Field(..., min_length=1, max_length=64)
    sentence: Optional[str] = Field(None, description="Sentence context for Word Sense Disambiguation")
    compare_word: Optional[str] = Field(None, description="Second word for WordNet similarity")


class SemanticSimilarityRequest(BaseModel):
    sentence1: str = Field(..., min_length=3, max_length=5000)
    sentence2: str = Field(..., min_length=3, max_length=5000)
    method: str = Field("auto", description="auto | transformer | tfidf")


class SemanticAnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=15000)
    target_word: Optional[str] = Field(None, description="Optional word to inspect contextual meaning")
    paper_id: Optional[str] = None


class DiscourseAnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=15000)
    paper_id: Optional[str] = None


class ConversationRequest(BaseModel):
    conversation: str = Field(..., min_length=5, max_length=10000)


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=20, max_length=15000)
    paper_id: Optional[str] = None
    length: str = Field("short", description="short | detailed")
    instruction: str = Field("researcher", description="beginner | researcher | bullets | methodology | findings")
    use_hf: bool = Field(True, description="Attempt Hugging Face pipeline before falling back")


class EvaluateSummaryRequest(BaseModel):
    generated_summary: str = Field(..., min_length=5, max_length=10000)
    reference_summary: str = Field(..., min_length=5, max_length=10000)
