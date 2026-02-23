# Nevora English-to-Code Translator

English idea → starter code for Python, Blueprint, C++, C#, JavaScript, and GDScript.

## Next phase (v4) implemented

### 1) Explainability layer
- Added `explain_plan(...)` in core to return a structured payload with intent, IR, steps, and state model.
- Added CLI `--explain-plan` to print JSON plan diagnostics.

### 2) Stronger regression scoring
- Eval now checks three dimensions per case:
  - structure checks
  - intent token coverage
  - deterministic output consistency
- Added determinism score summary to evaluation output.

### 3) Prior v3 capabilities retained
- Canonical schema normalization and IR-first planning.
- Scaffold creation + scaffold verification via CLI.
- Unreal graph payload export with IR included.

## Quick start

```bash
pip install -r requirements.txt
python -m translator.cli --target python --prompt "Create player jump on space" --mode gameplay --verify
```

## Explain plan

```bash
python -m translator.cli \
  --target cpp \
  --prompt "Spawn enemy when timer reaches zero" \
  --mode gameplay \
  --explain-plan
```

## Scaffold + verify

```bash
python -m translator.cli \
  --target javascript \
  --prompt "When request arrives validate and respond" \
  --mode web-backend \
  --scaffold-dir artifacts/js_app \
  --verify-scaffold
```

## Evaluation

```bash
python eval/run_eval.py
```
