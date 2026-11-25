"""Unit V: AI Summarizer Service with Lazy Hugging Face Pipeline & Extractive Fallback."""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

HF_MODEL_NAME = os.getenv("HF_SUMMARIZER_MODEL", "sshleifer/distilbart-cnn-12-6")
ENABLE_HF_MODELS = os.getenv("ENABLE_HF_MODELS", "true").lower() == "true"

_pipeline_instance = None
_model_status = "not_loaded"
_last_error: str | None = None

PROMPT_TEMPLATES: Dict[str, str] = {
    "beginner": "Summarize this research abstract in simple, accessible language for a beginner student:",
    "researcher": "Provide a concise technical summary preserving methodology and empirical results for a researcher:",
    "bullets": "Summarize the key points of this paper in five concise bullet points:",
    "methodology": "Explain the core research methodology and experimental approach described in this text:",
    "findings": "Extract the main findings, metrics, and conclusions from this research abstract:",
}


def get_summarizer_status() -> Dict[str, Any]:
    """Return current lazy-loading status of the Hugging Face summarization pipeline."""
    return {
        "model_name": HF_MODEL_NAME,
        "enable_hf_models": ENABLE_HF_MODELS,
        "status": _model_status,
        "last_error": _last_error,
        "fallback_available": True,
    }


def _extractive_summarize(text: str, length: str = "short", instruction: str = "researcher") -> str:
    """Deterministic TF-IDF sentence-scoring extractive summarization fallback."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if len(s.strip()) > 10]
    if not sentences:
        return text.strip()

    target_count = 2 if length == "short" else min(4, len(sentences))
    if instruction == "bullets":
        target_count = min(5, len(sentences))

    if len(sentences) <= target_count:
        chosen = sentences
    else:
        try:
            vec = TfidfVectorizer(stop_words="english")
            mat = vec.fit_transform(sentences)
            scores = np.asarray(mat.sum(axis=1)).ravel()
        except ValueError:
            scores = np.array([len(s.split()) for s in sentences], dtype=float)

        # Boost sentences matching the instruction focus
        for i, s in enumerate(sentences):
            sl = s.lower()
            if instruction == "methodology" and any(k in sl for k in ["propose", "method", "architecture", "framework", "approach", "using"]):
                scores[i] *= 1.6
            elif instruction == "findings" and any(k in sl for k in ["result", "demonstrate", "improve", "achieve", "%", "outperform"]):
                scores[i] *= 1.6

        top_indices = sorted(np.argsort(scores)[::-1][:target_count].tolist())
        chosen = [sentences[i] for i in top_indices]

    if instruction == "bullets":
        return "\n".join(f"- {s}" for s in chosen)
    if instruction == "beginner":
        return "In simple terms: " + " ".join(chosen)
    return " ".join(chosen)


def _try_load_hf_pipeline():
    global _pipeline_instance, _model_status, _last_error
    if _pipeline_instance is not None:
        return _pipeline_instance
    if not ENABLE_HF_MODELS:
        _model_status = "disabled"
        return None
    try:
        _model_status = "loading"
        from transformers import pipeline
        _pipeline_instance = pipeline("summarization", model=HF_MODEL_NAME)
        _model_status = "ready"
        _last_error = None
        return _pipeline_instance
    except Exception as exc:
        _model_status = "unavailable"
        _last_error = str(exc)
        return None


def summarize_text(
    text: str,
    length: str = "short",
    instruction: str = "researcher",
    use_hf: bool = True,
) -> Dict[str, Any]:
    """Summarize text using lazy HF pipeline if available, else reliable extractive fallback."""
    prompt_used = PROMPT_TEMPLATES.get(instruction, PROMPT_TEMPLATES["researcher"])
    method_used = "TF-IDF Extractive Summarizer (Reliable Local Fallback)"
    hf_attempted = False

    summary = ""
    if use_hf and ENABLE_HF_MODELS:
        hf_attempted = True
        pipe = _try_load_hf_pipeline()
        if pipe is not None:
            try:
                max_len = 75 if length == "short" else 140
                min_len = 25 if length == "short" else 55
                out = pipe(text, max_length=max_len, min_length=min_len, do_sample=False)
                if out and isinstance(out, list) and "summary_text" in out[0]:
                    summary = out[0]["summary_text"].strip()
                    method_used = f"Hugging Face Pipeline ({HF_MODEL_NAME})"
            except Exception as exc:
                global _last_error
                _last_error = str(exc)

    if not summary:
        summary = _extractive_summarize(text, length=length, instruction=instruction)

    return {
        "summary": summary,
        "length": length,
        "instruction_key": instruction,
        "prompt_template_used": prompt_used,
        "prompt_note": (
            "Prompt templates act as instructions to the local summarization workflow "
            "(not an external commercial LLM API call)."
        ),
        "method_used": method_used,
        "hf_attempted": hf_attempted,
        "model_status": get_summarizer_status(),
    }
