from __future__ import annotations

import json
import os
from typing import Any


WORLD_BUILDER_SYSTEM_PROMPT = (
    "You are a game world builder and code generator. "
    "Given staged world design inputs, generate a runnable Python + Pygame starter project. "
    "Return STRICT JSON only with keys: environment, characters, rules, events, main. "
    "Each value must be a complete code section string. "
    "Make sure sections are connected and coherent."
)


def build_world_builder_prompt(
    environment: str,
    characters: str,
    rules: str,
    events: str,
) -> str:
    return (
        "Build a complete connected game world using these 4 design stages:\n\n"
        f"1) Environment:\n{environment}\n\n"
        f"2) Characters:\n{characters}\n\n"
        f"3) Rules:\n{rules}\n\n"
        f"4) Events:\n{events}\n\n"
        "Output strict JSON with keys: environment, characters, rules, events, main. "
        "The `main` section should import/use the other sections and be runnable with pygame."
    )


def parse_world_builder_response(raw: str) -> dict[str, str]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("World Builder response was not valid JSON") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("World Builder response must be a JSON object")

    required = ["environment", "characters", "rules", "events", "main"]
    missing = [k for k in required if k not in payload]
    if missing:
        raise RuntimeError(f"World Builder response missing keys: {', '.join(missing)}")

    result: dict[str, str] = {}
    for key in required:
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(f"World Builder key '{key}' must be a non-empty string")
        result[key] = value
    return result


def generate_world_with_claude(
    environment: str,
    characters: str,
    rules: str,
    events: str,
    model: str = "claude-haiku-4-5",
    max_tokens: int = 4000,
) -> dict[str, str]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")

    try:
        from anthropic import Anthropic  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("anthropic package is required for World Builder generation") from exc

    client = Anthropic(api_key=api_key)
    prompt = build_world_builder_prompt(environment, characters, rules, events)
    response = client.messages.create(
        model=model,
        system=WORLD_BUILDER_SYSTEM_PROMPT,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )

    chunks: list[str] = []
    for block in getattr(response, "content", []):
        text = getattr(block, "text", None)
        if text:
            chunks.append(text)

    raw = "\n".join(chunks).strip()
    if not raw:
        raise RuntimeError("Claude returned an empty response for World Builder")
    return parse_world_builder_response(raw)
