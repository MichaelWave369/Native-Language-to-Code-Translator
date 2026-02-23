import json

from translator.core import EnglishToCodeTranslator
from translator.planners.heuristic import HeuristicPlanner



def test_pipeline_translation_and_modes() -> None:
    translator = EnglishToCodeTranslator(planner=HeuristicPlanner())
    out = translator.translate(
        prompt="When request arrives validate and respond",
        target="python",
        mode="web-backend",
    )
    assert "GeneratedFeature" in out
    assert "Mode: web-backend" in out



def test_new_target_registry_renders() -> None:
    translator = EnglishToCodeTranslator(planner=HeuristicPlanner())
    prompt = "Spawn enemy when timer reaches zero"

    assert "GeneratedFeature" in translator.translate(prompt=prompt, target="cpp")
    assert "public class GeneratedFeature" in translator.translate(prompt=prompt, target="csharp")
    assert "class GeneratedFeature" in translator.translate(prompt=prompt, target="javascript")
    assert "extends Node" in translator.translate(prompt=prompt, target="gdscript")



def test_unreal_uasset_payload_export_v2(tmp_path) -> None:
    translator = EnglishToCodeTranslator(planner=HeuristicPlanner())
    target = tmp_path / "bp_feature.json"

    result = translator.export_unreal_uasset_payload(
        prompt="When player collides with enemy play hit animation",
        output_path=str(target),
        blueprint_name="BP_TestFeature",
    )

    assert result.endswith("bp_feature.json")
    data = json.loads(target.read_text(encoding="utf-8"))
    assert data["schema"] == "nevora.unreal.blueprint.graph.v2"
    assert data["blueprint_name"] == "BP_TestFeature"
    assert isinstance(data["nodes"], list)
    assert isinstance(data["edges"], list)



def test_scaffold_project_python(tmp_path) -> None:
    translator = EnglishToCodeTranslator(planner=HeuristicPlanner())
    root = translator.scaffold_project(
        prompt="Create a player that jumps",
        target="python",
        output_dir=str(tmp_path / "pyproj"),
    )
    assert (tmp_path / "pyproj" / "src" / "generated_feature.py").exists()
    assert root.endswith("pyproj")



def test_refine_with_context_changes_prompt_usage() -> None:
    translator = EnglishToCodeTranslator(planner=HeuristicPlanner())
    out = translator.translate(
        prompt="add saving",
        target="python",
        mode="automation",
        context="Previous output had no persistence",
        refine=True,
    )
    assert "Previous output context" in out



def test_verify_python_passes() -> None:
    translator = EnglishToCodeTranslator(planner=HeuristicPlanner())
    output = translator.translate("Create jump", "python")
    ok, _ = translator.verify_output(output, "python")
    assert ok
