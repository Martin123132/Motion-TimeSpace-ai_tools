from __future__ import annotations

"""Training harness for running batches through the recursive AGI loop."""

from pathlib import Path
from typing import Iterable, List
import json

from mbt_ai_tools.contradiction.engine import Claim
from .loop import RecursiveAGILoop


class LoopTrainer:
    def __init__(self, loop: RecursiveAGILoop | None = None) -> None:
        self.loop = loop or RecursiveAGILoop()

    def train(self, claims: Iterable[Claim]) -> List[dict]:
        results = self.loop.run_batch(claims)
        return results

    def export(self, path: str | Path) -> None:
        data = {
            "system_state": self.loop.get_system_state(),
            "learning_events": self.loop.learning_events,
        }
        Path(path).write_text(json.dumps(data, indent=2))


__all__ = ["LoopTrainer"]
