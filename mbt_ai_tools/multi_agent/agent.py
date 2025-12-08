from __future__ import annotations

"""Minimal multi-agent building blocks."""

from dataclasses import dataclass, field
from typing import Callable, Dict, List
import random


@dataclass
class Message:
    sender: str
    recipient: str
    content: str
    metadata: Dict[str, object] = field(default_factory=dict)


class Agent:
    def __init__(self, name: str, policy: Callable[[str], str] | None = None) -> None:
        self.name = name
        self.policy = policy or (lambda message: f"ack:{message}")
        self.state: Dict[str, object] = {"memory": []}

    def act(self, observation: str) -> str:
        response = self.policy(observation)
        self.state["memory"].append({"obs": observation, "resp": response})
        return response

    def receive(self, message: Message) -> Message:
        reply_content = self.act(message.content)
        return Message(sender=self.name, recipient=message.sender, content=reply_content)

    def broadcast(self, peers: List["Agent"], content: str) -> List[Message]:
        return [Message(sender=self.name, recipient=peer.name, content=content) for peer in peers if peer.name != self.name]


def noisy_policy(noise: float = 0.1) -> Callable[[str], str]:
    def _policy(message: str) -> str:
        if random.random() < noise:
            return "noise"
        return f"processed:{message}"

    return _policy


__all__ = ["Agent", "Message", "noisy_policy"]
