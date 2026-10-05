# Weather Data Analyzer: project architecture

This diagram describes the implemented local service. The domain path is deterministic Python logic; it does not call a hosted model or execute production changes.

```mermaid
flowchart LR
  C["Client / JSON request"] --> A["FastAPI app: src/weather/main.py"]
  A --> D["/analyze: domain handler"]
  D --> L["analyze.py: domain logic"]
  L --> R["JSON result or InputError"]
  A --> O["/v1 ops router"]
  O --> W["In-memory workspaces and jobs"]
  O --> U["In-memory audit and counters"]
  H["Caller-supplied X-Tenant-Id"] --> O
```

The handler translates `InputError` to HTTP 422. Domain logic is implemented in [analyze.py](src/weather/analyze.py); router registration is in [main.py](src/weather/main.py). Ops state and policy checks are in [ops.py](src/weather/ops.py). The tenant header is a lab selector, not authenticated identity. Global dictionaries are process-local and reset on restart. Ops jobs are records; no worker executes them or invokes the domain endpoint.

## Repository components

| Path | Responsibility |
| --- | --- |
| [src/weather/analyze.py](src/weather/analyze.py) | Domain behavior and validation |
| [src/weather/main.py](src/weather/main.py) | HTTP routes and domain error translation |
| [src/weather/ops.py](src/weather/ops.py) | Workspace/job records, tenant filtering, audit, counters |
| [tests](tests/) | Domain examples and ops behavior checks |
| [Dockerfile](Dockerfile) | Python runtime and Uvicorn entry point |
| [k8s](k8s/) | Local Kubernetes deployment examples |

## Deployment boundary

The Dockerfile serves `weather.main:app` on port 8080. Container packaging does not add storage durability, authentication, or job execution. Multiple workers hold separate ops state. Kubernetes manifests are lab examples, not evidence that a customer environment is deployed.

## Request and job flows

See [process diagrams](docs/PROCESS_FLOW.md) for the domain request and the independent approval state flow. See [interview questions and answers](INTERVIEW_QA.md) for concrete behavior, tradeoffs, and limitations.
