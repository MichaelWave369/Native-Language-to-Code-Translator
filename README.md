# Nevora English-to-Code Translator

English idea → starter code for Python, Blueprint, C++, C#, JavaScript, and GDScript.

## What's now included (all 10 upgrades)

1. **Multi-step generation pipeline**
   - intent parse → decomposition → target design → generation → self-check.
2. **LLM planner with schema validation + retry + fallback**
   - OpenAI planner validates structured JSON and retries; safely falls back to heuristics.
3. **Project scaffolding mode**
   - `--scaffold-dir` creates runnable project skeletons for Python/JS/C#/C++/Godot.
4. **Unreal importer bridge**
   - Exports graph contract + ships prototype importer script (`examples/unreal_importer.py`).
5. **Domain modes**
   - `gameplay`, `automation`, `video-processing`, `web-backend`.
6. **Evaluation harness**
   - `eval/run_eval.py` + golden prompt dataset for regression checks.
7. **Verification adapters**
   - `--verify` supports syntax checks per target when tools exist.
8. **Iterative refinement memory**
   - `--context-file` + `--refine` to improve code based on previous outputs.
9. **Renderer plugin registry**
   - Target renderers moved into `translator/targets/*` with a central registry.
10. **Optional LLM dependency strategy**
   - Base requirements are minimal; LLM dependencies are in `requirements-llm.txt`.

## Quick start

```bash
pip install -r requirements.txt
python -m translator.cli --target python --prompt "Create player jump on space" --mode gameplay --verify
```

## Scaffold a project

```bash
python -m translator.cli \
  --target javascript \
  --prompt "When request arrives validate and respond" \
  --mode web-backend \
  --scaffold-dir artifacts/js_app
```

## Unreal graph contract export

```bash
python -m translator.cli \
  --target blueprint \
  --prompt "When health is zero, play death animation and disable input" \
  --export-uasset-json artifacts/bp_graph.json \
  --blueprint-name BP_PlayerDeath
```

Then use `examples/unreal_importer.py` inside Unreal Editor Python environment as a starting point.

## Evaluation

```bash
python eval/run_eval.py
```
