"""Unit I: Introduction and Word Analysis NLP Service.

Implements:
- Tokenization
- Text Normalization
- Stop-word Removal
- Stemming (PorterStemmer)
- Lemmatization (WordNetLemmatizer with graceful fallback)
- Bag of Words (Scikit-learn CountVectorizer)
- N-gram Analysis (unigrams, bigrams, trigrams)
- Regular Expressions
- Morphological Analysis (inflectional vs derivational)
- Finite Automata and Finite State Transducers (educational demo)
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, List

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

from app.services.nltk_setup import FALLBACK_STOPWORDS, get_nltk_status


def _safe_word_tokenize(text: str) -> List[str]:
    status = get_nltk_status()
    if status.get("punkt_tab") or status.get("punkt"):
        try:
            return nltk.word_tokenize(text)
        except Exception:
            pass
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*|[^\w\s]", text)


def _safe_stopwords() -> set:
    status = get_nltk_status()
    if status.get("stopwords"):
        try:
            return set(stopwords.words("english"))
        except Exception:
            pass
    return FALLBACK_STOPWORDS


def _rule_based_lemmatize(word: str) -> str:
    """Fallback lemmatizer when WordNet corpus is unavailable."""
    w = word.lower()
    if len(w) <= 3:
        return w
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("ing") and len(w) > 5:
        stem = w[:-3]
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            return stem[:-1]
        return stem
    if w.endswith("ed") and len(w) > 4:
        return w[:-2]
    if w.endswith("es") and len(w) > 4:
        return w[:-2]
    if w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def _fsa_accepts_ing(word: str) -> Dict[str, Any]:
    """Educational Finite-State Automaton (FSA) recognizing words ending in 'ing'."""
    state = "q0"
    transitions = []
    for ch in word.lower():
        if state == "q0":
            state = "q1" if ch == "i" else "q0"
        elif state == "q1":
            if ch == "n":
                state = "q2"
            elif ch == "i":
                state = "q1"
            else:
                state = "q0"
        elif state == "q2":
            if ch == "g":
                state = "q3_accept"
            elif ch == "i":
                state = "q1"
            else:
                state = "q0"
        elif state == "q3_accept":
            state = "q1" if ch == "i" else "q0"
        transitions.append({"char": ch, "state": state})

    return {
        "word": word,
        "accepted": state == "q3_accept",
        "final_state": state,
        "transitions": transitions,
    }


def _fst_to_base_form(word: str) -> Dict[str, str]:
    """Educational Finite-State Transducer (FST) mapping inflected words to base forms."""
    w = word.lower()
    if w.endswith("ies") and len(w) > 4:
        return {"input": word, "base_form": w[:-3] + "y", "rule": "FST: -ies -> -y (plural/3sg verb)"}
    if w.endswith("ing") and len(w) > 5:
        stem = w[:-3]
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            stem = stem[:-1]
        return {"input": word, "base_form": stem, "rule": "FST: -ing -> base (progressive participle)"}
    if w.endswith("ed") and len(w) > 4:
        return {"input": word, "base_form": w[:-2], "rule": "FST: -ed -> base (past tense)"}
    if w.endswith("s") and len(w) > 3 and not w.endswith("ss"):
        return {"input": word, "base_form": w[:-1], "rule": "FST: -s -> base (plural noun/3sg)"}
    return {"input": word, "base_form": w, "rule": "FST: identity (already base/unmatched)"}


def _morphological_analysis(words: List[str]) -> Dict[str, Any]:
    """Analyze inflectional and derivational morphology on sample tokens."""
    inflectional_suffixes = ("s", "es", "ed", "ing", "er", "est")
    derivational_suffixes = ("tion", "sion", "ment", "ness", "ity", "able", "ible", "al", "ic", "ize", "ise", "ly")

    analyzed = []
    seen = set()
    for w in words:
        lw = w.lower()
        if lw in seen or len(lw) < 4:
            continue
        seen.add(lw)

        morph_type = "Root / Uninflected"
        affix = "-"
        note = "Base lexical form without common English affixes."

        for suf in derivational_suffixes:
            if lw.endswith(suf) and len(lw) > len(suf) + 2:
                morph_type = "Derivational"
                affix = f"-{suf}"
                note = f"Derivational suffix '-{suf}' typically changes grammatical category or core meaning."
                break
        else:
            for suf in inflectional_suffixes:
                if lw.endswith(suf) and len(lw) > len(suf) + 2:
                    morph_type = "Inflectional"
                    affix = f"-{suf}"
                    note = f"Inflectional suffix '-{suf}' marks tense, number, or degree without changing word class."
                    break

        analyzed.append({
            "word": w,
            "morphology_type": morph_type,
            "detected_affix": affix,
            "explanation": note,
        })
        if len(analyzed) >= 15:
            break

    return {
        "explanation": (
            "Inflectional morphology modifies a word to express grammatical features (tense, plural, comparative) "
            "without changing its part of speech (e.g., model -> models, train -> training). "
            "Derivational morphology creates a new word or changes its part of speech (e.g., compute -> computation, predict -> predictive)."
        ),
        "examples": [
            {"word": "models", "base": "model", "type": "Inflectional", "affix": "-s (plural)"},
            {"word": "evaluating", "base": "evaluate", "type": "Inflectional", "affix": "-ing (progressive)"},
            {"word": "classification", "base": "classify", "type": "Derivational", "affix": "-ication (V -> N)"},
            {"word": "predictive", "base": "predict", "type": "Derivational", "affix": "-ive (V -> Adj)"},
        ],
        "tokens_analyzed": analyzed,
    }


def analyze_text_unit1(text: str) -> Dict[str, Any]:
    """Run all Unit I NLP analyses on the input text."""
    # A. Tokenization
    raw_tokens = _safe_word_tokenize(text)

    # B. Text Normalization
    lowercased = text.lower()
    whitespace_cleaned = re.sub(r"\s+", " ", lowercased).strip()
    no_punct = re.sub(r"[^\w\s]", " ", whitespace_cleaned)
    normalized_text = re.sub(r"\s+", " ", no_punct).strip()
    alpha_tokens = [t for t in re.findall(r"[A-Za-z]+", normalized_text)]

    # C. Stop-word Removal
    stop_set = _safe_stopwords()
    removed_stopwords = [t for t in alpha_tokens if t in stop_set]
    remaining_tokens = [t for t in alpha_tokens if t not in stop_set]

    # D. Stemming (PorterStemmer)
    stemmer = PorterStemmer()
    unique_content_words = list(dict.fromkeys(remaining_tokens))[:25]
    stemming_rows = [
        {"original": w, "stemmed": stemmer.stem(w)}
        for w in unique_content_words
    ]

    # E. Lemmatization (WordNetLemmatizer with fallback)
    status = get_nltk_status()
    wordnet_available = status.get("wordnet", False)
    lemmatizer = WordNetLemmatizer()
    lemmatization_note = (
        "Using NLTK WordNetLemmatizer with WordNet lexical database."
        if wordnet_available
        else "WordNet corpus not found locally; using rule-based suffix lemmatization fallback."
    )
    lemmatization_rows = []
    for w in unique_content_words:
        if wordnet_available:
            try:
                lemma = lemmatizer.lemmatize(w)
            except Exception:
                lemma = _rule_based_lemmatize(w)
        else:
            lemma = _rule_based_lemmatize(w)
        lemmatization_rows.append({"original": w, "lemmatized": lemma})

    # F. Bag of Words (Scikit-learn CountVectorizer)
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    if not sentences:
        sentences = [text]
    vectorizer = CountVectorizer(stop_words="english", max_features=20)
    try:
        bow_matrix_sparse = vectorizer.fit_transform(sentences)
        vocabulary = vectorizer.get_feature_names_out().tolist()
        bow_matrix = bow_matrix_sparse.toarray().tolist()
        total_counts = bow_matrix_sparse.sum(axis=0).A1.tolist()
        word_frequencies = sorted(
            [{"term": term, "count": int(cnt)} for term, cnt in zip(vocabulary, total_counts)],
            key=lambda x: x["count"],
            reverse=True,
        )
    except ValueError:
        vocabulary = []
        bow_matrix = []
        word_frequencies = []

    # G. N-gram Analysis
    ngram_tokens = remaining_tokens if remaining_tokens else alpha_tokens
    unigrams = Counter(ngram_tokens).most_common(10)
    bigrams = Counter(
        [" ".join(ngram_tokens[i:i + 2]) for i in range(len(ngram_tokens) - 1)]
    ).most_common(10)
    trigrams = Counter(
        [" ".join(ngram_tokens[i:i + 3]) for i in range(len(ngram_tokens) - 2)]
    ).most_common(10)

    # H. Regular Expressions
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    years = re.findall(r"\b(?:19|20)\d{2}\b", text)
    numbers = re.findall(r"\b\d+(?:\.\d+)?%?\b", text)
    tech_terms = list(dict.fromkeys(
        re.findall(r"\b(?:[A-Z]{2,}[A-Za-z0-9-]*|[A-Za-z]+-[A-Za-z]+)\b", text)
    ))

    # I. Morphological Analysis
    morphology = _morphological_analysis(alpha_tokens)

    # J. Finite Automata & Finite State Transducers
    ing_candidates = [w for w in dict.fromkeys(alpha_tokens) if w.endswith("ing")][:4]
    non_ing_candidates = [w for w in dict.fromkeys(alpha_tokens) if not w.endswith("ing") and len(w) > 3][:2]
    fsa_samples = [_fsa_accepts_ing(w) for w in (ing_candidates + non_ing_candidates or ["learning", "model"])]

    fst_candidates = list(dict.fromkeys(
        [w for w in alpha_tokens if w.endswith(("ing", "ed", "ies", "s")) and len(w) > 4]
    ))[:8]
    if not fst_candidates:
        fst_candidates = ["learning", "models", "evaluated", "studies"]
    fst_samples = [_fst_to_base_form(w) for w in fst_candidates]

    return {
        "tokenization": {
            "original_text": text,
            "tokens": raw_tokens,
            "total_token_count": len(raw_tokens),
            "explanation": "Tokenization splits raw text into discrete word and punctuation units for downstream NLP.",
        },
        "normalization": {
            "lowercased": lowercased,
            "whitespace_cleaned": whitespace_cleaned,
            "normalized_text": normalized_text,
            "explanation": "Text normalization standardizes casing, collapses extra whitespace, and removes punctuation noise.",
        },
        "stopword_removal": {
            "original_tokens": alpha_tokens,
            "removed_stopwords": removed_stopwords,
            "remaining_tokens": remaining_tokens,
            "explanation": "Stop-word removal filters high-frequency function words (e.g., 'the', 'is', 'in') to emphasize content terms.",
        },
        "stemming": {
            "method": "NLTK PorterStemmer",
            "rows": stemming_rows,
            "explanation": "Stemming strips suffixes heuristically to reduce words to a common root stem (not always a valid dictionary word).",
        },
        "lemmatization": {
            "method": "NLTK WordNetLemmatizer" if wordnet_available else "Rule-based Lemmatizer Fallback",
            "wordnet_available": wordnet_available,
            "note": lemmatization_note,
            "rows": lemmatization_rows,
            "explanation": "Lemmatization maps inflected words to their canonical dictionary base form (lemma).",
        },
        "bag_of_words": {
            "vocabulary": vocabulary,
            "word_frequencies": word_frequencies,
            "sentences": sentences,
            "matrix": bow_matrix,
            "explanation": "Bag-of-Words (CountVectorizer) represents each sentence as a vector of term occurrence counts over the vocabulary.",
        },
        "ngrams": {
            "unigrams": [{"ngram": k, "count": v} for k, v in unigrams],
            "bigrams": [{"ngram": k, "count": v} for k, v in bigrams],
            "trigrams": [{"ngram": k, "count": v} for k, v in trigrams],
            "explanation": "N-grams capture contiguous sequences of 1, 2, or 3 tokens to preserve local word order and collocations.",
        },
        "regex": {
            "emails": emails,
            "years": years,
            "numbers": numbers,
            "technical_patterns": tech_terms,
            "explanation": "Regular expressions match structured patterns such as emails, publication years, numeric metrics, and acronyms/hyphenated terms.",
        },
        "morphology": morphology,
        "finite_automata": {
            "note": "Educational demonstration only — not a comprehensive morphological transducer.",
            "fsa_ing_recognizer": fsa_samples,
            "fst_base_form": fst_samples,
            "explanation": "Finite-State Automata (FSA) accept/reject patterns (here: words ending in '-ing'), while Finite-State Transducers (FST) map inflected surface forms to base stems.",
        },
    }
