from __future__ import annotations

"""Evolutionary loop for multi-agent simulations."""

from dataclasses import dataclass
from typing import Callable, List, Tuple
import random

from .agent import Agent, noisy_policy
from .world import World


@dataclass
class FitnessResult:
    agent: str
    fitness: float


def evaluate_world(world: World, objective: Callable[[Agent], float]) -> List[FitnessResult]:
    results = []
    for agent in world.agents.values():
        results.append(FitnessResult(agent=agent.name, fitness=objective(agent)))
    return results


def evolve_agents(world: World, objective: Callable[[Agent], float], survival_rate: float = 0.5) -> Tuple[World, List[FitnessResult]]:
    scores = evaluate_world(world, objective)
    scores.sort(key=lambda r: r.fitness, reverse=True)
    cutoff = max(1, int(len(scores) * survival_rate))
    survivors = scores[:cutoff]

    new_agents: List[Agent] = []
    for result in survivors:
        parent = world.agents[result.agent]
        mutated_policy = noisy_policy(noise=max(0.05, 0.2 * random.random()))
        child = Agent(name=f"{parent.name}_child{random.randint(0, 999)}", policy=mutated_policy)
        new_agents.append(child)

    for agent in new_agents:
        world.add_agent(agent)

    return world, scores


__all__ = ["FitnessResult", "evaluate_world", "evolve_agents"]
