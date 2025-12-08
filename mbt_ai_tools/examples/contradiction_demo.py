"""Run a quick contradiction detection demo."""

from mbt_ai_tools.contradiction.engine import Claim, ContradictionEngine
from mbt_ai_tools.contradiction.evaluator import ContradictionEvaluator, build_labeled_examples


def main():
    engine = ContradictionEngine()
    claims = [
        Claim("demo1", "Water boils at 100C", "Water boils at 95C"),
        Claim("demo2", "Triangles have three sides", "Triangle true three sides"),
    ]
    for claim in claims:
        contradiction = engine.detect(claim)
        print(f"Claim {claim.id}: {claim.query}")
        if contradiction:
            print(f" -> Contradiction detected: {contradiction.type.value} ({contradiction.note})")
        else:
            print(" -> No contradiction detected")

    evaluator = ContradictionEvaluator(engine)
    result = evaluator.evaluate(build_labeled_examples())
    print("\nEvaluation:")
    print(f"Precision: {result.precision:.2f} | Recall: {result.recall:.2f} | F1: {result.f1:.2f}")


if __name__ == "__main__":
    main()
