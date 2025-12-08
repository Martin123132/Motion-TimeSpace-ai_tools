from __future__ import annotations

"""Helpers to export contradiction data into OpenAI fine-tuning format."""

from typing import Iterable
import json

from .dataset_builder import ContradictionExample


def to_openai_messages(example: ContradictionExample) -> dict:
    return {
        "messages": [
            {"role": "system", "content": "Classify contradiction type"},
            {"role": "user", "content": f"Premise: {example.premise}\nQuery: {example.query}"},
            {"role": "assistant", "content": example.label.value},
        ]
    }


def export_openai_jsonl(examples: Iterable[ContradictionExample], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(to_openai_messages(ex)) + "\n")


__all__ = ["to_openai_messages", "export_openai_jsonl"]
