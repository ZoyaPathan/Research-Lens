"""Unit V: Summarization Evaluation Service (ROUGE-1, ROUGE-2, ROUGE-L)."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, List

try:
    from rouge_score import rouge_scorer
    _ROUGE_PKG_AVAILABLE = True
except Exception:
    _ROUGE_PKG_AVAILABLE = False


def _lcs_length(a: List[str], b: List[str]) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def _f1_from_counts(overlap: int, pred_len: int, ref_len: int) -> Dict[str, float]:
    prec = overlap / pred_len if pred_len > 0 else 0.0
    rec = overlap / ref_len if ref_len > 0 else 0.0
    f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
    return {"precision": round(prec, 4), "recall": round(rec, 4), "fmeasure": round(f1, 4)}


def evaluate_rouge(generated_summary: str, reference_summary: str) -> Dict[str, Any]:
    """Compute real ROUGE-1, ROUGE-2, and ROUGE-L scores without fabricating values."""
    if _ROUGE_PKG_AVAILABLE:
        scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
        scores = scorer.score(reference_summary, generated_summary)
        return {
            "engine": "rouge-score",
            "rouge1": {
                "precision": round(scores["rouge1"].precision, 4),
                "recall": round(scores["rouge1"].recall, 4),
                "fmeasure": round(scores["rouge1"].fmeasure, 4),
            },
            "rouge2": {
                "precision": round(scores["rouge2"].precision, 4),
                "recall": round(scores["rouge2"].recall, 4),
                "fmeasure": round(scores["rouge2"].fmeasure, 4),
            },
            "rougeL": {
                "precision": round(scores["rougeL"].precision, 4),
                "recall": round(scores["rougeL"].recall, 4),
                "fmeasure": round(scores["rougeL"].fmeasure, 4),
            },
            "explanation": (
                "ROUGE-1 measures unigram overlap, ROUGE-2 measures bigram overlap (fluency/phrasing), "
                "and ROUGE-L measures Longest Common Subsequence overlap between the generated summary and reference summary."
            ),
        }

    gen_toks = re.findall(r"[a-z0-9]+", generated_summary.lower())
    ref_toks = re.findall(r"[a-z0-9]+", reference_summary.lower())

    gen_1 = Counter(gen_toks)
    ref_1 = Counter(ref_toks)
    overlap_1 = sum((gen_1 & ref_1).values())

    gen_2 = Counter(zip(gen_toks, gen_toks[1:]))
    ref_2 = Counter(zip(ref_toks, ref_toks[1:]))
    overlap_2 = sum((gen_2 & ref_2).values())

    lcs = _lcs_length(gen_toks, ref_toks)

    return {
        "engine": "Pure-Python ROUGE",
        "rouge1": _f1_from_counts(overlap_1, len(gen_toks), len(ref_toks)),
        "rouge2": _f1_from_counts(overlap_2, max(len(gen_toks) - 1, 0), max(len(ref_toks) - 1, 0)),
        "rougeL": _f1_from_counts(lcs, len(gen_toks), len(ref_toks)),
        "explanation": (
            "ROUGE-1 measures unigram overlap, ROUGE-2 measures bigram overlap, "
            "and ROUGE-L measures Longest Common Subsequence overlap."
        ),
    }
