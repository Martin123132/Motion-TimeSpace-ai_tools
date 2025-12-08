from __future__ import annotations

"""Lightweight contradiction detection engine.

The module centers around a composable :class:`ContradictionEngine` that bundles
simple symbolic checks with optional learned patterns. It is intentionally
minimal so it can run in constrained environments while remaining easy to
extend with new rules.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple
import re
import time


class ContradictionType(str, Enum):
    """Enumerates contradiction categories handled by the engine."""

    DIRECT_NEGATION = "direct_negation"
    PROPERTY_MISMATCH = "property_mismatch"
    DEFINITIONAL_VIOLATION = "definitional_violation"
    UNIVERSAL_COUNTEREXAMPLE = "universal_counterexample"
    TEMPORAL_CONFLICT = "temporal_conflict"
    NONE = "none"


@dataclass
class Claim:
    """Simple container for a premise/query pair.

    Attributes:
        id: Stable identifier for cross referencing.
        premise: Statement representing prior knowledge.
        query: Statement being tested against the premise.
        domain: Optional domain tag used by heuristics.
        metadata: Arbitrary metadata stored on the instance.
    """

    id: str
    premise: str
    query: str
    domain: str | None = None
    metadata: Dict[str, object] | None = None


@dataclass
class Contradiction:
    """Represents a detected contradiction."""

    claim_id: str
    type: ContradictionType
    note: str
    repair_suggestion: str
    detected_at: float = field(default_factory=time.time)
    score: float = 1.0


Rule = Callable[[Claim], Optional[Contradiction]]


class ContradictionEngine:
    """Symbolic contradiction detector with composable rules."""

    def __init__(self, rules: Optional[Sequence[Rule]] = None) -> None:
        self.rules: List[Rule] = list(rules) if rules else self._default_rules()
        self.history: List[Contradiction] = []

    def _default_rules(self) -> List[Rule]:
        return [
            self._direct_negation_rule,
            self._property_mismatch_rule,
            self._definitional_rule,
            self._universal_rule,
            self._temporal_conflict_rule,
        ]

    def add_rule(self, rule: Rule) -> None:
        """Register a new rule at runtime."""

        self.rules.append(rule)

    def detect(self, claim: Claim) -> Optional[Contradiction]:
        """Run all rules until the first contradiction is found."""

        for rule in self.rules:
            contradiction = rule(claim)
            if contradiction:
                self.history.append(contradiction)
                return contradiction
        return None

    def detect_batch(self, claims: Iterable[Claim]) -> List[Tuple[Claim, Optional[Contradiction]]]:
        """Evaluate a collection of claims and return paired results."""

        return [(claim, self.detect(claim)) for claim in claims]

    # --- built-in rules -------------------------------------------------

    def _direct_negation_rule(self, claim: Claim) -> Optional[Contradiction]:
        premise = claim.premise.lower()
        query = claim.query.lower()
        if premise.startswith("not ") and premise[4:] in query:
            return Contradiction(
                claim_id=claim.id,
                type=ContradictionType.DIRECT_NEGATION,
                note="Query affirms a negated premise",
                repair_suggestion="Clarify whether negation is scoped to all contexts.",
                score=0.9,
            )
        if query.startswith("not ") and query[4:] in premise:
            return Contradiction(
                claim_id=claim.id,
                type=ContradictionType.DIRECT_NEGATION,
                note="Query negates the premise",
                repair_suggestion="Add provenance or evidential support for the negation.",
                score=0.9,
            )
        return None

    def _property_mismatch_rule(self, claim: Claim) -> Optional[Contradiction]:
        premise = claim.premise.lower()
        query = claim.query.lower()

        # Temperature mismatch with simple numeric extraction
        if "boil" in premise and "boil" in query:
            premise_temp = self._extract_number(premise)
            query_temp = self._extract_number(query)
            if premise_temp is not None and query_temp is not None and premise_temp != query_temp:
                return Contradiction(
                    claim_id=claim.id,
                    type=ContradictionType.PROPERTY_MISMATCH,
                    note=f"Boiling point differs: premise={premise_temp}, query={query_temp}",
                    repair_suggestion="Normalize measurement units or capture altitude context.",
                    score=0.8,
                )

        # Simple unit mismatch
        if ("kilogram" in premise or "kg" in premise) and ("pound" in query or "lb" in query):
            return Contradiction(
                claim_id=claim.id,
                type=ContradictionType.PROPERTY_MISMATCH,
                note="Mass is compared across unit systems without conversion",
                repair_suggestion="Convert units or store canonical SI representation.",
                score=0.7,
            )
        return None

    def _definitional_rule(self, claim: Claim) -> Optional[Contradiction]:
        premise = claim.premise.lower()
        query = claim.query.lower()
        if "triangle" in premise and "three" in premise and "false" in query:
            return Contradiction(
                claim_id=claim.id,
                type=ContradictionType.DEFINITIONAL_VIOLATION,
                note="Query denies definitional property of triangles",
                repair_suggestion="Reject malformed query or revisit category constraints.",
                score=0.95,
            )
        if "prime" in premise and "even" in query and "false" in query:
            return Contradiction(
                claim_id=claim.id,
                type=ContradictionType.DEFINITIONAL_VIOLATION,
                note="Query violates prime definition with even-number exception",
                repair_suggestion="Explicitly encode special cases (e.g., 2 is prime).",
                score=0.85,
            )
        return None

    def _universal_rule(self, claim: Claim) -> Optional[Contradiction]:
        premise = claim.premise.lower()
        query = claim.query.lower()
        if "all " in premise and any(token in query for token in ["exception", "counterexample", "false"]):
            return Contradiction(
                claim_id=claim.id,
                type=ContradictionType.UNIVERSAL_COUNTEREXAMPLE,
                note="Universal premise challenged by a counterexample in the query",
                repair_suggestion="Change quantifier to 'most' or record known exceptions.",
                score=0.88,
            )
        if "all mammals" in premise and "platypus" in query:
            return Contradiction(
                claim_id=claim.id,
                type=ContradictionType.UNIVERSAL_COUNTEREXAMPLE,
                note="Platypus counters universal mammal live-birth claim",
                repair_suggestion="Annotate monotremes as explicit exceptions.",
                score=0.9,
            )
        return None

    def _temporal_conflict_rule(self, claim: Claim) -> Optional[Contradiction]:
        premise = claim.premise.lower()
        query = claim.query.lower()
        time_refs = re.findall(r"(\d{4})", premise + " " + query)
        if len(set(time_refs)) >= 2 and "always" in premise:
            return Contradiction(
                claim_id=claim.id,
                type=ContradictionType.TEMPORAL_CONFLICT,
                note="Time-dependent statement conflicts with 'always' quantifier",
                repair_suggestion="Replace 'always' with bounded time span and cite evidence.",
                score=0.6,
            )
        return None

    @staticmethod
    def _extract_number(text: str) -> Optional[float]:
        match = re.search(r"(-?\d+(?:\.\d+)?)", text)
        return float(match.group(1)) if match else None


__all__ = [
    "Claim",
    "Contradiction",
    "ContradictionEngine",
    "ContradictionType",
]
