from __future__ import annotations

from translator.models import ParsedIntent


class PythonRenderer:
    name = "python"

    def render(self, prompt: str, intent: ParsedIntent, mode: str = "gameplay") -> str:
        return f'''"""Auto-generated from English prompt.
Prompt: {prompt}
Mode: {mode}
"""

class GeneratedFeature:
    def __init__(self):
        self.entities = {intent.entities!r}
        self.outputs = {intent.outputs!r}

    def run(self, event: dict) -> None:
        if event.get("type") in ("input", "tick", "request"):
            print("Actions: {', '.join(intent.actions)}")
'''
