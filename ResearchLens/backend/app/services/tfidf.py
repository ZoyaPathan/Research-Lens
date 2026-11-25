"""Unit II.B & Smart Search: TF-IDF Scoring and Document Retrieval Service."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app.models import ResearchPaper


def compute_tfidf_for_text(db: Session, target_text: str, top_k: int = 10) -> Dict[str, Any]:
    """Compute TF-IDF scores for a target text against the ResearchLens corpus."""
    papers = db.query(ResearchPaper).all()
    corpus_docs = [f"{p.title}. {p.abstract} {p.keywords}" for p in papers]
    docs = [target_text] + corpus_docs

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=3000)
    matrix = vectorizer.fit_transform(docs)
    feature_names = vectorizer.get_feature_names_out()

    target_vec = matrix[0].toarray().flatten()
    nonzero_indices = np.where(target_vec > 0)[0]
    sorted_indices = nonzero_indices[np.argsort(target_vec[nonzero_indices])[::-1]]

    terms = [
        {
            "term": str(feature_names[idx]),
            "tfidf_score": round(float(target_vec[idx]), 4),
        }
        for idx in sorted_indices[:top_k]
    ]

    return {
        "corpus_size": len(papers),
        "vocabulary_size": len(feature_names),
        "top_terms": terms,
        "explanation": (
            "TF-IDF (Term Frequency-Inverse Document Frequency) weights words higher when they appear "
            "frequently in the target document but rarely across the rest of the research corpus."
        ),
    }


def search_papers_tfidf(
    db: Session,
    query: str,
    mode: str = "hybrid",
    top_k: int = 15,
) -> Dict[str, Any]:
    """Search research papers using keyword matching + TF-IDF cosine similarity."""
    papers = db.query(ResearchPaper).all()
    if not papers:
        return {
            "query": query,
            "retrieval_method": "TF-IDF + Cosine Similarity",
            "total_results": 0,
            "results": [],
        }

    docs = [f"{p.title}. {p.abstract} {p.keywords} {p.methodology} {p.research_domain}" for p in papers]

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=5000)
    doc_matrix = vectorizer.fit_transform(docs)
    query_vec = vectorizer.transform([query])

    cos_scores = cosine_similarity(query_vec, doc_matrix).flatten()

    query_tokens = {t for t in re.findall(r"[a-z0-9]+", query.lower()) if len(t) > 2}

    results: List[Dict[str, Any]] = []
    for idx, paper in enumerate(papers):
        tfidf_sim = float(cos_scores[idx])
        paper_text_lower = f"{paper.title} {paper.abstract} {paper.keywords} {paper.research_domain}".lower()
        paper_tokens = set(re.findall(r"[a-z0-9]+", paper_text_lower))
        matched_tokens = sorted(query_tokens.intersection(paper_tokens))

        kw_list = [k.strip() for k in paper.keywords.split(",") if k.strip()]
        matching_keywords = [
            kw for kw in kw_list
            if any(qt in kw.lower() for qt in query_tokens)
        ]

        kw_overlap_score = len(matched_tokens) / max(len(query_tokens), 1)
        if mode == "keyword":
            combined = kw_overlap_score
        else:
            combined = 0.72 * tfidf_sim + 0.28 * kw_overlap_score

        if combined > 0.01 or matched_tokens:
            results.append({
                "paper_id": paper.paper_id,
                "title": paper.title,
                "abstract_preview": paper.abstract[:240] + ("..." if len(paper.abstract) > 240 else ""),
                "authors": paper.authors,
                "research_domain": paper.research_domain,
                "publication_year": paper.publication_year,
                "methodology": paper.methodology,
                "relevance_score": round(min(combined, 1.0), 4),
                "tfidf_cosine_score": round(tfidf_sim, 4),
                "keyword_match_score": round(kw_overlap_score, 4),
                "matching_keywords": matching_keywords if matching_keywords else matched_tokens[:6],
            })

    results.sort(key=lambda r: r["relevance_score"], reverse=True)
    top_results = results[:top_k]

    method_label = (
        "Keyword Overlap Matching"
        if mode == "keyword"
        else "TF-IDF Vectorization + Cosine Similarity (with Keyword Boost)"
    )

    return {
        "query": query,
        "retrieval_method": method_label,
        "semantic_note": (
            "Using Scikit-learn TF-IDF + Cosine Similarity for fast, deterministic local retrieval. "
            "Transformer sentence embeddings are optional and not required."
        ),
        "total_results": len(top_results),
        "results": top_results,
    }
