from __future__ import annotations

"""Symbolic core inspired by the original MBT loop scripts."""

from dataclasses import dataclass
from typing import Dict, List
import time

from mbt_ai_tools.contradiction.engine import (
    Claim,
    Contradiction,
    ContradictionEngine,
)


@dataclass
class LogicPattern:
    pattern: str
    repair: str
    human_insight: str
    learned_at: float


class MBTSymbolicCore:
    """Tracks contradictions and learns structural repair patterns."""

    def __init__(self, engine: ContradictionEngine | None = None) -> None:
        self.engine = engine or ContradictionEngine()
        self.logic_map: Dict[str, List[LogicPattern]] = {}
        self.contradiction_history: List[Contradiction] = []
        self.evolution_count = 0

    def detect_contradiction(self, claim: Claim) -> Contradiction | None:
        contradiction = self.engine.detect(claim)
        if contradiction:
            self.contradiction_history.append(contradiction)
        return contradiction

    def learn_from_patch(self, contradiction: Contradiction, human_insight: str, repair_action: str) -> bool:
        domain_key = contradiction.type.value
        patterns = self.logic_map.setdefault(domain_key, [])
        patterns.append(
            LogicPattern(
                pattern=contradiction.note,
                repair=repair_action,
                human_insight=human_insight,
                learned_at=time.time(),
            )
        )
        return True

    def evolve(self) -> Dict[str, object]:
        self.evolution_count += 1
        refined_patterns = {
            domain: {
                "pattern_count": len(patterns),
                "common_repairs": list({p.repair for p in patterns}),
                "last_updated": max((p.learned_at for p in patterns), default=None),
            }
            for domain, patterns in self.logic_map.items()
        }
        return {
            "evolution_count": self.evolution_count,
            "refined_patterns": refined_patterns,
            "total_contradictions": len(self.contradiction_history),
        }


__all__ = ["MBTSymbolicCore", "LogicPattern"]
