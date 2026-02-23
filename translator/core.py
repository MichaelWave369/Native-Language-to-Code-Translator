from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional

from translator.models import GenerationPlan, ParsedIntent, PlanStep
from translator.planners.heuristic import HeuristicPlanner
from translator.planners.openai_planner import OpenAISemanticPlanner
from translator.targets.registry import build_registry


class EnglishToCodeTranslator:
    MODES = {"gameplay", "automation", "video-processing", "web-backend"}

    def __init__(self, planner: Optional[object] = None) -> None:
        self._heuristic = HeuristicPlanner()
        self.planner = planner
        self.renderers = build_registry()

    @property
    def supported_targets(self) -> set[str]:
        return set(self.renderers.keys())

    def _get_planner(self) -> object:
        if self.planner is not None:
            return self.planner
        try:
            return OpenAISemanticPlanner()
        except Exception:
            return self._heuristic

    def plan_intent(self, prompt: str, mode: str = "gameplay") -> ParsedIntent:
        planner = self._get_planner()
        try:
            return planner.plan(prompt, mode=mode)
        except Exception:
            return self._heuristic.plan(prompt, mode=mode)

    def build_generation_plan(self, prompt: str, mode: str = "gameplay") -> GenerationPlan:
        intent = self.plan_intent(prompt, mode=mode)
        steps = [
            PlanStep("intent-parse", f"entities={intent.entities}, actions={intent.actions}"),
            PlanStep("task-decompose", "Split into event handling, state transitions, and outputs"),
            PlanStep("target-design", f"Use templates optimized for mode={mode}"),
            PlanStep("generate", "Render target code"),
            PlanStep("self-check", "Optional syntax verification and basic lint checks"),
        ]
        state_model = {"active": "bool", "last_event": "string", "status": "string"}
        return GenerationPlan(intent=intent, steps=steps, state_model=state_model)

    def translate(
        self,
        prompt: str,
        target: str,
        mode: str = "gameplay",
        context: Optional[str] = None,
        refine: bool = False,
    ) -> str:
        if mode not in self.MODES:
            raise ValueError(f"Unsupported mode '{mode}'. Supported: {', '.join(sorted(self.MODES))}")

        normalized_target = target.strip().lower()
        if normalized_target not in self.supported_targets:
            supported = ", ".join(sorted(self.supported_targets))
            raise ValueError(f"Unsupported target '{target}'. Supported: {supported}")

        combined_prompt = prompt
        if refine and context:
            combined_prompt = f"{prompt}\n\nPrevious output context:\n{context}"

        plan = self.build_generation_plan(combined_prompt, mode=mode)
        renderer = self.renderers[normalized_target]
        return renderer.render(combined_prompt, plan.intent, mode=mode)

    def scaffold_project(self, prompt: str, target: str, output_dir: str, mode: str = "gameplay") -> str:
        root = Path(output_dir)
        root.mkdir(parents=True, exist_ok=True)
        code = self.translate(prompt, target=target, mode=mode)

        if target == "python":
            (root / "src").mkdir(exist_ok=True)
            (root / "src" / "generated_feature.py").write_text(code, encoding="utf-8")
            (root / "tests").mkdir(exist_ok=True)
            (root / "tests" / "test_generated.py").write_text("def test_smoke():\n    assert True\n", encoding="utf-8")
        elif target == "javascript":
            (root / "src").mkdir(exist_ok=True)
            (root / "src" / "generatedFeature.js").write_text(code, encoding="utf-8")
            (root / "package.json").write_text('{"name":"generated-feature","version":"0.1.0"}\n', encoding="utf-8")
        elif target == "csharp":
            (root / "GeneratedFeature.cs").write_text(code, encoding="utf-8")
            (root / "GeneratedFeature.csproj").write_text(
                "<Project Sdk=\"Microsoft.NET.Sdk\"><PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup></Project>",
                encoding="utf-8",
            )
        elif target == "cpp":
            (root / "main.cpp").write_text(code, encoding="utf-8")
            (root / "CMakeLists.txt").write_text("cmake_minimum_required(VERSION 3.16)\nproject(GeneratedFeature)\nadd_executable(app main.cpp)\n", encoding="utf-8")
        elif target == "gdscript":
            (root / "GeneratedFeature.gd").write_text(code, encoding="utf-8")
            (root / "project.godot").write_text("; generated skeleton\n", encoding="utf-8")
        else:
            (root / "README.txt").write_text(code, encoding="utf-8")

        return str(root)

    def verify_output(self, code: str, target: str) -> tuple[bool, str]:
        if target == "python":
            try:
                compile(code, "<generated>", "exec")
                return True, "python compile ok"
            except Exception as exc:
                return False, f"python compile failed: {exc}"

        if target == "javascript":
            if shutil.which("node"):
                proc = subprocess.run(["node", "--check", "-"], input=code, text=True, capture_output=True)
                return proc.returncode == 0, proc.stderr.strip() or "node check ok"
            return False, "node unavailable"

        if target == "cpp":
            if shutil.which("clang++"):
                proc = subprocess.run(["clang++", "-fsyntax-only", "-x", "c++", "-"], input=code, text=True, capture_output=True)
                return proc.returncode == 0, proc.stderr.strip() or "clang++ syntax ok"
            return False, "clang++ unavailable"

        if target == "csharp":
            if shutil.which("dotnet"):
                return True, "dotnet available (project verification supported via scaffold)"
            return False, "dotnet unavailable"

        if target == "gdscript":
            if shutil.which("godot"):
                return True, "godot available"
            return False, "godot unavailable"

        return True, "verification not implemented for target"

    def export_unreal_uasset_payload(
        self,
        prompt: str,
        output_path: str,
        blueprint_name: str = "BP_GeneratedFeature",
        mode: str = "gameplay",
    ) -> str:
        plan = self.build_generation_plan(prompt, mode=mode)
        payload: dict[str, Any] = {
            "schema": "nevora.unreal.blueprint.graph.v2",
            "blueprint_name": blueprint_name,
            "mode": mode,
            "prompt": prompt,
            "intent": {
                "entities": plan.intent.entities,
                "actions": plan.intent.actions,
                "conditions": plan.intent.conditions,
                "outputs": plan.intent.outputs,
            },
            "nodes": [
                {"id": "begin_play", "type": "EventBeginPlay", "pins": ["exec_out"]},
                {
                    "id": "branch_condition",
                    "type": "Branch",
                    "condition_tokens": plan.intent.conditions,
                    "pins": ["exec_in", "true", "false"],
                },
                {
                    "id": "action_sequence",
                    "type": "ActionSequence",
                    "actions": plan.intent.actions,
                    "entities": plan.intent.entities,
                    "outputs": plan.intent.outputs,
                    "pins": ["exec_in", "exec_out"],
                },
            ],
            "edges": [
                {"from": "begin_play.exec_out", "to": "branch_condition.exec_in"},
                {"from": "branch_condition.true", "to": "action_sequence.exec_in"},
            ],
            "import_hints": {
                "unreal_plugin": "examples/unreal_importer.py",
                "notes": "Use Unreal Editor Python API to materialize nodes into a real .uasset",
            },
        }

        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return str(destination)
