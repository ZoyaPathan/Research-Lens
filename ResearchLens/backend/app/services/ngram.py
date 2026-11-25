"""Unit II.C: N-gram Language Model Service."""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models import ResearchPaper


def analyze_ngram_language_model(
    db: Session,
    context: Optional[str] = None,
    custom_text: Optional[str] = None,
    n: int = 2,
) -> Dict[str, Any]:
    """Build unigram, bigram, and trigram counts from the corpus and compute next-word probabilities."""
    papers = db.query(ResearchPaper).all()
    corpus_texts = [f"{p.title} {p.abstract}" for p in papers]
    if custom_text:
        corpus_texts.append(custom_text)

    tokens: List[str] = []
    for doc in corpus_texts:
        tokens.extend(re.findall(r"[a-z]+", doc.lower()))

    vocab = set(tokens)
    vocab_size = max(len(vocab), 1)
    total_tokens = max(len(tokens), 1)

    unigram_counts = Counter(tokens)
    bigram_counts: Dict[str, Counter] = defaultdict(Counter)
    trigram_counts: Dict[str, Counter] = defaultdict(Counter)

    for i in range(len(tokens) - 1):
        bigram_counts[tokens[i]][tokens[i + 1]] += 1
    for i in range(len(tokens) - 2):
        ctx = f"{tokens[i]} {tokens[i + 1]}"
        trigram_counts[ctx][tokens[i + 2]] += 1

    # Top N-grams
    top_unigrams = [{"ngram": w, "count": c, "probability": round(c / total_tokens, 5)} for w, c in unigram_counts.most_common(10)]

    flat_bigrams = Counter()
    for w1, counter in bigram_counts.items():
        for w2, c in counter.items():
            flat_bigrams[f"{w1} {w2}"] = c
    top_bigrams = [{"ngram": ng, "count": c} for ng, c in flat_bigrams.most_common(10)]

    flat_trigrams = Counter()
    for ctx, counter in trigram_counts.items():
        for w3, c in counter.items():
            flat_trigrams[f"{ctx} {w3}"] = c
    top_trigrams = [{"ngram": ng, "count": c} for ng, c in flat_trigrams.most_common(10)]

    # Next-word prediction for context
    clean_ctx = re.findall(r"[a-z]+", (context or "deep learning").lower())
    predictions: List[Dict[str, Any]] = []
    model_used = "Bigram (Laplace Smoothed)"

    if n == 3 and len(clean_ctx) >= 2:
        ctx_key = f"{clean_ctx[-2]} {clean_ctx[-1]}"
        candidates = trigram_counts.get(ctx_key)
        if candidates:
            denom = sum(candidates.values()) + vocab_size
            model_used = f"Trigram P(w | '{ctx_key}') with Laplace smoothing"
            for w, cnt in candidates.most_common(8):
                prob = (cnt + 1) / denom
                predictions.append({
                    "next_word": w,
                    "count": cnt,
                    "smoothed_probability": round(prob, 6),
                    "log_probability": round(math.log(prob), 4),
                })

    if not predictions and len(clean_ctx) >= 1:
        w1 = clean_ctx[-1]
        candidates = bigram_counts.get(w1)
        model_used = f"Bigram P(w | '{w1}') with Laplace smoothing"
        if candidates:
            denom = unigram_counts[w1] + vocab_size
            for w, cnt in candidates.most_common(8):
                prob = (cnt + 1) / denom
                predictions.append({
                    "next_word": w,
                    "count": cnt,
                    "smoothed_probability": round(prob, 6),
                    "log_probability": round(math.log(prob), 4),
                })

    if not predictions:
        model_used = "Unigram Fallback P(w)"
        for w, cnt in unigram_counts.most_common(8):
            prob = cnt / total_tokens
            predictions.append({
                "next_word": w,
                "count": cnt,
                "smoothed_probability": round(prob, 6),
                "log_probability": round(math.log(prob), 4),
            })

    return {
        "corpus_tokens": total_tokens,
        "vocabulary_size": vocab_size,
        "context_used": " ".join(clean_ctx) if clean_ctx else "deep learning",
        "model_used": model_used,
        "predictions": predictions,
        "top_unigrams": top_unigrams,
        "top_bigrams": top_bigrams,
        "top_trigrams": top_trigrams,
        "explanation": (
            "An N-gram language model estimates the probability of the next word using the preceding N-1 words "
            "via the Markov assumption: P(w_t | w_{t-n+1}...w_{t-1}). Laplace (+1) smoothing prevents zero probabilities for unseen N-grams."
        ),
    }
