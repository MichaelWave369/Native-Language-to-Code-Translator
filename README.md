# Nevora English-to-Code Translator

English idea → starter code for Python, Blueprint, C++, C#, JavaScript, and GDScript.

## Next phase (v6) implemented

### 1) Build-level scaffold verification
- Added `verify_scaffold_build(...)` to run tool-based checks on generated scaffolds.
- Supports Python/JavaScript/C++/C# verification when local tools exist.
- CLI supports `--verify-scaffold-build`.

### 2) Explain-plan export to file
- CLI supports `--explain-plan-file` to write plan diagnostics JSON to disk.
- Useful for CI artifacts and debugging pipelines.

### 3) Evaluation buildability metric
- Eval now computes a new buildability score by scaffolding each case and running build checks.
- Existing structure, intent coverage, and determinism metrics are retained.

### 4) Prior v5 capabilities retained
- Planner provider abstraction: `auto`, `heuristic`, `openai`.
- Optional strict safety mode via `--strict-safety`.

## Quick start

```bash
pip install -r requirements.txt
python -m translator.cli --target python --prompt "Create player jump on space" --mode gameplay --verify
```

## Scaffold + build verification

```bash
python -m translator.cli \
  --target python \
  --prompt "Create player jump on space" \
  --scaffold-dir artifacts/py_app \
  --verify-scaffold \
  --verify-scaffold-build
```

## Explain plan artifact

```bash
python -m translator.cli \
  --target cpp \
  --prompt "Spawn enemy when timer reaches zero" \
  --explain-plan-file artifacts/plan.json
```

## Evaluation

```bash
python eval/run_eval.py
```
