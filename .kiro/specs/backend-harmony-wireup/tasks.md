# Implementation Plan: Backend Harmony Wire-Up

## Overview

This plan wires the Harmony frontend to the real DFM Inspector backend in six phases, ordered P0 -> P4. Each phase has a checkpoint that confirms the prior work before later phases land. Phases 1-3 (P0-P2) can be done locally without AWS access; Phase 4 (P1 hosting) is the blocker for everything user-facing after that.

## Tasks

- [ ] 1. P0 -- Contract and pydantic models
  - [x] 1.1 Author `docs/api-contract.md` describing every field, type, allowed values, and a worked example for sheet metal.
  - [x] 1.2 Add `src/api_contract.py` with pydantic models: `Finding`, `Summary`, `Metadata`, `Geometry`, `Exports`, `ApiAnalyzeResponse`, `AnalyzeRequest`.
  - [ ] 1.3 * Tests: pydantic models reject invalid severities, missing required fields, malformed timestamps.
  - [ ] 1.4 Verify the contract matches what the Harmony agent generated for the frontend (any mismatches -> adjust contract or note for frontend update).

- [x] 2. P0 -- Transformation layer
  - [x] 2.1 Add `src/api_transform.py` exposing `to_api_response(internal_result, request_metadata)` returning a validated `ApiAnalyzeResponse`.
  - [x] 2.2 Implement severity mapping per the design's mapping table.
  - [x] 2.3 Implement deduplication keyed on `(rule_name, severity)` preferring `all_rules`.
  - [x] 2.4 Implement `location: null` default; document how analyzers will later supply coords.
  - [x] 2.5 Wire `/api/analyze` in `app.py` to apply `to_api_response` before `jsonify`.
  - [ ] 2.6 * Tests: each severity mapping, dedup behaviour, missing-field tolerance, no-mutation guarantee.
  - [x] 2.7 Smoke-test locally: upload a sample STEP, run analysis, confirm response shape validates against pydantic.

- [x] 3. P0 -- Checkpoint
  - [x] 3.1 All local analyzers (sheet metal, CNC, injection molding, die casting, welding) produce contract-valid responses against the fixtures in `sample_files/`.

- [ ] 4. P1 -- Backend hosting (Apollo + ECS Fargate)
  - [ ] 4.1 Brazilify the backend as a standalone Brazil package. Reuse the Dockerfile from commit `a608615 feat(deploy): containerize app for AWS App Runner deployment` as the base.
  - [ ] 4.2 Wire `brazil-build release` to produce a publishable container image.
  - [ ] 4.3 Push image to team ECR repository.
  - [ ] 4.4 Define Apollo environment with a Beta stage. Owner bindle: `Prod-Dev-Eng`.
  - [ ] 4.5 Provision ECS Fargate task definition (2 vCPU, 4 GB memory baseline).
  - [ ] 4.6 Provision internal ALB with `/health` health check; register the Fargate service as the target.
  - [ ] 4.7 Register internal DNS (CNAME `dfm-inspector-api.<team-domain>` -> ALB).
  - [ ] 4.8 First successful deploy to Beta; confirm `GET /health` returns 200 over HTTPS.

- [ ] 5. P2 -- Export endpoints
  - [ ] 5.1 Add an in-memory analysis result store (LRU + TTL) keyed by `analysis_id`.
  - [ ] 5.2 Add `GET /api/report/<id>/json` returning the wire-format response.
  - [ ] 5.3 Add `GET /api/report/<id>/html` returning a styled HTML report.
  - [ ] 5.4 Add `GET /api/report/<id>/docx` returning a Word file with `Content-Disposition: attachment`.
  - [ ] 5.5 * Tests: 404 for unknown id, correct content-type and headers, correct content for each format.

- [ ] 6. P3 -- Frontend wire-up
  - [ ] 6.1 Add `VITE_API_BASE_URL` environment variable to the Harmony app; set the Beta value to the new backend URL.
  - [ ] 6.2 Replace the mock `/api/analyze` call in the frontend with a real fetch against `${VITE_API_BASE_URL}/api/analyze`.
  - [ ] 6.3 Render the wire-format response into summary cards, findings list, filter chips, and export links.
  - [ ] 6.4 Enable CORS on the backend for the prototype origin under `/api/*`.
  - [ ] 6.5 End-to-end smoke test: upload a sample STEP through the prototype URL, see real findings render.

- [ ] 7. P4 -- Auth bridge
  - [ ] 7.1 Confirm the Midway-validation library used by the team (likely the same as `ApolloDashboard`).
  - [ ] 7.2 Frontend forwards the Midway token in the `Authorization` header on every `/api/*` request.
  - [ ] 7.3 Backend `@require_midway` decorator validates the token, sets `g.user`, and returns 401 on failure.
  - [ ] 7.4 Audit log: `(timestamp, user, process, material, filename, analysis_id, duration_ms)` on every successful analysis.
  - [ ] 7.5 End-to-end test with a Midway-authenticated browser session.

- [ ] 8. Final checkpoint
  - [ ] 8.1 25-engineer cohort can run real analyses end-to-end on the Beta URL with their own STEP files.
  - [ ] 8.2 Audit log shows all expected fields for each run.
  - [ ] 8.3 No PII or proprietary CAD data is logged beyond filenames.

## Notes

* Tasks marked `*` are optional and primarily add test coverage. Per the project default, tests are not auto-added unless explicitly requested. Mark these `[x]` only if you actually do the work; otherwise leave `[ ]*`.
* Phases 1-3 (P0-P2) can largely be done locally without AWS access. Phase 4 (P1 hosting) is the critical blocker for everything user-facing after that.
* Phase 6 frontend updates require the Harmony AgentSpace; coordinate timing with the prototype 30-day TTL.
