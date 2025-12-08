from __future__ import annotations

"""Neural observer that mirrors and compresses symbolic updates."""

from dataclasses import dataclass
from typing import Dict, List
import time

from mbt_ai_tools.contradiction.engine import Contradiction


@dataclass
class Observation:
    contradiction_type: str
    repair_pattern: str
    human_reasoning: str
    success: bool
    closure_impact: float


@dataclass
class LearnedPattern:
    patterns: Dict[str, str]
    confidence: float
    learned_at: float


class NeuralObserver:
    def __init__(self) -> None:
        self.observation_history: List[Observation] = []
        self.learned_patterns: List[LearnedPattern] = []
        self.symbolic_fluency: float = 0.0

    def observe_repair(self, contradiction: Contradiction, human_insight: str, repair_action: str) -> Observation:
        observation = Observation(
            contradiction_type=contradiction.type.value,
            repair_pattern=repair_action,
            human_reasoning=human_insight,
            success=True,
            closure_impact=contradiction.score,
        )
        self.observation_history.append(observation)
        return observation

    def learn_pattern(self) -> LearnedPattern | None:
        if len(self.observation_history) < 2:
            return None
        recent = self.observation_history[-5:]
        pattern_types: Dict[str, List[str]] = {}
        for obs in recent:
            pattern_types.setdefault(obs.contradiction_type, []).append(obs.repair_pattern)

        common_patterns = {
            ctype: max(set(repairs), key=repairs.count) for ctype, repairs in pattern_types.items() if repairs
        }
        pattern = LearnedPattern(
            patterns=common_patterns,
            confidence=min(len(recent) / 5.0, 1.0),
            learned_at=time.time(),
        )
        self.learned_patterns.append(pattern)
        return pattern

    def evolve_fluency(self) -> Dict[str, float | int]:
        fluency_gain = len(self.learned_patterns) * 0.1
        self.symbolic_fluency = min(self.symbolic_fluency + fluency_gain, 100.0)
        return {
            "symbolic_fluency": self.symbolic_fluency,
            "pattern_count": len(self.learned_patterns),
            "observation_count": len(self.observation_history),
        }


__all__ = ["NeuralObserver", "Observation", "LearnedPattern"]
