from __future__ import annotations

"""Curriculum generation for staged contradiction training."""

from dataclasses import dataclass
from typing import Dict, List

from .dataset_builder import ContradictionExample


@dataclass
class CurriculumStage:
    name: str
    examples: List[ContradictionExample]


class CurriculumGenerator:
    def __init__(self, stages: Dict[str, List[str]] | None = None) -> None:
        # map contradiction types to stage names
        self.stages = stages or {
            "intro": ["direct_negation", "definitional_violation"],
            "intermediate": ["property_mismatch"],
            "advanced": ["universal_counterexample", "temporal_conflict"],
        }

    def build(self, examples: List[ContradictionExample]) -> List[CurriculumStage]:
        buckets: Dict[str, List[ContradictionExample]] = {stage: [] for stage in self.stages}
        for ex in examples:
            for stage, labels in self.stages.items():
                if ex.label.value in labels:
                    buckets[stage].append(ex)
                    break
            else:
                buckets.setdefault("overflow", []).append(ex)

        return [CurriculumStage(name=stage, examples=data) for stage, data in buckets.items()]


__all__ = ["CurriculumGenerator", "CurriculumStage"]
