# Design Document: Backend Harmony Wire-Up

## Overview

The DFM Suite frontend on Harmony talks to a backend service that runs the existing DFM Inspector Flask analyzer logic. This design covers four interlocked decisions:

1. The HTTP/JSON contract between frontend and backend.
2. The transformation layer that converts internal analyzer dicts to the contract.
3. The hosting choice and architecture.
4. The auth model.

## Architecture

```
+----------------------------------+      +----------------------------------+
|  Harmony Frontend (static SPA)   |      |  DFM Inspector Backend           |
|  *.harmony.a2z.com               |      |  dfm-inspector-api.<team>...     |
|                                  | HTTPS|                                  |
|  - React/Vite                    +----->+  - Internal ALB                  |
|  - Cloudscape UI                 |      |  - ECS Fargate                   |
|  - Calls /api/analyze            |      |  - Flask + gunicorn              |
|  - Renders wire format           |      |  - CadQuery + OpenCascade        |
|                                  |      |  - api_contract pydantic         |
|                                  |      |  - api_transform layer           |
+----------------------------------+      +----------------------------------+
                |                                       |
                +-- Midway token forwarded -------------+
                                             |
                                          NAWS validates
```

## The wire format contract

Full schema lives at `docs/api-contract.md`. Pydantic models live at `src/api_contract.py`. Key principles:

* Single response shape for all processes. Process-specific information lives in `findings[].measured_value` / `expected_value` / `rationale`, not in new top-level fields.
* `severity` is always one of `critical | warning | suggestion | passed | info`.
* `location` is null-tolerant. Analyzers can populate it later without breaking the contract.
* `analysis_id` is a UUID generated server-side and used by export endpoints.
* `exports` URLs are relative — the frontend prepends the backend base URL.

### Example response (abridged)

```json
{
  "success": true,
  "analysis_id": "f2c1...",
  "metadata": {
    "process": "Sheet Metal",
    "process_id": "sheet_metal",
    "material": "Aluminum 6061-T6",
    "material_id": "aluminum",
    "filename": "part.step",
    "analyzed_at": "2026-06-26T14:32:11Z"
  },
  "summary": {
    "score": 78.5,
    "total_rules": 14,
    "passed": 8,
    "warnings": 4,
    "critical": 2,
    "info": 0,
    "narrative": "Mostly manufacturable; 2 critical thickness violations to address."
  },
  "findings": [
    {
      "id": "f-001",
      "rule_id": "sheet_metal.material_thickness",
      "rule_name": "Material Thickness",
      "standard": "0.5-3.0mm per 930-00172",
      "severity": "critical",
      "title": "Material thickness 0.30 mm below 0.4 mm minimum",
      "description": "Detected thickness 0.30 mm; below 0.4 mm forming limit",
      "recommendation": "Increase to 0.5 mm minimum",
      "rationale": "Material <0.4mm tears during forming",
      "measured_value": "0.30 mm",
      "expected_value": ">=0.4 mm",
      "cost_impact": "+150-200% from specialized micro-forming",
      "location": null
    }
  ],
  "geometry": {
    "dimensions_mm": {"x": 100, "y": 50, "z": 5},
    "volume_mm3": 25000,
    "surface_area_mm2": 12500,
    "estimated_min_thickness_mm": 0.30,
    "holes_count": 6,
    "bends_count": 2,
    "quality_rating": "Good"
  },
  "exports": {
    "html": "/api/report/f2c1.../html",
    "json": "/api/report/f2c1.../json",
    "docx": "/api/report/f2c1.../docx"
  }
}
```

## Transformation layer

Internal analyzer outputs are heterogeneous (different process analyzers return slightly different fields). The transformation function takes the internal dict and request metadata and returns a validated `ApiAnalyzeResponse`:

```python
def to_api_response(
    internal_result: dict,
    request_metadata: AnalyzeRequestMetadata,
) -> ApiAnalyzeResponse:
    ...
```

### Severity mapping

| Internal source                                | Wire `severity` |
| ---------------------------------------------- | --------------- |
| `all_rules[]` with `status == "FAIL"`          | `critical`      |
| `all_rules[]` with `status == "WARNING"`       | `warning`       |
| `all_rules[]` with `status == "PASS"`          | `passed`        |
| `all_rules[]` with `status == "INFO"`          | `info`          |
| `issues[]` (no equivalent in `all_rules`)      | `critical`      |
| `warnings[]` (no equivalent)                   | `warning`       |
| `suggestions[]`                                | `suggestion`    |
| `passed[]` (no equivalent)                     | `passed`        |

Deduplication is keyed on `(rule_name, severity)`. The `all_rules` entry is the preferred source because it carries the richer per-rule payload.

### Non-mutating

The transformation does not mutate the input internal dict. It builds a new pydantic model. This keeps the existing analyzers' downstream consumers (e.g., the Word export path that re-uses the parser) untouched.

## Hosting

ECS Fargate, fronted by an internal Application Load Balancer, deployed by Apollo. Container image is built from the existing `Dockerfile` via Brazil. The image is published to ECR (internal registry).

### Why Fargate over EC2

* Container-native — the existing Dockerfile drops in cleanly.
* No host management — Apollo deploys to Fargate task definitions; no AMI cycles.
* Right-sized cost — pay per task-second.

### Why Apollo over App Runner or ECS Express

* Owned by the team — bindle, deployment policy, and audit live in standard Amazon plumbing.
* Internal-only — avoids public-internet exposure of CAD uploads.
* Integrates with Pipelines for CI/CD on CR merge.

There is an existing commit (`a608615 feat(deploy): containerize app for AWS App Runner deployment`) that started an App Runner path. The Dockerfile and entrypoint work from that commit are reusable; the deploy target swaps to ECS Fargate.

### Task sizing (initial)

* 2 vCPU, 4 GB memory baseline. CadQuery / OpenCascade is memory-hungry on large STEP files.
* Min 1, Max 4 tasks behind the ALB. Auto-scale on CPU above 70%.
* Health check: `GET /health`, 30-second interval.

## Auth

Midway token forwarded from the frontend in the `Authorization` header. Backend validates via NAWS (or the internal validation library used by sibling services like `ApolloDashboard`). Validated user identity is available via Flask `g.user`.

Audit log lines emit on every successful analysis: `(timestamp, user, process, material, filename, analysis_id, duration_ms)`. CloudWatch Logs is the initial sink; consider Timber for longer retention.

## Result storage

Wire-format responses are kept in an in-memory LRU cache (extending the existing `_parser_cache` pattern) keyed by `analysis_id`. TTL: 1 hour. After expiry, export endpoints return 404 and the user must re-run.

Future: persist to S3 with the analysis ID as the key and a Glacier transition for older results. Out of scope for this spec.

## CORS

Backend allows the prototype origin (and any future Harmony origins) via `Access-Control-Allow-Origin` for `/api/*`. Implemented via Flask-CORS scoped to the API routes only. OPTIONS pre-flight handled.

## Open questions

* Which Midway validation library do other Apollo-deployed services on the team use? Confirm with the team or the `ApolloDashboard` maintainers.
* Should we also expose the existing local-app UI routes (`/`, `/enhanced-test`) on the deployed service, or strictly the `/api/*` surface? Current plan: API-only on the public surface; legacy UI routes blocked at the ALB.
* Do we want streaming progress for slow analyses (large STEPs), or is request-response enough? Plan: request-response for v1; streaming is a follow-up if users complain.

## Testing strategy

* Pydantic model validation runs on every response (cheap and continuous).
* Unit tests for `to_api_response()` cover each severity mapping, dedup logic, and missing-field edge cases.
* One end-to-end test per process (sheet metal, CNC, injection molding, die casting, welding) loads a fixture STEP, runs the analyzer, transforms, and validates against the contract.
* Optional: a frontend contract test that confirms the rendered UI for a fixture wire-format payload.
