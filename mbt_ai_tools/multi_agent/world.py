from __future__ import annotations

"""Simple multi-agent world supporting synchronous message passing."""

from typing import Dict, List

from .agent import Agent, Message


class World:
    def __init__(self, agents: List[Agent] | None = None) -> None:
        self.agents: Dict[str, Agent] = {a.name: a for a in agents} if agents else {}
        self.time = 0

    def add_agent(self, agent: Agent) -> None:
        self.agents[agent.name] = agent

    def step(self, broadcasts: Dict[str, str]) -> List[Message]:
        self.time += 1
        outbound: List[Message] = []
        for sender_name, content in broadcasts.items():
            sender = self.agents[sender_name]
            peers = [agent for name, agent in self.agents.items() if name != sender_name]
            outbound.extend(sender.broadcast(peers, content))

        inbox = []
        for message in outbound:
            recipient = self.agents.get(message.recipient)
            if recipient:
                inbox.append(recipient.receive(message))
        return inbox


__all__ = ["World"]
