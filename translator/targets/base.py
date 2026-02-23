from __future__ import annotations

from typing import Protocol

from translator.models import ParsedIntent


class TargetRenderer(Protocol):
    name: str

    def render(self, prompt: str, intent: ParsedIntent, mode: str = "gameplay") -> str:
        ...
