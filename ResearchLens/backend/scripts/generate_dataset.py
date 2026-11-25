"""Synthetic Academic Research Paper Dataset Generator for ResearchLens.

Generates 210 original, realistic synthetic academic research paper records
(30 per domain across 7 domains) and saves them to:
- backend/data/research_papers.csv
- backend/data/research_papers.json
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path
from typing import Dict, List

SEED = 42

FIRST_NAMES = [
    "Aarav", "Ananya", "Elena", "Marcus", "Priya", "Liam", "Sophia", "Kenji",
    "Fatima", "Lucas", "Meera", "Daniel", "Chloe", "Rohan", "Hannah", "Vikram",
    "Nadia", "Ethan", "Yuki", "Omar", "Clara", "Siddharth", "Isabel", "Noah",
    "Kavya", "Benjamin", "Zara", "Arjun", "Maya", "Sebastian", "Divya", "Leo",
]

LAST_NAMES = [
    "Sharma", "Patel", "Chen", "Rodriguez", "Kim", "Müller", "Okafor", "Nair",
    "Williams", "Tanaka", "Al-Mansoor", "Kowalski", "Reddy", "Lindqvist", "Das",
    "Bennett", "Ibrahim", "Vargas", "Sato", "Kapoor", "Fernandez", "Gupta",
    "Nakamura", "Hassan", "Johansson", "Verma", "Rossi", "Park", "Menon", "Silva",
]

DOMAIN_SPECS: Dict[str, Dict[str, List[str]]] = {
    "Artificial Intelligence and Machine Learning": {
        "topics": [
            "federated healthcare diagnostics",
            "explainable credit risk scoring",
            "reinforcement learning for robotic manipulation",
            "self-supervised representation learning in tabular data",
            "causal inference for personalized treatment planning",
            "meta-learning under severe class imbalance",
            "neuro-symbolic reasoning for automated theorem proving",
            "continual learning without catastrophic forgetting",
            "active learning for clinical triage systems",
            "bayesian neural networks for uncertainty quantification",
        ],
        "methods": [
            "Gradient-Boosted Decision Trees",
            "Federated Averaging with Differential Privacy",
            "Proximal Policy Optimization",
            "SHAP-Guided Explainable Ensemble",
            "Variational Autoencoder",
            "Graph Attention Network",
            "Contrastive Self-Supervised Learning",
            "Bayesian Deep Learning",
            "Meta-Agnostic Gradient Descent",
            "Neuro-Symbolic Rule Distillation",
        ],
        "contexts": [
            "multi-center clinical registries",
            "industrial automation testbeds",
            "high-dimensional financial benchmarks",
            "low-resource sensor streams",
            "autonomous navigation simulations",
            "real-world longitudinal patient cohorts",
        ],
        "metrics": [
            "macro F1-score by 6.4%",
            "AUROC by 4.8% while reducing calibration error",
            "sample efficiency by 31% across unseen tasks",
            "convergence stability by 22% under non-IID data",
            "interpretability fidelity without sacrificing predictive accuracy",
        ],
        "keywords_pool": [
            "machine learning", "explainable AI", "federated learning",
            "reinforcement learning", "uncertainty estimation", "deep learning",
            "representation learning", "causal inference", "model calibration",
            "continual learning", "SHAP", "neural networks",
        ],
    },
    "Natural Language Processing": {
        "topics": [
            "aspect-based sentiment analysis in multilingual reviews",
            "low-resource machine translation using cross-lingual adapters",
            "abstractive summarization of biomedical literature",
            "discourse-aware coreference resolution in legal contracts",
            "hallucination detection in retrieval-augmented generation",
            "named entity recognition for clinical discharge notes",
            "argumentation mining in peer-review corpora",
            "zero-shot intent classification for conversational agents",
            "pragmatic implicature detection in dialogue systems",
            "morphological disambiguation for agglutinative languages",
        ],
        "methods": [
            "LoRA-Tuned Transformer Encoder",
            "Retrieval-Augmented Generation with Reranking",
            "BiLSTM-CRF with Contextual Embeddings",
            "Cross-Lingual Adapter Fusion",
            "Contrastive Sentence Embedding",
            "Discourse Graph Neural Network",
            "Multi-Task Sequence-to-Sequence Learning",
            "WordNet-Guided Lesk Disambiguation",
            "Prompt-Tuned Language Model",
            "Hierarchical Attention Network",
        ],
        "contexts": [
            "domain-specific academic abstracts",
            "multilingual customer feedback datasets",
            "annotated clinical narrative corpora",
            "multi-turn task-oriented dialogues",
            "long-form regulatory documents",
            "cross-domain benchmark suites",
        ],
        "metrics": [
            "ROUGE-L by 5.2 points",
            "entity-level F1-score by 7.1%",
            "BLEU score by 3.9 points on low-resource pairs",
            "factual consistency by 18% on long documents",
            "semantic retrieval MRR@10 by 9.4%",
        ],
        "keywords_pool": [
            "natural language processing", "transformers", "sentiment analysis",
            "text summarization", "named entity recognition", "word sense disambiguation",
            "discourse analysis", "semantic similarity", "language models",
            "TF-IDF", "pos tagging", "retrieval augmented generation",
        ],
    },
    "Computer Vision": {
        "topics": [
            "real-time defect inspection on manufacturing lines",
            "3D point-cloud segmentation for autonomous driving",
            "retinal lesion detection in fundus photography",
            "low-light pedestrian tracking in urban surveillance",
            "vision-language grounding for industrial robotics",
            "few-shot plant disease classification from leaf imagery",
            "monocular depth estimation under adverse weather",
            "histopathology whole-slide image classification",
            "pose estimation for physical rehabilitation monitoring",
            "self-supervised pretraining for satellite land-cover mapping",
        ],
        "methods": [
            "Vision Transformer with Shifted Windows",
            "Deformable Convolutional Network",
            "YOLOv8-Style Multi-Scale Detector",
            "Masked Autoencoder Pretraining",
            "Siamese Metric Learning Network",
            "U-Net with Attention Gates",
            "Diffusion-Based Data Augmentation",
            "Cross-Modal Vision-Language Encoder",
            "PointNet++ Hierarchical Aggregation",
            "Knowledge-Distilled MobileNet",
        ],
        "contexts": [
            "high-resolution medical imaging cohorts",
            "embedded camera streams at 60 FPS",
            "multi-spectral remote sensing archives",
            "noisy industrial inspection datasets",
            "urban driving benchmarks",
            "resource-constrained mobile vision pipelines",
        ],
        "metrics": [
            "mean Average Precision (mAP@0.5) by 5.6%",
            "Dice similarity coefficient to 0.93",
            "inference latency by 38% on edge GPUs",
            "top-1 classification accuracy by 4.3% under domain shift",
            "boundary IoU by 6.1% on small objects",
        ],
        "keywords_pool": [
            "computer vision", "vision transformer", "object detection",
            "semantic segmentation", "medical imaging", "convolutional neural networks",
            "self-supervised learning", "knowledge distillation", "point clouds",
            "image classification", "feature extraction", "attention mechanism",
        ],
    },
    "Edge Computing and IoT": {
        "topics": [
            "energy-aware task offloading in smart-factory IoT networks",
            "tinyml anomaly detection on wearable health sensors",
            "adaptive MQTT broker scheduling for smart agriculture",
            "vehicular edge caching for connected autonomous mobility",
            "federated intrusion monitoring on microcontroller gateways",
            "thermal-aware workload placement in fog computing clusters",
            "compressed neural inference for acoustic predictive maintenance",
            "blockchain-free lightweight consensus for sensor swarms",
            "latency-bounded video analytics on roadside edge nodes",
            "digital twin synchronization for smart grid substations",
        ],
        "methods": [
            "8-Bit Quantized TinyML Classifier",
            "Deep Q-Network Offloading Scheduler",
            "Lyapunov Drift-Plus-Penalty Optimization",
            "Split-Inference Neural Partitioning",
            "Lightweight CoAP/MQTT Telemetry Pipeline",
            "Edge-Fog Hierarchical Clustering",
            "Structured Pruning with Knowledge Distillation",
            "Kalman-Filtered Sensor Fusion",
            "Game-Theoretic Resource Allocation",
            "Event-Driven Stream Processing",
        ],
        "contexts": [
            "ARM Cortex-M microcontroller testbeds",
            "heterogeneous 5G multi-access edge clusters",
            "battery-powered environmental sensor deployments",
            "real-time industrial telemetry pipelines",
            "simulated smart-city traffic corridors",
            "intermittent wide-area IoT backhauls",
        ],
        "metrics": [
            "end-to-end latency by 41%",
            "device battery longevity by 29%",
            "flash memory footprint by 68% with minimal accuracy loss",
            "packet delivery ratio to 99.2% under congestion",
            "task deadline satisfaction rate by 19%",
        ],
        "keywords_pool": [
            "edge computing", "internet of things", "tinyml", "task offloading",
            "fog computing", "model quantization", "sensor networks",
            "predictive maintenance", "low latency", "energy efficiency",
            "MQTT", "smart grid",
        ],
    },
    "Cybersecurity": {
        "topics": [
            "zero-day ransomware detection via system-call graphs",
            "adversarial robustness of network intrusion classifiers",
            "automated phishing URL detection using lexical transformers",
            "zero-trust micro-segmentation for hybrid enterprise networks",
            "side-channel leakage mitigation in cryptographic accelerators",
            "threat intelligence correlation across SIEM log streams",
            "privacy-preserving federated malware classification",
            "deepfake audio verification for voice authentication",
            "software supply-chain vulnerability prioritization",
            "DDoS traffic mitigation in software-defined networks",
        ],
        "methods": [
            "Temporal Graph Convolutional Network",
            "Adversarial Training with PGD Perturbations",
            "Character-Level Transformer Classifier",
            "Zero-Trust Policy Verification Engine",
            "Isolation Forest with Flow Entropy Features",
            "Differential Privacy Gradient Clipping",
            "Spectral Spoofing Detector",
            "MITRE ATT&CK Knowledge Graph Mapping",
            "SDN Flow-Rule Anomaly Detector",
            "Static-Dynamic Hybrid Taint Analysis",
        ],
        "contexts": [
            "enterprise SOC telemetry logs",
            "encrypted TLS traffic metadata",
            "containerized microservice clusters",
            "publicly available intrusion benchmarks",
            "sandboxed malware execution traces",
            "multi-tenant cloud perimeter gateways",
        ],
        "metrics": [
            "false-positive alert rate by 44%",
            "zero-day recall to 96.4%",
            "adversarial accuracy by 21% under evasion attacks",
            "mean time to detect (MTTD) by 53%",
            "throughput overhead to under 2.5%",
        ],
        "keywords_pool": [
            "cybersecurity", "intrusion detection", "zero trust", "malware analysis",
            "adversarial machine learning", "network security", "threat intelligence",
            "ransomware", "anomaly detection", "differential privacy",
            "phishing detection", "software defined networking",
        ],
    },
    "Data Science": {
        "topics": [
            "automated feature engineering for retail demand forecasting",
            "concept drift adaptation in real-time fraud analytics",
            "missing-value imputation in longitudinal electronic health records",
            "graph-based customer churn prediction in telecom networks",
            "synthetic tabular data generation with privacy guarantees",
            "spatial-temporal crime hotspot forecasting for urban planning",
            "multi-objective hyperparameter tuning for imbalanced datasets",
            "causal uplift modeling for targeted marketing campaigns",
            "outlier-robust clustering of high-dimensional genomics profiles",
            "automated data-quality profiling for enterprise data lakes",
        ],
        "methods": [
            "Temporal Fusion Transformer",
            "ADWIN Drift-Adaptive Ensemble",
            "Denoising Diffusion Tabular Imputer",
            "Bipartite GraphSAGE Embedding",
            "CTGAN with Wasserstein Loss",
            "Spatio-Temporal Kriging with XGBoost",
            "Bayesian Hyperparameter Optimization",
            "Doubly Robust Uplift Estimator",
            "UMAP-HDBSCAN Density Clustering",
            "Schema-Aware Statistical Profiling",
        ],
        "contexts": [
            "multi-year transactional data warehouses",
            "streaming payment authorization pipelines",
            "clinical trial cohorts with 30% missingness",
            "large-scale mobility and census datasets",
            "high-dimensional omics repositories",
            "enterprise lakehouse ingestion workflows",
        ],
        "metrics": [
            "RMSE by 14.2% across seasonal horizons",
            "post-drift F1-score recovery speed by 3x",
            "imputation Wasserstein distance by 27%",
            "Qini uplift coefficient by 11.8%",
            "data pipeline validation coverage to 98.5%",
        ],
        "keywords_pool": [
            "data science", "time series forecasting", "concept drift",
            "feature engineering", "fraud detection", "causal inference",
            "synthetic data", "clustering", "data quality", "missing data",
            "gradient boosting", "predictive analytics",
        ],
    },
    "Cloud Computing": {
        "topics": [
            "cold-start mitigation in serverless function-as-a-service",
            "carbon-aware workload scheduling across geo-distributed clouds",
            "autoscaling microservice DAGs using predictive queueing",
            "confidential computing isolation for multi-tenant AI inference",
            "cost-optimal spot-instance orchestration for batch ML training",
            "declarative Kubernetes placement for stateful distributed databases",
            "observability trace compression in high-throughput service meshes",
            "disaster-recovery replication optimization across object stores",
            "GPU-sharing virtualization for multi-tenant inference clusters",
            "SLA-aware container consolidation in green data centers",
        ],
        "methods": [
            "Pre-Warmed Snapshot Container Pool",
            "Carbon-Intensity-Aware MILP Scheduler",
            "LSTM Queue-Length Autoscaler",
            "Hardware TEE Enclave Attestation",
            "Spot-Interruption Markov Decision Process",
            "Custom Kubernetes Operator with eBPF Telemetry",
            "Sketch-Based Distributed Trace Sampling",
            "Erasure-Coded Geo-Replication",
            "MPS-Guided Fractional GPU Multiplexer",
            "Multi-Objective Bin-Packing Heuristic",
        ],
        "contexts": [
            "production Kubernetes clusters",
            "multi-region public cloud testbeds",
            "serverless event-driven benchmarks",
            "distributed GPU training workloads",
            "high-fanout microservice architectures",
            "geo-replicated storage systems",
        ],
        "metrics": [
            "p99 tail latency by 36%",
            "operational carbon footprint by 24%",
            "cloud compute expenditure by 33%",
            "GPU utilization from 41% to 78%",
            "cold-start initialization time by 64%",
        ],
        "keywords_pool": [
            "cloud computing", "serverless", "kubernetes", "autoscaling",
            "microservices", "green computing", "container orchestration",
            "confidential computing", "distributed systems", "GPU virtualization",
            "observability", "spot instances",
        ],
    },
}

TITLE_PATTERNS = [
    "{method} for {topic_title}",
    "Towards Reliable {topic_title} Using {method}",
    "A {method} Framework for {topic_title}",
    "Enhancing {topic_title} via {method}",
    "Scalable {topic_title}: A {method} Approach",
    "Evaluating {method} in {topic_title}",
]


def _title_case(phrase: str) -> str:
    minor = {"for", "in", "on", "of", "the", "a", "an", "and", "via", "with", "to", "under", "from"}
    words = phrase.split()
    out = []
    for i, w in enumerate(words):
        if w.upper() in {"AI", "NLP", "IOT", "3D", "MQTT", "SDN", "SIEM", "URL", "DAGS", "DAG", "GPU", "SLA", "DDOS"}:
            out.append(w.upper() if w.upper() != "IOT" else "IoT")
        elif i == 0 or w.lower() not in minor:
            out.append(w[0].upper() + w[1:] if w else w)
        else:
            out.append(w.lower())
    return " ".join(out)


def _generate_authors(rng: random.Random) -> str:
    count = rng.randint(2, 4)
    chosen = set()
    names = []
    while len(names) < count:
        full = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
        if full not in chosen:
            chosen.add(full)
            names.append(full)
    return ", ".join(names)


def generate_dataset() -> List[dict]:
    rng = random.Random(SEED)
    records: List[dict] = []
    used_titles = set()
    paper_idx = 1

    for domain, spec in DOMAIN_SPECS.items():
        topics = spec["topics"]
        methods = spec["methods"]
        contexts = spec["contexts"]
        metrics = spec["metrics"]
        kw_pool = spec["keywords_pool"]

        # Create 30 distinct combinations per domain (210 total)
        combos = [(t, m) for t in topics for m in methods]
        rng.shuffle(combos)

        count_for_domain = 0
        for topic, method in combos:
            if count_for_domain >= 30:
                break
            pattern = TITLE_PATTERNS[(paper_idx + count_for_domain) % len(TITLE_PATTERNS)]
            title = pattern.format(method=method, topic_title=_title_case(topic))
            if title in used_titles:
                continue
            used_titles.add(title)

            context = contexts[(paper_idx + count_for_domain) % len(contexts)]
            metric = metrics[(paper_idx * 3 + count_for_domain) % len(metrics)]
            year = rng.randint(2020, 2026)
            authors = _generate_authors(rng)

            # Pick 5-6 domain keywords + method-relevant terms
            selected_kws = rng.sample(kw_pool, k=5)
            method_kw = method.lower()
            if method_kw not in selected_kws:
                selected_kws.append(method_kw)
            keywords_str = ", ".join(selected_kws)

            abstract = (
                f"Research in {domain.lower()} increasingly demands robust solutions for {topic}. "
                f"However, existing approaches often struggle with scalability, domain shift, and reproducibility when deployed on {context}. "
                f"In this paper, we propose a {method} architecture specifically designed to address these limitations through structured representation learning and adaptive optimization. "
                f"We evaluate our methodology across {context} and compare it against established baseline models. "
                f"Experimental results demonstrate that the proposed framework improves {metric}, while maintaining practical computational overhead for real-world deployment."
            )

            records.append(
                {
                    "paper_id": f"RL-{year}-{paper_idx:03d}",
                    "title": title,
                    "abstract": abstract,
                    "authors": authors,
                    "research_domain": domain,
                    "keywords": keywords_str,
                    "methodology": method,
                    "publication_year": year,
                }
            )
            paper_idx += 1
            count_for_domain += 1

    return records


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    records = generate_dataset()

    json_path = data_dir / "research_papers.json"
    csv_path = data_dir / "research_papers.csv"

    with json_path.open("w", encoding="utf-8") as jf:
        json.dump(records, jf, indent=2, ensure_ascii=False)

    fieldnames = [
        "paper_id",
        "title",
        "abstract",
        "authors",
        "research_domain",
        "keywords",
        "methodology",
        "publication_year",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} synthetic papers.")
    print(f"JSON: {json_path}")
    print(f"CSV:  {csv_path}")


if __name__ == "__main__":
    main()
