from __future__ import annotations

"""Utilities for evaluating contradiction detection performance."""

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

from .engine import Claim, Contradiction, ContradictionType, ContradictionEngine


@dataclass
class LabeledExample:
    claim: Claim
    expected: ContradictionType


@dataclass
class Prediction:
    claim_id: str
    predicted: ContradictionType
    detected: Contradiction | None


@dataclass
class EvaluationResult:
    precision: float
    recall: float
    f1: float
    support: int
    predictions: List[Prediction]


class ContradictionEvaluator:
    """Compute simple precision/recall metrics for an engine."""

    def __init__(self, engine: ContradictionEngine | None = None) -> None:
        self.engine = engine or ContradictionEngine()

    def evaluate(self, dataset: Sequence[LabeledExample]) -> EvaluationResult:
        predictions: List[Prediction] = []
        true_positive = false_positive = false_negative = 0

        for example in dataset:
            detected = self.engine.detect(example.claim)
            predicted = detected.type if detected else ContradictionType.NONE
            predictions.append(Prediction(example.claim.id, predicted, detected))

            if predicted != ContradictionType.NONE and example.expected != ContradictionType.NONE:
                true_positive += 1 if predicted == example.expected else 0
                false_positive += 1 if predicted != example.expected else 0
            elif predicted != ContradictionType.NONE and example.expected == ContradictionType.NONE:
                false_positive += 1
            elif predicted == ContradictionType.NONE and example.expected != ContradictionType.NONE:
                false_negative += 1

        precision = true_positive / max(true_positive + false_positive, 1)
        recall = true_positive / max(true_positive + false_negative, 1)
        f1 = 2 * precision * recall / max(precision + recall, 1e-9)

        return EvaluationResult(
            precision=precision,
            recall=recall,
            f1=f1,
            support=len(dataset),
            predictions=predictions,
        )


def build_labeled_examples() -> List[LabeledExample]:
    """Tiny helper dataset covering all rule types."""

    return [
        LabeledExample(
            Claim("c1", "Water boils at 100C", "Water boils at 95C"),
            ContradictionType.PROPERTY_MISMATCH,
        ),
        LabeledExample(
            Claim("c2", "Triangles have three sides", "Triangle false three sides"),
            ContradictionType.DEFINITIONAL_VIOLATION,
        ),
        LabeledExample(
            Claim("c3", "All mammals give live birth", "Platypus is an exception"),
            ContradictionType.UNIVERSAL_COUNTEREXAMPLE,
        ),
        LabeledExample(
            Claim("c4", "Always in 1950", "In 2020 things changed"),
            ContradictionType.TEMPORAL_CONFLICT,
        ),
        LabeledExample(
            Claim("c5", "Paris is not the capital of France", "Paris is the capital of France"),
            ContradictionType.DIRECT_NEGATION,
        ),
    ]


__all__ = [
    "LabeledExample",
    "Prediction",
    "EvaluationResult",
    "ContradictionEvaluator",
    "build_labeled_examples",
]
