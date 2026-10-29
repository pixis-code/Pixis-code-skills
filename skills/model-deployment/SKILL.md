---
name: model-deployment
description: "Prepare, validate, and deploy ML models (API, Docker, local serve). Use when packaging a model for inference, FastAPI/Flask endpoints, Dockerizing a model, or troubleshooting serving. Not for Docker daemon issues alone (docker-environment-manager), API debug without models (api-backend-troubleshooter), charts (data-visualization), or notebook EDA (jupyter-notebook)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: MLOps
    tags: [ml, deployment, inference, fastapi, docker, pytorch, tensorflow, sklearn]
    related_skills: [docker-environment-manager, api-backend-troubleshooter, fastmcp, jupyter-notebook]
    attribution: New Pixis skill; serving patterns informed by Hermes optional mlops skills (vLLM/Modal) without copying Hermes runtime
---

# Model deployment

Inspect a project’s ML artifacts and help **prepare, locally validate, containerize,
and troubleshoot** model inference serving. Supports common stacks (scikit-learn,
PyTorch, TensorFlow/Keras) and delivery shapes (REST API, Docker, optional cloud
inference) when tools and credentials exist.

**When to use:** serialize/load a model · inference endpoint · Dockerfile for a
model service · health checks · dependency/runtime errors in serving · staging
prep.

**Do not use:** Docker Engine/Compose crashes with no model angle →
`docker-environment-manager`; HTTP 4xx/5xx on a healthy non-ML API →
`api-backend-troubleshooter`; charts/EDA → `data-visualization` /
`jupyter-notebook`; MCP tool servers → `fastmcp`.

## Safety / authorization

1. **Never** deploy to production, create paid cloud resources, or change live
   infra without **explicit** user approval for that action.
2. Distinguish clearly: local validation ≠ staging deploy ≠ production success.
3. Do not print secrets (API keys, cloud tokens). Reference env var **names** only.
4. Inspect existing Docker/K8s/compose/serve configs before adding new ones.

## Dependencies

| Kind | Items |
|------|--------|
| Detect / optional | `scikit-learn`, `torch`, `tensorflow` / `keras`, `joblib`, `onnxruntime` |
| Serving (common) | `fastapi`, `uvicorn`, `flask` (project choice) |
| Containers | Docker CLI (via `docker-environment-manager` if daemon issues) |
| Optional cloud | provider CLIs/SDKs only when user requests (Modal, etc.) — setup first |

```bash
bash scripts/ensure_deps.sh --check-only
```

Heavy frameworks are **not** auto-installed by default. Install into the project
venv only when the user approves.

## Stages (label every result)

| Stage | Meaning |
|-------|---------|
| Inspect | Framework, artifact paths, deps, existing serve/Docker configs |
| Prepare | Serialize, requirements, endpoint stub, env/logging/health |
| Local validate | Load model + run a sample inference in-process or localhost |
| Staging deploy | Deploy only with explicit approval to a non-prod target |
| Production | Explicit approval + verification; never claim from local-only |

## Procedure

### 1. Inspect the project

Find model artifacts (`.pt`, `.pth`, `.ckpt`, `.pkl`, `.joblib`, `.h5`, `.onnx`,
`SavedModel/`), training/serve entrypoints, `requirements*.txt` / `pyproject.toml`,
Dockerfiles, compose files, and existing `/health` or `/predict` routes. Detect
framework from imports and file types. Summarize before changing files.

### 2. Prepare for serving

Choose a delivery shape matching the repo (extend existing app > new FastAPI
stub). Cover:

- Model path via env (e.g. `MODEL_PATH`) — never hardcode secrets
- Load-once at startup; clear errors if artifact missing
- Inference input validation and typed response
- `/health` (process up) and optionally `/ready` (model loaded)
- Logging without dumping PII or secrets
- Pinned runtime deps consistent with training when possible

Example local FastAPI shape (adapt to project):

```python
# illustrative — prefer project's patterns
from fastapi import FastAPI
import os
app = FastAPI()
MODEL = None
@app.on_event("startup")
def load():
    global MODEL
    path = os.environ["MODEL_PATH"]
    # load with the project's framework
@app.get("/health")
def health(): return {"status": "ok"}
@app.post("/predict")
def predict(payload: dict): ...
```

### 3. Local validate before deploy

1. Confirm artifact loads in the target Python env  
2. Run one sample inference; report latency/shape/errors  
3. If serving HTTP: start locally, hit `/health` and `/predict`  
4. If Dockerizing: build image, run container, same checks — use
   `docker-environment-manager` for daemon/build failures  

Do **not** mark deployment successful after only a successful import.

### 4. Container / infra (when requested)

- Prefer extending existing Dockerfile/compose  
- Multi-stage builds when useful; non-root user when straightforward  
- Healthcheck against `/health` or `/ready`  
- Resource notes (CPU/GPU/memory) as guidance — don’t invent cluster quotas  

Cloud GPU serverless (e.g. Modal-style) only when the user asks and CLI/auth
exists; otherwise give setup steps (`modal setup`, etc.) and stop.

### 5. Troubleshoot serving failures

Classify: missing dep · wrong artifact/version · OOM · CUDA/device mismatch ·
bad env path · port bind · timeout · schema mismatch. Reproduce locally when
possible. For pure container networking/daemon issues, hand off to
`docker-environment-manager`.

## Pitfalls

- Claiming “deployed to production” after localhost or dry-run only  
- Auto-creating paid cloud GPUs  
- Overwriting working serve configs without reading them first  
- Training-serving skew (preprocessing mismatch)  
- Logging API keys or full credentials  

## Completion criteria

- Framework + artifact paths identified (or blockers stated)
- Stage clearly labeled (inspect / prepare / local validate / staging / prod)
- Local load + sample inference attempted when artifacts exist
- No production/paid action without explicit approval
- Secrets referenced by env name only
