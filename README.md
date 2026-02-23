# Natural Language-to-Code Translator NL2CT

Translate natural-language ideas into starter code for Python, Blueprint, C++, C#, JavaScript, and GDScript.

## Next phase (v13) implemented

### 1) Speed optimization with lattice RAG cache
- Added a lightweight in-memory retrieval cache keyed by a **12x12x12x12 lattice** bucket.
- Each translation can store/retrieve nearby prior generations to reuse context and reduce repeated planning overhead on similar prompts.
- Batch reports now include `lattice_shape` and `lattice_bucket_counts` for observability.

### 2) AI swarm batch execution
- Batch translation now supports parallel workers for swarm execution via `swarm_workers` (CLI: `--swarm-workers`).
- Maintains deterministic output ordering by original item index while executing items concurrently.

### 3) VM-like sandbox command execution
- Added `run_in_vm_sandbox(...)` for isolated command execution in a temporary working directory with timeout protection.
- CLI support: `--sandbox-command ...` to run quick validation/safety tasks in the sandbox flow.

### 4) Multilingual + audio pipeline retained
- Multilingual prompt normalization (English/Spanish/French/German/Portuguese).
- Audio input (`--audio-input`) with transcript-file fallback.
- Audio output (`--audio-output`) with `.txt` fallback when TTS is unavailable.

## Quick start

```bash
pip install -r requirements.txt
python -m translator.cli --target python --prompt "Create player jump on space" --mode gameplay --verify
```

## Swarm batch example

```bash
python -m translator.cli \
  --target python \
  --batch-input batch.jsonl \
  --batch-report artifacts/batch_report.json \
  --swarm-workers 4
```

## Sandbox command example

```bash
python -m translator.cli \
  --target python \
  --sandbox-command python3 /tmp/sandbox_cmd.py \
  --prompt "Create player jump"
```

## Audio + multilingual example

```bash
python -m translator.cli \
  --target python \
  --source-language spanish \
  --audio-input /tmp/nevora_audio_prompt.txt \
  --audio-output artifacts/speech.wav
```

## Evaluation

```bash
python eval/run_eval.py
```
