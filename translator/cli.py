from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import EnglishToCodeTranslator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="English-to-code translator")
    parser.add_argument("--target", required=True)
    parser.add_argument("--prompt", required=True, help="English description to translate")
    parser.add_argument(
        "--mode",
        default="gameplay",
        choices=["gameplay", "automation", "video-processing", "web-backend"],
    )
    parser.add_argument("--context-file", help="Optional previous output context for iterative refinement")
    parser.add_argument("--refine", action="store_true", help="Enable context-aware iterative refinement")
    parser.add_argument("--verify", action="store_true", help="Run target-specific syntax checks")
    parser.add_argument("--scaffold-dir", help="Generate a starter project scaffold in this folder")
    parser.add_argument("--verify-scaffold", action="store_true", help="Verify scaffold file/build structure")
    parser.add_argument("--export-uasset-json", help="Optional path to export Unreal Blueprint graph contract JSON")
    parser.add_argument("--blueprint-name", default="BP_GeneratedFeature")
    parser.add_argument("--explain-plan", action="store_true", help="Print planner/IR explanation as JSON")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    translator = EnglishToCodeTranslator()
    context = None
    if args.context_file:
        context = Path(args.context_file).read_text(encoding="utf-8")

    output = translator.translate(
        prompt=args.prompt,
        target=args.target,
        mode=args.mode,
        context=context,
        refine=args.refine,
    )
    print(output)

    if args.explain_plan:
        explanation = translator.explain_plan(args.prompt, target=args.target, mode=args.mode)
        print("\n[plan]")
        print(json.dumps(explanation, indent=2))

    if args.verify:
        ok, message = translator.verify_output(output, args.target)
        status = "ok" if ok else "warn"
        print(f"\n[verify:{status}] {message}")

    scaffold_root = None
    if args.scaffold_dir:
        scaffold_root = translator.scaffold_project(args.prompt, target=args.target, output_dir=args.scaffold_dir, mode=args.mode)
        print(f"\n[scaffold] created at: {scaffold_root}")

    if args.verify_scaffold:
        if scaffold_root is None and args.scaffold_dir:
            scaffold_root = args.scaffold_dir
        if scaffold_root is None:
            print("\n[verify-scaffold:warn] --verify-scaffold used without --scaffold-dir")
        else:
            ok, message = translator.verify_scaffold(scaffold_root, args.target)
            status = "ok" if ok else "warn"
            print(f"\n[verify-scaffold:{status}] {message}")

    if args.export_uasset_json:
        export_path = translator.export_unreal_uasset_payload(
            prompt=args.prompt,
            output_path=args.export_uasset_json,
            blueprint_name=args.blueprint_name,
            mode=args.mode,
        )
        print(f"\n[export] Unreal graph payload written to: {export_path}")


if __name__ == "__main__":
    main()
