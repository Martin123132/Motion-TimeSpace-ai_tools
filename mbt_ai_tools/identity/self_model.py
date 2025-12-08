from __future__ import annotations

"""Self-model tracking basic identity signals."""

from dataclasses import dataclass, field
from typing import Dict, List
import numpy as np


@dataclass
class SelfState:
    timestamp: float
    embedding: np.ndarray
    tags: Dict[str, float] = field(default_factory=dict)


class SelfModel:
    def __init__(self, dim: int = 16) -> None:
        self.dim = dim
        self.history: List[SelfState] = []
        self.current = SelfState(timestamp=0.0, embedding=np.zeros(dim), tags={})

    def observe(self, embedding: np.ndarray, timestamp: float, **tags: float) -> SelfState:
        if embedding.shape != (self.dim,):
            raise ValueError(f"Expected embedding shape ({self.dim},) got {embedding.shape}")
        self.current = SelfState(timestamp=timestamp, embedding=embedding, tags=tags)
        self.history.append(self.current)
        return self.current

    def mean_embedding(self) -> np.ndarray:
        if not self.history:
            return np.zeros(self.dim)
        stacked = np.stack([state.embedding for state in self.history])
        return stacked.mean(axis=0)


__all__ = ["SelfModel", "SelfState"]
