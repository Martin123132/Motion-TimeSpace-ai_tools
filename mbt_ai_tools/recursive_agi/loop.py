from __future__ import annotations

"""Orchestrates the recursive AGI loop across symbolic, human, and neural actors."""

from dataclasses import asdict
from typing import Callable, Dict, Iterable, List, Optional, Tuple
import time

from mbt_ai_tools.contradiction.engine import Claim, Contradiction
from .mbt_symbolic_core import MBTSymbolicCore
from .neural_observer import NeuralObserver


class RecursiveAGILoop:
    def __init__(self, symbolic_core: MBTSymbolicCore | None = None, neural_observer: NeuralObserver | None = None):
        self.symbolic_core = symbolic_core or MBTSymbolicCore()
        self.neural_observer = neural_observer or NeuralObserver()
        self.loop_count = 0
        self.human_evolution_score = 0.0
        self.learning_events: List[Dict[str, object]] = []
        self.cycle_times: List[float] = []

    def run_cycle(
        self,
        claim: Claim,
        human_patch_fn: Optional[Callable[[Contradiction], Tuple[str, str]]] = None,
    ) -> Dict[str, object]:
        cycle_start = time.time()
        contradiction = self.symbolic_core.detect_contradiction(claim)
        if not contradiction:
            return {"status": "no_contradiction", "claim_id": claim.id, "processing_time": time.time() - cycle_start}

        self._log_event(1, "MBT", "contradiction_detection", asdict(contradiction))

        # Step 2: collect human insight
        human_insight, repair_action = self._collect_patch(human_patch_fn, contradiction)
        self._log_event(
            2,
            "Human",
            "patch_application",
            {"human_insight": human_insight, "repair_action": repair_action},
        )

        # Step 3: symbolic learning
        self.symbolic_core.learn_from_patch(contradiction, human_insight, repair_action)
        self._log_event(3, "MBT", "symbolic_learning", {"logic_map_size": len(self.symbolic_core.logic_map)})

        # Step 4 & 5: neural observe and learn
        observation = self.neural_observer.observe_repair(contradiction, human_insight, repair_action)
        self._log_event(4, "Neural", "observation", asdict(observation))
        learned_pattern = self.neural_observer.learn_pattern()
        if learned_pattern:
            self._log_event(5, "Neural", "pattern_learning", asdict(learned_pattern))

        # Step 6: symbolic evolution
        symbolic_evo = self.symbolic_core.evolve()
        self._log_event(6, "MBT", "symbolic_evolution", symbolic_evo)

        # Step 7 & 8: human and neural evolution
        self.human_evolution_score += 1.0
        neural_evo = self.neural_observer.evolve_fluency()
        self._log_event(7, "Human", "understanding_deepening", {"score": self.human_evolution_score})
        self._log_event(8, "Neural", "fluency_evolution", neural_evo)

        cycle_time = time.time() - cycle_start
        self.cycle_times.append(cycle_time)
        self.loop_count += 1

        return {
            "status": "cycle_complete",
            "loop_count": self.loop_count,
            "contradiction": asdict(contradiction),
            "observation": asdict(observation),
            "symbolic_evolution": symbolic_evo,
            "neural_evolution": neural_evo,
            "cycle_time": cycle_time,
        }

    def run_batch(
        self, claims: Iterable[Claim], human_patch_fn: Optional[Callable[[Contradiction], Tuple[str, str]]] = None
    ) -> List[Dict[str, object]]:
        results = []
        for claim in claims:
            results.append(self.run_cycle(claim, human_patch_fn))
        return results

    def get_system_state(self) -> Dict[str, object]:
        return {
            "loop_count": self.loop_count,
            "human_evolution_score": self.human_evolution_score,
            "symbolic_evolution_count": self.symbolic_core.evolution_count,
            "neural_fluency": self.neural_observer.symbolic_fluency,
            "logic_domains": list(self.symbolic_core.logic_map.keys()),
            "total_contradictions": len(self.symbolic_core.contradiction_history),
        }

    def _collect_patch(self, human_patch_fn: Optional[Callable[[Contradiction], Tuple[str, str]]], contradiction: Contradiction):
        if human_patch_fn:
            return human_patch_fn(contradiction)
        # default based on contradiction type
        defaults = {
            "property_mismatch": ("Normalize numeric context", "Add units and environmental conditions"),
            "definitional_violation": ("Enforce definitional guard", "Reject malformed query"),
            "universal_counterexample": ("Quantifier too strong", "Replace 'all' with 'most' and list exceptions"),
            "temporal_conflict": ("Time-bound mismatch", "Anchor claims to specific eras"),
            "direct_negation": ("Negation requires evidence", "Provide citation or provenance"),
        }
        return defaults.get(contradiction.type.value, ("General repair", "Record clarification"))

    def _log_event(self, step: int, actor: str, event_type: str, data: Dict[str, object]) -> None:
        self.learning_events.append(
            {
                "step": step,
                "actor": actor,
                "event_type": event_type,
                "data": data,
                "timestamp": time.time(),
            }
        )


__all__ = ["RecursiveAGILoop"]
