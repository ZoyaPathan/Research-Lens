"""Unit II.A: Part-of-Speech (POS) Tagging Service."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, List

import nltk

from app.services.nltk_setup import get_nltk_status

try:
    import spacy
    _SPACY_AVAILABLE = True
except Exception:
    spacy = None
    _SPACY_AVAILABLE = False

POS_EXPLANATIONS: Dict[str, tuple[str, str]] = {
    "NN": ("Noun", "Singular or mass noun"),
    "NNS": ("Noun", "Plural noun"),
    "NNP": ("Noun", "Proper noun, singular"),
    "NNPS": ("Noun", "Proper noun, plural"),
    "NOUN": ("Noun", "Person, place, thing, or concept"),
    "PROPN": ("Noun", "Proper noun"),
    "VB": ("Verb", "Verb, base form"),
    "VBD": ("Verb", "Verb, past tense"),
    "VBG": ("Verb", "Verb, gerund or present participle"),
    "VBN": ("Verb", "Verb, past participle"),
    "VBP": ("Verb", "Verb, non-3rd person singular present"),
    "VBZ": ("Verb", "Verb, 3rd person singular present"),
    "VERB": ("Verb", "Action or state predicate"),
    "AUX": ("Verb", "Auxiliary verb"),
    "JJ": ("Adjective", "Adjective"),
    "JJR": ("Adjective", "Adjective, comparative"),
    "JJS": ("Adjective", "Adjective, superlative"),
    "ADJ": ("Adjective", "Modifies a noun"),
    "RB": ("Adverb", "Adverb"),
    "RBR": ("Adverb", "Adverb, comparative"),
    "RBS": ("Adverb", "Adverb, superlative"),
    "ADV": ("Adverb", "Modifies a verb, adjective, or adverb"),
    "PRP": ("Pronoun", "Personal pronoun"),
    "PRP$": ("Pronoun", "Possessive pronoun"),
    "WP": ("Pronoun", "Wh-pronoun"),
    "PRON": ("Pronoun", "Replaces a noun phrase"),
    "IN": ("Preposition", "Preposition or subordinating conjunction"),
    "ADP": ("Preposition", "Adposition / Preposition"),
    "DT": ("Determiner", "Determiner (e.g., the, a, this)"),
    "DET": ("Determiner", "Determiner"),
    "CC": ("Conjunction", "Coordinating conjunction"),
    "CCONJ": ("Conjunction", "Coordinating conjunction"),
    "SCONJ": ("Conjunction", "Subordinating conjunction"),
    "CD": ("Number", "Cardinal number"),
    "NUM": ("Number", "Numeric expression"),
    "TO": ("Particle", "Infinitive marker 'to'"),
    "MD": ("Modal", "Modal auxiliary (can, may, will)"),
}

FALLBACK_DETERMINERS = {"the", "a", "an", "this", "that", "these", "those", "each", "every", "some", "many"}
FALLBACK_PREPOSITIONS = {"in", "on", "at", "for", "from", "by", "with", "across", "under", "through", "into", "of", "to", "against"}
FALLBACK_PRONOUNS = {"we", "they", "it", "their", "our", "its", "them", "he", "she", "i", "you"}
FALLBACK_CONJUNCTIONS = {"and", "or", "but", "while", "however", "whereas", "although"}


def _fallback_pos_tag(tokens: List[str]) -> List[tuple[str, str]]:
    tagged = []
    for tok in tokens:
        lw = tok.lower()
        if not re.match(r"^[A-Za-z0-9-]+$", tok):
            tagged.append((tok, "PUNCT"))
        elif lw in FALLBACK_DETERMINERS:
            tagged.append((tok, "DT"))
        elif lw in FALLBACK_PREPOSITIONS:
            tagged.append((tok, "IN"))
        elif lw in FALLBACK_PRONOUNS:
            tagged.append((tok, "PRP"))
        elif lw in FALLBACK_CONJUNCTIONS:
            tagged.append((tok, "CC"))
        elif re.match(r"^\d+(\.\d+)?%?$", tok):
            tagged.append((tok, "CD"))
        elif lw.endswith(("ing", "ed", "ize", "ise", "ate")):
            tagged.append((tok, "VB"))
        elif lw.endswith(("ly",)):
            tagged.append((tok, "RB"))
        elif lw.endswith(("ive", "ous", "al", "ic", "able", "ible", "ful", "less")):
            tagged.append((tok, "JJ"))
        else:
            tagged.append((tok, "NN"))
    return tagged


def pos_tag_text(text: str) -> Dict[str, Any]:
    """Perform POS tagging using NLTK (or spaCy/rule fallback) and summarize categories."""
    status = get_nltk_status()
    engine_used = "Rule-based POS Tagger Fallback"
    tagged_pairs: List[tuple[str, str]] = []

    tokens = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*|[^\w\s]", text)

    if status.get("averaged_perceptron_tagger_eng") or status.get("averaged_perceptron_tagger"):
        try:
            if status.get("punkt_tab") or status.get("punkt"):
                tokens = nltk.word_tokenize(text)
            tagged_pairs = nltk.pos_tag(tokens)
            engine_used = "NLTK Averaged Perceptron Tagger"
        except Exception:
            tagged_pairs = _fallback_pos_tag(tokens)
    else:
        tagged_pairs = _fallback_pos_tag(tokens)

    items = []
    category_counts: Counter = Counter()

    for word, tag in tagged_pairs:
        if tag in {"PUNCT", ".", ",", ":", ";", "(", ")", "``", "''"} or not re.search(r"[A-Za-z0-9]", word):
            continue
        category, desc = POS_EXPLANATIONS.get(tag, ("Other", f"Penn Treebank tag '{tag}'"))
        category_counts[category] += 1
        items.append({
            "word": word,
            "pos_tag": tag,
            "category": category,
            "explanation": desc,
        })

    return {
        "engine_used": engine_used,
        "total_tagged_tokens": len(items),
        "category_distribution": [
            {"category": cat, "count": cnt}
            for cat, cnt in category_counts.most_common()
        ],
        "tokens": items[:120],
    }
