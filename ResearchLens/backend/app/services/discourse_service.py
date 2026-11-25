"""Unit IV: Discourse and Pragmatic Analysis Service (Educational Rule-Based Demonstrations).

Clearly labels heuristic predictions and limitations; does not claim human-level pragmatic understanding.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, List

REFERENCE_WORDS = {"this", "that", "these", "those", "it", "its", "they", "their", "them", "such", "former", "latter"}
CONJUNCTIONS = {"and", "but", "or", "yet", "so", "for", "nor", "because", "although", "while", "whereas", "since"}
DISCOURSE_MARKERS = {"however", "moreover", "furthermore", "therefore", "consequently", "additionally", "meanwhile", "in contrast", "nevertheless", "thus", "finally", "specifically", "importantly"}

PERSON_DEIXIS = {"i", "me", "my", "we", "us", "our", "you", "your"}
SPATIAL_DEIXIS = {"here", "there", "nearby", "above", "below"}
TEMPORAL_DEIXIS = {"today", "tomorrow", "yesterday", "now", "then", "recently", "currently", "soon"}
DEMONSTRATIVE_DEIXIS = {"this", "that", "these", "those"}

PRAGMATIC_MARKERS = {"well", "actually", "however", "so", "you know", "honestly", "basically", "anyway", "indeed"}


def _classify_sentence_structure(sentence: str, idx: int, total: int) -> str:
    sl = sentence.lower()
    if any(k in sl for k in ["however", "problem", "challenge", "struggle", "limitation", "gap", "lack", "difficult"]):
        return "Problem Statement (Heuristic)"
    if any(k in sl for k in ["propose", "method", "architecture", "framework", "design", "implement", "algorithm", "pipeline"]):
        return "Methodology (Heuristic)"
    if any(k in sl for k in ["result", "demonstrate", "evaluate", "experiment", "improve", "achieve", "accuracy", "score", "%"]):
        return "Findings / Results (Heuristic)"
    if idx == total - 1 or any(k in sl for k in ["conclude", "conclusion", "future", "summary", "maintaining", "overall"]):
        return "Conclusion (Heuristic)"
    return "Introduction / Background (Heuristic)"


def _classify_speech_act(sentence: str) -> Dict[str, str]:
    s = sentence.strip()
    sl = s.lower()
    if s.endswith("?"):
        if sl.startswith(("could you", "can you", "would you", "will you")):
            return {"act": "Directive (Indirect Request)", "directness": "Indirect", "reason": "Interrogative form functioning as a polite request."}
        return {"act": "Directive (Question)", "directness": "Direct", "reason": "Interrogative sentence requesting information."}
    if any(sl.startswith(p) for p in ["please ", "submit ", "run ", "check ", "open ", "explain ", "analyze "]):
        return {"act": "Directive", "directness": "Direct", "reason": "Imperative or requestive utterance."}
    if any(k in sl for k in ["will ", "promise ", "guarantee ", "commit ", "shall "]):
        return {"act": "Commissive", "directness": "Direct", "reason": "Commits the speaker/system to a future action."}
    if any(k in sl for k in ["thank", "congratulat", "sorry", "apologize", "appreciate", "glad", "unfortunately"]):
        return {"act": "Expressive", "directness": "Direct", "reason": "Expresses psychological state or attitude."}
    if any(k in sl for k in ["hereby", "declare", "pronounce", "certified", "approved"]):
        return {"act": "Declarative", "directness": "Direct", "reason": "Institutional or formal declaration."}
    return {"act": "Assertive", "directness": "Direct", "reason": "States a proposition, claim, or experimental fact."}


def analyze_discourse_text(text: str) -> Dict[str, Any]:
    """Run Unit IV discourse & pragmatic analyses on an academic or general text."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    if not sentences:
        sentences = [text.strip()]

    words_lower = re.findall(r"[a-z]+", text.lower())
    text_lower = text.lower()

    # A. Discourse Cohesion
    found_refs = sorted({w for w in words_lower if w in REFERENCE_WORDS})
    found_conj = sorted({w for w in words_lower if w in CONJUNCTIONS})
    found_markers = sorted({m for m in DISCOURSE_MARKERS if re.search(rf"\b{re.escape(m)}\b", text_lower)})
    content_words = [w for w in words_lower if len(w) > 4 and w not in REFERENCE_WORDS and w not in CONJUNCTIONS]
    repeated_terms = [
        {"term": term, "count": cnt}
        for term, cnt in Counter(content_words).most_common(8)
        if cnt >= 2
    ]

    # B. Discourse Structure
    structure = [
        {
            "index": i + 1,
            "sentence": sent,
            "predicted_role": _classify_sentence_structure(sent, i, len(sentences)),
        }
        for i, sent in enumerate(sentences)
    ]

    # F. Deixis
    deixis = {
        "person": sorted({w for w in words_lower if w in PERSON_DEIXIS}),
        "spatial": sorted({w for w in words_lower if w in SPATIAL_DEIXIS}),
        "temporal": sorted({w for w in words_lower if w in TEMPORAL_DEIXIS}),
        "demonstrative": sorted({w for w in words_lower if w in DEMONSTRATIVE_DEIXIS}),
        "explanation": "Deictic expressions depend on speaker, time, and spatial context for interpretation.",
    }

    # G. Endophora and Exophora
    anaphora_hits = [s for s in sentences if any(re.search(rf"\b{r}\b", s.lower()) for r in ["this", "these", "it", "they", "their"])]
    endophora_exophora = {
        "detected_anaphoric_sentences": anaphora_hits[:4],
        "examples": [
            {"type": "Anaphora (Endophora)", "example": "We propose a Transformer model. It achieves 94% accuracy.", "note": "'It' refers backward to 'a Transformer model'."},
            {"type": "Cataphora (Endophora)", "example": "Although it is compact, the quantized model retains high precision.", "note": "'It' refers forward to 'the quantized model'."},
            {"type": "Exophora", "example": "Please look at that chart over there.", "note": "'that' and 'there' point outside the text to the physical/UI context."},
        ],
    }

    # H. Speech Acts
    speech_acts = [
        {"sentence": s, **_classify_speech_act(s)}
        for s in sentences[:8]
    ]

    # I. Pragmatic Markers & Face
    found_pragmatic = [m for m in PRAGMATIC_MARKERS if re.search(rf"\b{re.escape(m)}\b", text_lower)]

    return {
        "disclaimer": "These analyses use transparent rule-based heuristics for educational demonstration, not human-level pragmatic reasoning.",
        "cohesion": {
            "reference_words": found_refs,
            "conjunctions": found_conj,
            "discourse_markers": found_markers,
            "repeated_key_terms": repeated_terms,
        },
        "discourse_structure": structure,
        "deixis": deixis,
        "endophora_exophora": endophora_exophora,
        "speech_acts": speech_acts,
        "pragmatic_markers": {
            "detected": found_pragmatic,
            "face_theory_examples": {
                "positive_face": "Example: 'Your methodology is really innovative — could we also test it on a second dataset?' (Affirms researcher's competence/belonging.)",
                "negative_face": "Example: 'I hate to bother you, but could you possibly share the baseline script when you have a moment?' (Respects autonomy and avoids imposition.)",
            },
        },
    }


def analyze_conversation_pragmatics(conversation: str) -> Dict[str, Any]:
    """Analyze conversational turns for Adjacency Pairs, Implicature, and Grice's Maxims."""
    lines = [ln.strip() for ln in conversation.splitlines() if ln.strip()]
    turns = []
    for ln in lines:
        if ":" in ln:
            speaker, utterance = ln.split(":", 1)
            turns.append({"speaker": speaker.strip(), "utterance": utterance.strip()})
        else:
            turns.append({"speaker": f"Turn {len(turns) + 1}", "utterance": ln})

    # C. Adjacency Pairs
    pairs = []
    greetings = ("hi", "hello", "hey", "good morning", "good evening")
    for i in range(len(turns) - 1):
        u1 = turns[i]["utterance"]
        u2 = turns[i + 1]["utterance"]
        u1l, u2l = u1.lower(), u2.lower()

        if any(u1l.startswith(g) for g in greetings) and any(u2l.startswith(g) for g in greetings):
            pair_type = "Greeting -> Greeting"
        elif u1.endswith("?"):
            pair_type = "Question -> Answer"
        elif any(k in u1l for k in ["can you", "could you", "please", "would you"]):
            pair_type = "Request -> Response"
        elif any(k in u1l for k in ["would you like", "want me to", "shall i", "offer"]):
            pair_type = "Offer -> Acceptance / Rejection"
        else:
            pair_type = "Statement -> Follow-up"

        pairs.append({
            "first_turn": f"{turns[i]['speaker']}: {u1}",
            "second_turn": f"{turns[i + 1]['speaker']}: {u2}",
            "pair_type": pair_type,
        })

    # D. Implicature (heuristic educational detection)
    implicatures = []
    for i in range(len(turns) - 1):
        u1 = turns[i]["utterance"]
        u2 = turns[i + 1]["utterance"]
        u2l = u2.lower()
        if u1.endswith("?") and not any(u2l.startswith(w) for w in ["yes", "no", "sure", "definitely"]):
            reason_hint = "indirect response"
            if any(k in u2l for k in ["exam", "tomorrow", "busy", "deadline", "sick", "meeting", "travel"]):
                reason_hint = "mentions a conflicting obligation or constraint"
            implicatures.append({
                "exchange": f"{turns[i]['speaker']}: \"{u1}\" -> {turns[i + 1]['speaker']}: \"{u2}\"",
                "possible_implied_meaning": (
                    f"Although {turns[i + 1]['speaker']} does not say 'no' directly, the response {reason_hint}, "
                    "which may imply inability, decline, or conditional availability."
                ),
                "caveat": "Educational heuristic interpretation only — not a guaranteed conclusion.",
            })

    # E. Cooperative Principle (Grice's 4 Maxims)
    total_words = sum(len(t["utterance"].split()) for t in turns)
    avg_len = total_words / max(len(turns), 1)
    maxims = [
        {
            "maxim": "Quantity",
            "principle": "Provide as much information as needed, and no more.",
            "heuristic_observation": (
                f"Average turn length is {avg_len:.1f} words."
                + (" Turns are concise." if avg_len <= 18 else " Some turns may be overly verbose.")
            ),
        },
        {
            "maxim": "Quality",
            "principle": "Be truthful; do not say what you believe is false or lack evidence for.",
            "heuristic_observation": "Check for hedging markers (e.g., 'maybe', 'probably') or unsupported absolute claims.",
        },
        {
            "maxim": "Relation",
            "principle": "Be relevant to the current conversational topic.",
            "heuristic_observation": (
                "Indirect answers (potential flouting of Relation) can trigger conversational implicature."
                if implicatures else "Turns appear topically aligned."
            ),
        },
        {
            "maxim": "Manner",
            "principle": "Be clear, brief, orderly, and avoid ambiguity.",
            "heuristic_observation": "Evaluates clarity and absence of obscure jargon.",
        },
    ]

    return {
        "disclaimer": "Rule-based pragmatic demonstration; conversational implicature depends on shared real-world context.",
        "turns": turns,
        "adjacency_pairs": pairs,
        "implicatures": implicatures,
        "cooperative_principle": maxims,
    }
