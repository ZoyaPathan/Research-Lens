"""Unit II.E, F, G: Lexical Semantics, Word Sense Disambiguation (Lesk), and Word Similarity."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from nltk.corpus import wordnet as wn
from nltk.wsd import lesk

from app.services.nltk_setup import get_nltk_status

FALLBACK_LEXICON: Dict[str, Dict[str, Any]] = {
    "model": {
        "synonyms": ["framework", "architecture", "representation", "prototype"],
        "antonyms": [],
        "hypernyms": ["representation", "system"],
        "hyponyms": ["neural network", "language model", "classifier"],
        "senses": [
            {"id": "model.n.01", "definition": "A simplified mathematical or computational representation of a system or process."},
            {"id": "model.n.02", "definition": "A person who poses for artistic or fashion photography."},
        ],
    },
    "network": {
        "synonyms": ["graph", "mesh", "architecture", "system"],
        "antonyms": [],
        "hypernyms": ["system", "structure"],
        "hyponyms": ["neural network", "sensor network", "convolutional network"],
        "senses": [
            {"id": "network.n.01", "definition": "An interconnected system of computing nodes, sensors, or artificial neurons."},
            {"id": "network.n.02", "definition": "A group of broadcasting stations or social acquaintances."},
        ],
    },
    "learning": {
        "synonyms": ["training", "acquisition", "adaptation"],
        "antonyms": ["forgetting"],
        "hypernyms": ["cognitive_process", "optimization"],
        "hyponyms": ["supervised learning", "reinforcement learning", "federated learning"],
        "senses": [
            {"id": "learning.n.01", "definition": "The process of acquiring knowledge or optimizing model parameters from data."},
        ],
    },
    "bank": {
        "synonyms": ["financial_institution", "depository", "slope", "ridge"],
        "antonyms": [],
        "hypernyms": ["institution", "terrain"],
        "hyponyms": ["commercial bank", "riverbank"],
        "senses": [
            {"id": "bank.n.01", "definition": "A financial institution that accepts deposits and channels money into lending activities."},
            {"id": "bank.n.02", "definition": "Sloping land beside a body of water such as a river or stream."},
        ],
    },
}


def analyze_wordnet(
    word: str,
    sentence: Optional[str] = None,
    compare_word: Optional[str] = None,
) -> Dict[str, Any]:
    """Perform Lexical Semantics, WSD (Lesk), and Word Similarity using WordNet or fallback."""
    clean_word = re.sub(r"[^a-zA-Z_-]", "", word.strip().lower())
    status = get_nltk_status()
    wn_available = status.get("wordnet", False)

    synonyms: List[str] = []
    antonyms: List[str] = []
    hypernyms: List[str] = []
    hyponyms: List[str] = []
    senses: List[Dict[str, str]] = []

    if wn_available:
        try:
            synsets = wn.synsets(clean_word)
            syn_set = set()
            ant_set = set()
            hyp_set = set()
            hypon_set = set()

            for s in synsets[:6]:
                senses.append({
                    "synset": s.name(),
                    "pos": s.pos(),
                    "definition": s.definition(),
                    "examples": "; ".join(s.examples()[:2]) if s.examples() else "",
                })
                for lemma in s.lemmas():
                    name = lemma.name().replace("_", " ")
                    if name.lower() != clean_word:
                        syn_set.add(name)
                    for ant in lemma.antonyms():
                        ant_set.add(ant.name().replace("_", " "))
                for h in s.hypernyms():
                    hyp_set.add(h.name().split(".")[0].replace("_", " "))
                for h in s.hyponyms()[:4]:
                    hypon_set.add(h.name().split(".")[0].replace("_", " "))

            synonyms = sorted(syn_set)[:12]
            antonyms = sorted(ant_set)[:8]
            hypernyms = sorted(hyp_set)[:8]
            hyponyms = sorted(hypon_set)[:10]
        except Exception:
            wn_available = False

    if not wn_available:
        fb = FALLBACK_LEXICON.get(clean_word, {
            "synonyms": [],
            "antonyms": [],
            "hypernyms": [],
            "hyponyms": [],
            "senses": [{"synset": f"{clean_word}.n.01", "pos": "n", "definition": "WordNet corpus unavailable locally; install NLTK 'wordnet' for full lexical graph.", "examples": ""}],
        })
        synonyms = fb["synonyms"]
        antonyms = fb["antonyms"]
        hypernyms = fb["hypernyms"]
        hyponyms = fb["hyponyms"]
        senses = [
            {"synset": s.get("id", f"{clean_word}.n.01"), "pos": "n", "definition": s["definition"], "examples": ""}
            for s in fb["senses"]
        ]

    # Word Sense Disambiguation (Lesk)
    wsd_result: Optional[Dict[str, Any]] = None
    if sentence:
        sent_tokens = re.findall(r"[A-Za-z]+", sentence.lower())
        if wn_available:
            try:
                best_sense = lesk(sent_tokens, clean_word)
                if best_sense:
                    wsd_result = {
                        "target_word": clean_word,
                        "sentence": sentence,
                        "predicted_sense": best_sense.name(),
                        "definition": best_sense.definition(),
                        "method": "NLTK WordNet Lesk Algorithm",
                        "explanation": (
                            "The Lesk algorithm compares the overlap between words in the context sentence "
                            "and the dictionary glosses (definitions) of each candidate WordNet synset."
                        ),
                    }
                else:
                    wsd_result = {
                        "target_word": clean_word,
                        "sentence": sentence,
                        "predicted_sense": "No matching WordNet synset found",
                        "definition": "Try a common English noun, verb, or adjective.",
                        "method": "NLTK WordNet Lesk Algorithm",
                        "explanation": "WordNet did not contain a synset for this exact token.",
                    }
            except Exception:
                wn_available = False

        if not wsd_result:
            # Simple overlap fallback
            best_def = senses[0]["definition"] if senses else "No definition available."
            best_syn = senses[0]["synset"] if senses else f"{clean_word}.n.01"
            best_overlap = -1
            ctx_set = set(sent_tokens)
            for s in senses:
                gloss_set = set(re.findall(r"[a-z]+", s["definition"].lower()))
                overlap = len(ctx_set.intersection(gloss_set))
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_def = s["definition"]
                    best_syn = s["synset"]
            wsd_result = {
                "target_word": clean_word,
                "sentence": sentence,
                "predicted_sense": best_syn,
                "definition": best_def,
                "method": "Fallback Gloss-Overlap Lesk",
                "explanation": "WordNet corpus unavailable; used fallback dictionary gloss overlap.",
            }

    # Word Similarity
    similarity_result: Optional[Dict[str, Any]] = None
    if compare_word:
        clean_cmp = re.sub(r"[^a-zA-Z_-]", "", compare_word.strip().lower())
        if wn_available:
            try:
                s1 = wn.synsets(clean_word)
                s2 = wn.synsets(clean_cmp)
                if s1 and s2:
                    wup_sim = s1[0].wup_similarity(s2[0]) or 0.0
                    path_sim = s1[0].path_similarity(s2[0]) or 0.0
                    interp = (
                        "High semantic relatedness" if wup_sim >= 0.7
                        else "Moderate semantic relatedness" if wup_sim >= 0.4
                        else "Low semantic relatedness"
                    )
                    similarity_result = {
                        "word1": clean_word,
                        "word2": clean_cmp,
                        "wup_similarity": round(float(wup_sim), 4),
                        "path_similarity": round(float(path_sim), 4),
                        "interpretation": f"{interp} (Wu-Palmer similarity = {wup_sim:.2f}, Path similarity = {path_sim:.2f}).",
                    }
                else:
                    similarity_result = {
                        "word1": clean_word,
                        "word2": clean_cmp,
                        "wup_similarity": 0.0,
                        "path_similarity": 0.0,
                        "interpretation": "One or both words were not found in WordNet synsets.",
                    }
            except Exception:
                pass
        if not similarity_result:
            # Character-bigram Jaccard fallback
            b1 = {clean_word[i:i + 2] for i in range(max(len(clean_word) - 1, 1))}
            b2 = {clean_cmp[i:i + 2] for i in range(max(len(clean_cmp) - 1, 1))}
            jacc = len(b1 & b2) / max(len(b1 | b2), 1)
            similarity_result = {
                "word1": clean_word,
                "word2": clean_cmp,
                "wup_similarity": round(jacc, 4),
                "path_similarity": round(jacc, 4),
                "interpretation": "Fallback lexical similarity (WordNet unavailable).",
            }

    return {
        "word": clean_word,
        "wordnet_available": wn_available,
        "lexical_semantics": {
            "synonyms": synonyms,
            "antonyms": antonyms,
            "hypernyms": hypernyms,
            "hyponyms": hyponyms,
            "senses": senses,
        },
        "word_sense_disambiguation": wsd_result,
        "word_similarity": similarity_result,
    }
