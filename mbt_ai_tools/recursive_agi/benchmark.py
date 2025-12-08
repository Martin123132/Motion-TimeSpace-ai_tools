from __future__ import annotations

"""Quick benchmarking helper for contradiction detection within the loop."""

from typing import Sequence

from mbt_ai_tools.contradiction.evaluator import ContradictionEvaluator, build_labeled_examples
from mbt_ai_tools.contradiction.engine import Claim
from .loop import RecursiveAGILoop


def run_contradiction_benchmark(loop: RecursiveAGILoop | None = None):
    loop = loop or RecursiveAGILoop()
    evaluator = ContradictionEvaluator(loop.symbolic_core.engine)
    dataset = build_labeled_examples()
    result = evaluator.evaluate(dataset)
    return result


def synthetic_claims() -> Sequence[Claim]:
    return [
        Claim("s1", "Water boils at 100C", "Water boils at 100C at sea level"),
        Claim("s2", "All mammals give live birth", "Platypus is a mammal that lays eggs"),
        Claim("s3", "Triangles have three sides", "Triangle false three sides"),
    ]


__all__ = ["run_contradiction_benchmark", "synthetic_claims"]
