from __future__ import annotations

"""Dataset construction utilities for contradiction training."""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List
import json

from mbt_ai_tools.contradiction.engine import Claim, ContradictionEngine, ContradictionType


@dataclass
class ContradictionExample:
    id: str
    premise: str
    query: str
    label: ContradictionType

    def to_record(self) -> dict:
        return {"id": self.id, "premise": self.premise, "query": self.query, "label": self.label.value}


def build_examples(engine: ContradictionEngine | None = None) -> List[ContradictionExample]:
    engine = engine or ContradictionEngine()
    seeds = [
        ("water", "Water boils at 100C", "Water boils at 95C"),
        ("triangle", "Triangles have three sides", "Triangle false three sides"),
        ("mammal", "All mammals give live birth", "Platypus is an exception"),
        ("time", "Always in 1950", "In 2020 things changed"),
        ("negation", "Paris is not the capital of France", "Paris is the capital of France"),
    ]
    examples: List[ContradictionExample] = []
    for idx, (slug, premise, query) in enumerate(seeds, start=1):
        claim = Claim(id=f"ex_{idx}", premise=premise, query=query)
        detected = engine.detect(claim)
        label = detected.type if detected else ContradictionType.NONE
        examples.append(ContradictionExample(claim.id, premise, query, label))
    return examples


def export_jsonl(examples: Iterable[ContradictionExample], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex.to_record()) + "\n")


__all__ = ["ContradictionExample", "build_examples", "export_jsonl"]
