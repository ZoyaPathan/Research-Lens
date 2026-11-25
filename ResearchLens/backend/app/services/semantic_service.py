"""Unit III: Modular Educational Semantic Analysis Service.

Note: Implemented as a modular semantic-analysis module pending detailed Unit III syllabus confirmation.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.keyword_extraction import extract_information
from app.services.wordnet_service import analyze_wordnet


def compute_sentence_similarity(sentence1: str, sentence2: str, method: str = "auto") -> Dict[str, Any]:
    """Compare two sentences using TF-IDF cosine similarity + concept overlap."""
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        mat = vectorizer.fit_transform([sentence1, sentence2])
        cos_sim = float(cosine_similarity(mat[0:1], mat[1:2])[0][0])
    except ValueError:
        cos_sim = 0.0

    t1 = {w for w in re.findall(r"[a-z0-9]+", sentence1.lower()) if len(w) > 2}
    t2 = {w for w in re.findall(r"[a-z0-9]+", sentence2.lower()) if len(w) > 2}
    overlap = sorted(t1.intersection(t2))
    jaccard = len(overlap) / max(len(t1.union(t2)), 1)

    score = round(min(0.75 * cos_sim + 0.25 * jaccard, 1.0), 4)
    pct = round(score * 100, 1)

    return {
        "sentence1": sentence1,
        "sentence2": sentence2,
        "method_used": "TF-IDF Cosine Similarity + Lexical Concept Overlap",
        "similarity_score": score,
        "similarity_percentage": pct,
        "matching_concepts": overlap,
        "explanation": (
            "Measures semantic closeness by projecting both sentences into a shared TF-IDF vector space "
            "and computing the cosine of the angle between them, supplemented by shared content-word overlap. "
            "Modular design allows plugging in dense transformer embeddings when available."
        ),
    }


def analyze_semantics(text: str, target_word: Optional[str] = None) -> Dict[str, Any]:
    """Identify main topic, technical concepts, methods, applications, and contextual word meaning."""
    extracted = extract_information(text)

    # Identify main topic from top TF-IDF / frequent content terms
    words = [w for w in re.findall(r"[a-z]+", text.lower()) if len(w) > 3]
    stop = {"this", "that", "with", "from", "using", "across", "while", "paper", "propose", "results", "demonstrate", "these", "their"}
    content = [w for w in words if w not in stop]
    freq: Dict[str, int] = {}
    for w in content:
        freq[w] = freq.get(w, 0) + 1
    top_concepts = [k for k, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]]

    main_topic = (
        extracted["domains"][0].title()
        if extracted["domains"]
        else (top_concepts[0].title() if top_concepts else "General Academic Research")
    )

    chosen_word = target_word.strip() if target_word and target_word.strip() else (top_concepts[0] if top_concepts else "model")
    wn_data = analyze_wordnet(chosen_word, sentence=text)

    return {
        "module_note": "Modular Unit III educational semantic-analysis module.",
        "concept_identification": {
            "main_research_topic": main_topic,
            "technical_concepts": extracted["technical_terms"] or top_concepts[:6],
            "methods": extracted["research_methods"] + extracted["algorithms"],
            "applications": extracted["domains"],
        },
        "contextual_meaning": wn_data["word_sense_disambiguation"],
        "semantic_relationships": {
            "word": wn_data["word"],
            "wordnet_available": wn_data["wordnet_available"],
            **wn_data["lexical_semantics"],
        },
    }
