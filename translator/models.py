from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ParsedIntent:
    entities: List[str]
    actions: List[str]
    conditions: List[str]
    outputs: List[str] = field(default_factory=list)


@dataclass
class PlanStep:
    name: str
    details: str


@dataclass
class GenerationPlan:
    intent: ParsedIntent
    steps: List[PlanStep]
    state_model: Dict[str, str]
