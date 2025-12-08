from __future__ import annotations

"""Export helper for Claude-style JSONL training."""

from typing import Iterable
import json

from .dataset_builder import ContradictionExample


def to_anthropic_format(example: ContradictionExample) -> dict:
    prompt = f"Premise: {example.premise}\nQuery: {example.query}\nLabel the contradiction type:"
    return {"prompt": prompt, "completion": example.label.value}


def export_anthropic_jsonl(examples: Iterable[ContradictionExample], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(to_anthropic_format(ex)) + "\n")


__all__ = ["to_anthropic_format", "export_anthropic_jsonl"]
