# Requirements Document

## Introduction

DFM Inspector's analytical backend currently runs as a local Flask app. The Harmony frontend at `rapid-lion-proto-1a492d63.beta.prototype.amazon.dev` renders the DFM Suite UI but mocks every call to `/api/analyze` with sample data. This spec wires the two together so the Harmony UI runs real CAD analysis against the Flask backend.

The deliverable spans six phases: lock the API contract, add a transformation layer in the backend that emits the contract, host the backend with a stable HTTPS URL, add export endpoints, point the Harmony frontend at the real URL, and add a Midway-based auth bridge between frontend and backend.

The contract is intentionally decoupled from internal analyzer dict shapes so the backend can evolve internal types without breaking the frontend.

### Priority and Sequencing

* **P0 — Contract and transformation:** Requirements 1, 2. Required before any deploy work.
* **P1 — Backend hosting:** Requirement 3. Required to make the URL live.
* **P2 — Export endpoints:** Requirement 4. Enables Export buttons in the UI.
* **P3 — Frontend wire-up:** Requirement 5. Brings real analysis to the prototype URL.
* **P4 — Auth bridge:** Requirement 6. Restricts access to Midway-authenticated users.

### Out of Scope

* Modifying internal analyzer logic (rules, thresholds, calculations).
* Refactoring the CadQuery / OpenCascade integration.
* Building should-cost (BDI / DFMA) or Teamcenter integration; those are separate specs.
* Adding new analyzers; this spec only changes how existing results are surfaced.

## Requirement 1 — Stable Wire Format

**As a** Harmony frontend developer
**I want** `POST /api/analyze` to return a stable, documented JSON shape
**So that** I can render summary cards, severity-coded findings, filters, and export buttons without depending on internal backend types.

### Acceptance Criteria

1. WHEN a valid `POST /api/analyze` request is received with `upload_id`, `filename`, `process`, and `material` THEN the response SHALL include top-level fields `success`, `analysis_id`, `metadata`, `summary`, `findings`, `geometry`, and `exports`.
2. WHEN findings are produced THEN each finding SHALL have a `severity` field with one of: `critical`, `warning`, `suggestion`, `passed`, `info`.
3. WHEN findings are produced THEN each finding SHALL include `id`, `rule_id`, `rule_name`, `title`, `description`, `recommendation`, `rationale`, `measured_value`, `expected_value`, `cost_impact`, and `location` (the last may be null).
4. WHEN the summary block is produced THEN it SHALL contain `score`, `total_rules`, `passed`, `warnings`, `critical`, `info`, and `narrative`.
5. WHEN analysis succeeds THEN `metadata.analyzed_at` SHALL be an ISO-8601 timestamp in UTC.
6. WHEN analysis succeeds THEN `exports` SHALL contain URL templates for `html`, `json`, and `docx` formats, each containing the `analysis_id`.
7. WHEN the wire format is documented THEN a markdown contract SHALL live at `docs/api-contract.md` describing every field, type, and example.
8. WHEN the wire format is implemented THEN pydantic models for the contract SHALL live at `src/api_contract.py` and validate any response before it is returned.

## Requirement 2 — Transformation Layer

**As a** backend developer
**I want** internal analyzer dict outputs converted to the wire format by a dedicated transformation layer
**So that** internal analyzer code can keep its current shape while the frontend gets a stable contract.

### Acceptance Criteria

1. WHEN an analyzer returns its internal dict THEN a function `to_api_response(internal_result, request_metadata)` in `src/api_transform.py` SHALL convert it to the wire format.
2. WHEN any analyzer `issues`, `warnings`, `suggestions`, or `passed` entries are present THEN each SHALL be mapped to a finding with the appropriate severity.
3. WHEN an analyzer `all_rules` array is present THEN each rule SHALL be mapped to a finding with severity derived from its status: `PASS` → `passed`, `WARNING` → `warning`, `FAIL` → `critical`, `INFO` → `info`.
4. WHEN duplicate findings appear in both `issues`/`warnings`/`suggestions` and `all_rules` THEN deduplication SHALL prefer the `all_rules` entry as the source of truth.
5. WHEN a finding has no `(x, y, z)` coordinates available THEN its `location` field SHALL be null and the contract SHALL remain valid.
6. WHEN the transformation runs THEN it SHALL NOT mutate the internal analyzer dict.
7. WHEN `/api/analyze` is called THEN it SHALL apply `to_api_response` before `jsonify` and return the transformed shape.

## Requirement 3 — Backend Hosting with HTTPS

**As a** PDE engineer using the Harmony app
**I want** the DFM Inspector backend to be reachable from the prototype URL with a stable HTTPS endpoint
**So that** real analyses run when I click Run Analysis.

### Acceptance Criteria

1. WHEN the backend is deployed THEN it SHALL be reachable at a stable HTTPS URL under team-controlled DNS.
2. WHEN deployed THEN it SHALL use a Brazil-built container image, owned by bindle `Prod-Dev-Eng`.
3. WHEN deployed THEN the compute layer SHALL be ECS Fargate (containerized) rather than a long-lived EC2 fleet, to minimize operational overhead.
4. WHEN deployed THEN the service SHALL be fronted by an Application Load Balancer with health checks against `GET /health`.
5. WHEN a request fails health checks THEN the ALB SHALL drain and replace the task automatically.
6. WHEN the deployment runs THEN it SHALL be driven by Apollo with at least a Beta stage. Prod stage is a follow-up before company-wide rollout.

## Requirement 4 — Export Endpoints

**As a** Harmony frontend
**I want** the Export buttons (HTML, JSON, Word) to download formatted reports for a given analysis
**So that** users can save and share results outside the Harmony UI.

### Acceptance Criteria

1. WHEN `GET /api/report/{analysis_id}/json` is called THEN the response SHALL be the wire-format JSON for that analysis with `Content-Type: application/json`.
2. WHEN `GET /api/report/{analysis_id}/html` is called THEN the response SHALL be a styled HTML report with severity color coding and `Content-Type: text/html`.
3. WHEN `GET /api/report/{analysis_id}/docx` is called THEN the response SHALL be a Word document with the docx MIME type and a `Content-Disposition: attachment` header.
4. WHEN an analysis is run THEN its wire-format response SHALL be persisted server-side (initially in memory, with TTL) so export endpoints can retrieve it by `analysis_id`.
5. WHEN an `analysis_id` is not found or has expired THEN export endpoints SHALL return HTTP 404 with a JSON error body.

## Requirement 5 — Frontend Wire-Up

**As a** PDE engineer using the prototype
**I want** the Harmony frontend to call the real backend instead of mocked data
**So that** clicking Run Analysis produces a real DFM result.

### Acceptance Criteria

1. WHEN the Harmony frontend is deployed THEN it SHALL read the backend base URL from an environment variable (e.g., `VITE_API_BASE_URL`).
2. WHEN the user clicks Run Analysis THEN the frontend SHALL POST to `${VITE_API_BASE_URL}/api/analyze`.
3. WHEN the backend responds with the wire format THEN the frontend SHALL render summary cards, severity-coded findings, filter chips, and export buttons populated from the response.
4. WHEN the backend responds with an error THEN the frontend SHALL display a non-blocking error message with the response body.
5. WHEN the backend is deployed THEN CORS SHALL allow the Harmony prototype origin (`https://rapid-lion-proto-1a492d63.beta.prototype.amazon.dev`) for the `/api/*` paths.

## Requirement 6 — Auth Bridge

**As a** team responsible for proprietary CAD data
**I want** the backend to accept requests only from Midway-authenticated users
**So that** the analysis service is not anonymously accessible to anyone who learns the URL.

### Acceptance Criteria

1. WHEN the Harmony frontend makes a backend request THEN it SHALL forward the user's Midway token via a request header (e.g., `Authorization: Bearer <token>` or the appropriate Midway-cookie pattern).
2. WHEN the backend receives a request to `/api/*` THEN it SHALL validate the Midway token before invoking analysis.
3. WHEN the token is missing or invalid THEN the backend SHALL return HTTP 401.
4. WHEN the token is valid THEN the validated user identity SHALL be available in the request context for audit logging.
5. WHEN audit logging is in place THEN every successful analysis SHALL log `(timestamp, user, process, material, filename, analysis_id)` for traceability.
