"""NLTK resource availability helper with graceful fallbacks."""

from __future__ import annotations

from functools import lru_cache
from typing import Dict
import nltk

REQUIRED_CORPORA = {
    "punkt": "tokenizers/punkt",
    "punkt_tab": "tokenizers/punkt_tab",
    "stopwords": "corpora/stopwords",
    "wordnet": "corpora/wordnet",
    "omw-1.4": "corpora/omw-1.4",
    "averaged_perceptron_tagger": "taggers/averaged_perceptron_tagger",
    "averaged_perceptron_tagger_eng": "taggers/averaged_perceptron_tagger_eng",
}


@lru_cache(maxsize=1)
def get_nltk_status() -> Dict[str, bool]:
    """Check which NLTK corpora/taggers are locally available."""
    status: Dict[str, bool] = {}
    for name, path in REQUIRED_CORPORA.items():
        try:
            nltk.data.find(path)
            status[name] = True
        except Exception:
            status[name] = False
    return status


def ensure_nltk_data() -> Dict[str, bool]:
    """Attempt to verify or download missing NLTK data silently."""
    status = get_nltk_status().copy()
    for name, available in status.items():
        if not available:
            try:
                nltk.download(name, quiet=True)
                nltk.data.find(REQUIRED_CORPORA[name])
                status[name] = True
            except Exception:
                status[name] = False
    get_nltk_status.cache_clear()
    return status


FALLBACK_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "by", "for", "from",
    "has", "have", "he", "in", "is", "it", "its", "of", "on", "or", "that",
    "the", "their", "them", "they", "this", "to", "was", "were", "will",
    "with", "we", "our", "these", "those", "such", "into", "using", "across",
    "while", "against", "between", "through", "more", "most", "can", "may",
}
