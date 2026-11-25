"""Unit II.D: Information Extraction Service (Methods, Technologies, Algorithms, Domains)."""

from __future__ import annotations

import re
from typing import Any, Dict, List

METHOD_PATTERNS = [
    "federated learning", "reinforcement learning", "self-supervised learning",
    "contrastive learning", "transfer learning", "meta-learning", "active learning",
    "knowledge distillation", "adversarial training", "differential privacy",
    "zero-shot", "few-shot", "fine-tuning", "retrieval-augmented generation",
    "sentiment analysis", "abstractive summarization", "object detection",
    "semantic segmentation", "task offloading", "anomaly detection",
    "intrusion detection", "uplift modeling", "hyperparameter optimization",
]

TECHNOLOGY_PATTERNS = [
    "kubernetes", "mqtt", "coap", "docker", "ebpf", "arm cortex-m", "5g",
    "gpu", "siem", "sdn", "tee", "tls", "wordnet", "spacy", "nltk",
    "pytorch", "tensorflow", "fastapi", "sqlite", "edge computing", "cloud",
]

ALGORITHM_PATTERNS = [
    "transformer", "vision transformer", "bert", "gpt", "lstm", "bilstm-crf",
    "cnn", "convolutional neural network", "graph neural network", "graph attention network",
    "graphsage", "u-net", "yolov8", "resnet", "mobilenet", "xgboost",
    "decision trees", "random forest", "isolation forest", "variational autoencoder",
    "diffusion", "proximal policy optimization", "deep q-network", "kalman",
    "markov decision process", "hdbscan", "umap", "ctgan", "lesk", "porterstemmer",
    "tf-idf", "cosine similarity",
]

DOMAIN_PATTERNS = [
    "healthcare", "clinical", "biomedical", "autonomous driving", "robotics",
    "manufacturing", "agriculture", "smart grid", "cybersecurity", "finance",
    "credit risk", "fraud", "telecom", "genomics", "education", "legal",
    "natural language processing", "computer vision", "internet of things", "cloud computing",
    "data science", "artificial intelligence", "machine learning",
]


def _match_patterns(text_lower: str, patterns: List[str]) -> List[str]:
    found = []
    for p in patterns:
        if re.search(rf"\b{re.escape(p)}\b", text_lower):
            found.append(p)
    return found


def extract_information(text: str) -> Dict[str, Any]:
    """Extract research methods, technologies, algorithms, domains, and technical terms."""
    text_lower = text.lower()

    methods = _match_patterns(text_lower, METHOD_PATTERNS)
    technologies = _match_patterns(text_lower, TECHNOLOGY_PATTERNS)
    algorithms = _match_patterns(text_lower, ALGORITHM_PATTERNS)
    domains = _match_patterns(text_lower, DOMAIN_PATTERNS)

    # Extract capitalized multi-word technical phrases & acronyms
    acronyms = re.findall(r"\b[A-Z]{2,}(?:-[A-Z0-9]+)?\b", text)
    capitalized_phrases = re.findall(r"\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b", text)
    technical_terms = list(dict.fromkeys(acronyms + capitalized_phrases))[:15]

    return {
        "extraction_method": "Domain-Specific Pattern Rules + Technical Phrase NER",
        "research_methods": methods,
        "technologies": technologies,
        "algorithms": algorithms,
        "domains": domains,
        "technical_terms": technical_terms,
        "explanation": (
            "Information extraction identifies structured entities (methods, algorithms, technologies, and application domains) "
            "from unstructured academic prose using lexical and pattern-based NER rules."
        ),
    }
