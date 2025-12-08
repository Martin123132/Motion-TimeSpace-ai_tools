from __future__ import annotations

"""Detects stability of self-model embeddings over time."""

from dataclasses import dataclass
from typing import List, Tuple
import numpy as np

from .self_model import SelfModel, SelfState


@dataclass
class InvarianceReport:
    stability_score: float
    drift_events: List[Tuple[int, float]]


class InvarianceDetector:
    def __init__(self, threshold: float = 0.3) -> None:
        self.threshold = threshold

    def analyze(self, model: SelfModel) -> InvarianceReport:
        if len(model.history) < 2:
            return InvarianceReport(stability_score=1.0, drift_events=[])

        drifts: List[Tuple[int, float]] = []
        similarities: List[float] = []
        prev = model.history[0].embedding
        for idx, state in enumerate(model.history[1:], start=1):
            sim = self._cosine_similarity(prev, state.embedding)
            similarities.append(sim)
            if sim < 1 - self.threshold:
                drifts.append((idx, sim))
            prev = state.embedding

        stability = sum(similarities) / len(similarities)
        return InvarianceReport(stability_score=stability, drift_events=drifts)

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        denom = (np.linalg.norm(a) * np.linalg.norm(b)) or 1e-9
        return float(np.dot(a, b) / denom)


__all__ = ["InvarianceDetector", "InvarianceReport"]
