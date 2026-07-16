# DFM Inspector API Contract v1

**Status:** Draft (Task 1.1 of the [`backend-harmony-wireup`](../.kiro/specs/backend-harmony-wireup/) spec)
**Stability:** Subject to change until v1.0. Versioned via `X-API-Version` header.
**Maintainer:** Product Development Engineering / DFM Inspector

## Overview

This document describes the HTTP/JSON contract between the DFM Inspector backend and any client. Today the only client is the Harmony "DFM Suite" frontend at `rapid-lion-proto-1a492d63.beta.prototype.amazon.dev`; later it will be additional Design-for-X modules and integrations.

Design goals:
- **Stable.** Internal analyzer code can evolve without changing the contract.
- **Forward-compatible.** New optional fields can be added without a version bump.
- **Type-safe.** Pydantic models on the backend, TypeScript types on the frontend. Validation runs on every response.

## Versioning

The current canonical paths live under `/api/v1/...`. All v1 responses include `X-API-Version: 1`. Future incompatible changes get a v2 published in parallel at `/api/v2/...`.

The legacy `/api/analyze` (no version prefix) returns the original analyzer dict shape and remains as long as the local HTML UI in `templates/` is in use. It is not part of the v1 contract; new consumers should not target it.

Within a major version, the backend MAY:
- Add new optional response fields.
- Add new severity, process, or material enum values.
- Add new endpoints.

The backend MUST NOT, within a major version:
- Remove or rename existing fields.
- Change a field's type.
- Make an optional field required.

Clients SHOULD ignore unknown fields rather than error on them.

## Authentication

Requests carry a Midway token in the `Authorization` header:

```
Authorization: Bearer <midway-token>
```

The backend validates via NAWS. Invalid or missing tokens return `401`.

> Phase 4 of the spec. Not yet enforced while the contract is being stabilized.

## CORS

| Setting | Value |
|---|---|
| Allowed origins | `https://rapid-lion-proto-1a492d63.beta.prototype.amazon.dev` (additional Harmony stages added as needed) |
| Allowed methods | `GET`, `POST`, `OPTIONS` |
| Allowed headers | `Content-Type`, `Authorization`, `X-Request-Id` |
| Max age | 600 seconds |

## Endpoints

### `POST /api/upload`

Upload a CAD file. Returns an opaque handle for use with `/api/v1/analyze`.

**Request:** `multipart/form-data` with field `file`. Max size 100 MB.

**Response 200**

```json
{
  "success": true,
  "upload_id": "f7a8c391-1b2c-4d5e-9876-abc123def456",
  "filename": "part.step",
  "size_bytes": 1234567
}
```

`upload_id` is a UUIDv4 used as the handle for `/api/v1/analyze`. Uploads are stored on the backend and reaped after one hour of inactivity.

---

### `POST /api/v1/analyze`

Run DFM analysis against an uploaded file.

**Request body**

```json
{
  "upload_id": "f7a8c391-1b2c-4d5e-9876-abc123def456",
  "filename": "part.step",
  "process": "sheet_metal",
  "material": "aluminum"
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `upload_id` | `string (UUIDv4)` | yes | From `POST /api/upload` |
| `filename` | `string` | yes | Used to verify the file is still resolvable |
| `process` | [`ProcessId`](#process-ids) | yes | |
| `material` | [`MaterialId`](#material-ids) | yes | |

**Response 200** — see [`ApiAnalyzeResponse`](#apianalyzeresponse)

**Errors:** see [Error responses](#error-responses).

---

### `GET /api/v1/report/{analysis_id}/json`
### `GET /api/v1/report/{analysis_id}/html`
### `GET /api/v1/report/{analysis_id}/docx`

Download a formatted report for a prior analysis. `analysis_id` is the UUID returned from `/api/v1/analyze`.

| Endpoint | Content-Type | Notes |
|---|---|---|
| `/json` | `application/json` | Same body as the original `/api/v1/analyze` response |
| `/html` | `text/html` | Styled standalone HTML page |
| `/docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | Includes `Content-Disposition: attachment; filename="dfm-report-<id>.docx"` |

**Response 404** when the `analysis_id` is unknown or has expired:

```json
{
  "success": false,
  "error": "Analysis not found or expired",
  "code": "ANALYSIS_NOT_FOUND"
}
```

Analyses are retained one hour after creation; older results require a fresh `/api/v1/analyze` run.

---

### `GET /health`

Liveness probe for the load balancer and ops tooling. No auth required.

**Response 200**

```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime_seconds": 3621
}
```

## Type definitions

The pydantic source of truth lives in `src/api_contract.py` (Task 1.2). The shapes below are TypeScript-style for readability.

### `ApiAnalyzeResponse`

```typescript
{
  success: boolean,
  analysis_id: string,           // UUIDv4 generated server-side
  metadata: Metadata,
  summary: Summary,
  findings: Finding[],
  geometry: Geometry,
  exports: Exports
}
```

### `Metadata`

```typescript
{
  process: string,               // Human-readable, e.g. "Sheet Metal"
  process_id: ProcessId,
  material: string,              // Human-readable, e.g. "Aluminum 6061-T6"
  material_id: MaterialId,
  filename: string,
  analyzed_at: string            // ISO-8601 UTC, e.g. "2026-06-26T14:32:11Z"
}
```

### `Summary`

```typescript
{
  score: number,                 // 0–100, weighted by passed/warnings/critical
  total_rules: number,
  passed: number,
  warnings: number,
  critical: number,
  info: number,
  narrative: string              // One-sentence human summary
}
```

Invariant: `passed + warnings + critical + info === total_rules`. Suggestions are surfaced as findings but do not count toward `total_rules`.

### `Finding`

```typescript
{
  id: string,                    // Unique within this response, e.g. "f-001"
  rule_id: string,               // Stable across responses, e.g. "sheet_metal.material_thickness"
  rule_name: string,
  standard: string,              // Source standard, e.g. "930-00172"
  severity: Severity,
  title: string,                 // One-line summary
  description: string,
  recommendation: string,
  rationale: string,
  measured_value: string | null, // Includes units, e.g. "0.30 mm"
  expected_value: string | null, // Includes units, e.g. ">=0.4 mm"
  cost_impact: string | null,
  location: Location | null
}
```

All `*_value` fields are strings (with units) rather than numbers, to give analyzers flexibility for non-numeric results ("multiple holes", "see diagram", etc.).

### `Location`

```typescript
{
  x: number,                     // mm
  y: number,                     // mm
  z: number,                     // mm
  kind: "hole" | "edge" | "face" | "bend" | "corner" | "vertex"
}
```

`location` is `null` when the analyzer can't pin a finding to a specific coordinate. Most findings will have `null` `location` until analyzer-specific coordinate support lands as follow-up work.

### `Geometry`

```typescript
{
  dimensions_mm: Dimensions,
  volume_mm3: number,
  surface_area_mm2: number,
  estimated_min_thickness_mm: number,
  holes_count: number,
  bends_count: number,
  quality_rating: "Excellent" | "Good" | "Fair" | "Poor" | "Unknown"
}
```

### `Dimensions`

```typescript
{
  x: number,                     // mm (bounding-box width)
  y: number,                     // mm (bounding-box depth)
  z: number                      // mm (bounding-box height)
}
```

### `Exports`

```typescript
{
  html: string,                  // e.g. "/api/v1/report/<id>/html"
  json: string,
  docx: string
}
```

URLs are relative paths. Clients prepend their configured backend base URL (`VITE_API_BASE_URL` on the Harmony frontend).

## Enums

### `Severity`

| Value | Suggested UI color | Semantic |
|---|---|---|
| `critical` | red | Must fix before manufacturing; rule failed hard |
| `warning` | orange | Risk to cost or yield; should be reviewed |
| `suggestion` | yellow | Optimization opportunity; not blocking |
| `passed` | green | Rule satisfied; no action needed |
| `info` | gray | Rule not applicable or could not be evaluated |

### `ProcessId`

Maps to the existing `PROCESSES` dict in `app.py`:

| `process_id` | Display name |
|---|---|
| `cnc_machining` | CNC Machining |
| `sheet_metal` | Sheet Metal |
| `injection_molding` | Injection Molding |
| `die_casting` | Die Casting (HPDC) |
| `lpdc` | Low-Pressure Die Casting |
| `permanent_mold` | Permanent Mold Casting |
| `investment_casting` | Investment Casting |
| `mim` | Metal Injection Molding |
| `rotational_molding` | Rotational Molding |
| `wire_forming` | Wire Forming |
| `vacuum_forming` | Vacuum Forming |
| `welding` | Welding |

### `MaterialId`

| `material_id` | Display name |
|---|---|
| `aluminum` | Aluminum 6061-T6 |
| `steel` | Steel (low carbon) |
| `stainless_steel` | Stainless Steel 304 |
| `plastic` | Generic plastic (ABS / PC) |

Additional material IDs may be added in a minor version; clients should accept unknown values gracefully (display the raw ID if no friendly name is known).

## Error responses

All errors follow this shape:

```json
{
  "success": false,
  "error": "Human-readable message",
  "code": "MACHINE_READABLE_CODE",
  "details": { /* optional, context-specific */ }
}
```

| Status | Meaning |
|---|---|
| `400` | Malformed request (missing field, invalid enum value, bad upload ID format) |
| `401` | Missing or invalid Midway token (Phase 4) |
| `404` | Resource not found (e.g. unknown `analysis_id`) |
| `413` | Upload exceeds 100 MB |
| `500` | Internal server error |
| `503` | Backend temporarily unavailable |

Common error codes (non-exhaustive — extend as needed):

| `code` | Typical status | Meaning |
|---|---|---|
| `FILE_MISSING` | 400 | `/api/upload` had no file in the request |
| `INVALID_UPLOAD_ID` | 400 | `upload_id` is not a valid UUIDv4 |
| `INVALID_FILE_PATH` | 400 | Resolved file would escape the upload folder |
| `INVALID_PROCESS` | 400 | `process` is not a recognized `ProcessId` |
| `INVALID_MATERIAL` | 400 | `material` is not a recognized `MaterialId` |
| `UPLOAD_TOO_LARGE` | 413 | File exceeds 100 MB |
| `ANALYSIS_NOT_FOUND` | 404 | `analysis_id` unknown or expired |
| `ANALYZER_FAILED` | 500 | Internal analyzer error; details may include process and stack |
| `UNAUTHORIZED` | 401 | Midway token invalid or missing |

## Worked example: sheet-metal analysis

**Step 1 — Upload**

Request:

```
POST /api/upload
Content-Type: multipart/form-data; boundary=----abc
Authorization: Bearer <midway-token>

------abc
Content-Disposition: form-data; name="file"; filename="bracket.step"
Content-Type: application/octet-stream

<binary STEP content>
------abc--
```

Response:

```json
{
  "success": true,
  "upload_id": "f7a8c391-1b2c-4d5e-9876-abc123def456",
  "filename": "bracket.step",
  "size_bytes": 482311
}
```

**Step 2 — Analyze**

Request:

```
POST /api/v1/analyze
Content-Type: application/json
Authorization: Bearer <midway-token>

{
  "upload_id": "f7a8c391-1b2c-4d5e-9876-abc123def456",
  "filename": "bracket.step",
  "process": "sheet_metal",
  "material": "aluminum"
}
```

Response:

```json
{
  "success": true,
  "analysis_id": "a2e9b481-0c3f-4e22-9a85-7c39b1f4a8de",
  "metadata": {
    "process": "Sheet Metal",
    "process_id": "sheet_metal",
    "material": "Aluminum 6061-T6",
    "material_id": "aluminum",
    "filename": "bracket.step",
    "analyzed_at": "2026-06-26T14:32:11Z"
  },
  "summary": {
    "score": 78.5,
    "total_rules": 14,
    "passed": 8,
    "warnings": 4,
    "critical": 2,
    "info": 0,
    "narrative": "Mostly manufacturable; two thickness violations to address before tooling."
  },
  "findings": [
    {
      "id": "f-001",
      "rule_id": "sheet_metal.material_thickness",
      "rule_name": "Material Thickness",
      "standard": "930-00172",
      "severity": "critical",
      "title": "Material thickness 0.30 mm below 0.4 mm minimum",
      "description": "Detected thickness 0.30 mm; below the 0.4 mm minimum needed for reliable forming.",
      "recommendation": "Increase to 0.5 mm minimum for prototype / low-volume.",
      "rationale": "Material under 0.4 mm tears during bending and cannot hold tolerance during handling.",
      "measured_value": "0.30 mm",
      "expected_value": ">=0.4 mm",
      "cost_impact": "+150-200% from specialized micro-forming",
      "location": null
    },
    {
      "id": "f-002",
      "rule_id": "sheet_metal.hole_to_edge",
      "rule_name": "Hole to Edge Distance",
      "standard": "930-00172",
      "severity": "warning",
      "title": "2 holes within 1.2 mm of edge",
      "description": "Edge distance is below 2T; punching may deform the edge.",
      "recommendation": "Move holes to at least 2.0 mm from the part edge.",
      "rationale": "Holes under 2T from an edge curl or tear the edge during punching.",
      "measured_value": "1.20 mm",
      "expected_value": ">=2.0 mm",
      "cost_impact": "+10-20% scrap from edge tearing",
      "location": null
    },
    {
      "id": "f-003",
      "rule_id": "sheet_metal.bend_radius",
      "rule_name": "Bend Radius",
      "standard": "930-00172",
      "severity": "passed",
      "title": "All bends meet minimum 1.0 mm radius",
      "description": "All four detected bends use the 1.0 mm minimum radius for 1.0 mm material.",
      "recommendation": "No changes needed.",
      "rationale": "Bends at 1.0T avoid cracking and excessive springback.",
      "measured_value": "1.00 mm",
      "expected_value": ">=1.0 mm",
      "cost_impact": "Standard tooling cost",
      "location": null
    }
  ],
  "geometry": {
    "dimensions_mm": {"x": 120, "y": 80, "z": 25},
    "volume_mm3": 18500,
    "surface_area_mm2": 14200,
    "estimated_min_thickness_mm": 0.30,
    "holes_count": 6,
    "bends_count": 4,
    "quality_rating": "Good"
  },
  "exports": {
    "html": "/api/v1/report/a2e9b481-0c3f-4e22-9a85-7c39b1f4a8de/html",
    "json": "/api/v1/report/a2e9b481-0c3f-4e22-9a85-7c39b1f4a8de/json",
    "docx": "/api/v1/report/a2e9b481-0c3f-4e22-9a85-7c39b1f4a8de/docx"
  }
}
```

**Step 3 — Export**

```
GET /api/v1/report/a2e9b481-0c3f-4e22-9a85-7c39b1f4a8de/docx
Authorization: Bearer <midway-token>
```

Response: `200 OK`, body is a `.docx` file, headers include `Content-Disposition: attachment; filename="dfm-report-a2e9b481.docx"`.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-06-26 | aleatala | Initial draft (Task 1.1 of backend-harmony-wireup) |
