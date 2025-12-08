"""Demonstrate the recursive AGI loop processing a batch of claims."""

from mbt_ai_tools.contradiction.engine import Claim, ContradictionType
from mbt_ai_tools.recursive_agi.loop import RecursiveAGILoop


def human_patch(contradiction):
    if contradiction.type == ContradictionType.PROPERTY_MISMATCH:
        return ("Temperature requires altitude context", "Add altitude condition")
    if contradiction.type == ContradictionType.UNIVERSAL_COUNTEREXAMPLE:
        return ("Universal quantifier too strong", "Switch to 'most' and list exceptions")
    return ("Default reasoning", "Record clarification")


def main():
    loop = RecursiveAGILoop()
    claims = [
        Claim("c1", "Water boils at 100C", "Water boils at 95C"),
        Claim("c2", "All mammals give live birth", "Platypus lays eggs"),
        Claim("c3", "Triangles have three sides", "Triangle false three sides"),
    ]
    results = loop.run_batch(claims, human_patch)
    for res in results:
        print(res)
    print("\nSystem state:")
    print(loop.get_system_state())


if __name__ == "__main__":
    main()
