from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from translator.core import EnglishToCodeTranslator


def main() -> None:
    dataset = json.loads(Path("eval/prompts/golden.json").read_text(encoding="utf-8"))
    translator = EnglishToCodeTranslator()

    total = len(dataset)
    passed = 0
    for case in dataset:
        out = translator.translate(case["prompt"], case["target"])
        ok = all(token in out for token in case["must_contain"])
        if ok:
            passed += 1
        print(f"[{'PASS' if ok else 'FAIL'}] target={case['target']} prompt={case['prompt']}")

    print(f"\nScore: {passed}/{total}")


if __name__ == "__main__":
    main()
