# Requirements Document

## Introduction

This spec addresses the analyzer findings that are blocking
**CR-27652557 ([DFMAnalyzer] Initial import of DFM Inspector tool)**
from auto-merging. The CR is currently flagged as "Analyzers failed" in the
Code Dashboard, with two failure surfaces:

1. **AutoSDE Code Analysis** — 14 findings ranging from security
   (path traversal, debugger exposure, file collision) to correctness
   (dead code, duplicate definitions, broken keys, wrong raycast
   direction) to maintainability (unbounded cache, file with severe
   syntax corruption).
2. **InclusiveTechScanner** — 1 finding for non-inclusive terminology in
   `test/test_properties_parser.py`.

Additionally, the BEARS build for `DFMAnalyzer-1.0` on `AL2_x86_64` is
**FAILED** with a "cpp error" Point-of-Interest after only 41 seconds.
Local verification has confirmed that `src/process_analyzers.py` is
unparseable (`SyntaxError` at line 42), so this BEARS failure is almost
certainly a package-import-time `SyntaxError` being mis-tagged by BEARS as
a `cpp error`. Fixing `process_analyzers.py` is therefore expected to also
unblock the BEARS analyzer.

The goal of this spec is to land a single coherent CR revision that:

* turns every required CRUX analyzer green;
* preserves existing functionality (no regressions in CNC, sheet-metal,
  casting, injection-molding, welding, or 3D rendering paths);
* introduces only the minimum new structure required to fix the findings
  cleanly (an upload-token model and an LRU-bounded parser cache).

Two of the findings (`app.py` upload collision and `app.py` debug
exposure) are already implemented locally and are listed under
Requirement 1 and Requirement 2 for completeness so we can track them
through the same acceptance gate.

### Priority and Sequencing

Findings are grouped by priority. Higher priority blocks more analyzers,
so later requirements may depend on earlier ones being complete.

* **P0 — Blocks the BEARS build (entire package fails to import):**
  Requirement 11 (`process_analyzers.py` rebuild).
* **P1 — Security and data-integrity in `app.py`:**
  Requirements 1, 2, 3.
* **P2 — Correctness bugs that produce wrong results at runtime:**
  Requirements 4, 5, 6, 7, 8, 9.
* **P3 — Maintainability / dead code / inclusive language:**
  Requirements 10, 12.

### Out of Scope

* Adding new functional features to DFMAnalyzer.
* Re-architecting CadQuery / OpenCascade integration.
* Changing the public Coral/HTTP contract for the three analyze
  endpoints beyond what the security fix requires (the contract change is
  explicit in Requirement 1).
* Investigating reviewer assignment, auto-merge configuration, or the
  Brazil `Config` for `DFMAnalyzer-1.0` (those are tracked separately).

## Glossary

* **Upload token (`upload_id`)** — A server-generated UUID identifying
  the unique subdirectory under `UPLOAD_FOLDER` that holds a single
  uploaded file. Replaces client-supplied `filepath` in JSON payloads.
* **Containment check** — A filesystem-level check that ensures a
  resolved absolute path lies inside an expected root directory, using
  `os.path.realpath` and `startswith(root + os.sep)` to defeat
  prefix-matching attacks.
* **AutoSDE** — Automated CR analyzer that surfaces code-quality and
  security findings during CRUX review.
* **InclusiveTechScanner** — Automated CR analyzer that flags
  non-inclusive terminology.
* **BEARS** — Brazil's build/analysis runner whose results are surfaced
  on CRs as a required analyzer.

## Requirements

### Requirement 1: Secure upload + analyze flow (collision, info leak, path traversal)

**Findings addressed:** AutoSDE #1 (file upload collision), AutoSDE #3
(full filepath returned to client), AutoSDE #5 (path traversal
validation).

**User Story:** As an operator running DFM Inspector, I want the server
to reject any client request that points at an arbitrary filesystem path,
so that an attacker cannot read or process files outside the upload
directory, and so that two concurrent uploads of the same filename cannot
collide.

#### Acceptance Criteria

1. WHEN a client uploads a file via `/api/upload` (or its equivalent)
   THEN the server SHALL save the file into a unique per-upload
   subdirectory under `app.config['UPLOAD_FOLDER']`, named with a freshly
   generated UUID v4.
2. WHEN the upload endpoint responds successfully THEN the JSON SHALL
   contain `success`, `filename`, `upload_id`, and `size`, AND SHALL NOT
   contain the absolute server-side `filepath`.
3. WHEN any analyze endpoint
   (`/api/analyze`, `/api/enhanced-analyze`, `/api/enhanced-dfm-analyze`)
   receives a request body THEN the server SHALL accept `upload_id` and
   `filename` from the client AND SHALL NOT accept `filepath`.
4. WHEN any analyze endpoint resolves the file to operate on THEN it
   SHALL: validate that `upload_id` matches a UUID v4 pattern; apply
   `werkzeug.utils.secure_filename` to the supplied `filename`; build the
   candidate path as `os.path.join(UPLOAD_FOLDER, upload_id,
   secure_filename(filename))`; resolve via `os.path.realpath`; verify
   the resolved path starts with `os.path.realpath(UPLOAD_FOLDER) +
   os.sep`; and verify the file exists.
5. IF any check in criterion 4 fails THEN the endpoint SHALL return
   HTTP 400 with `{"error": "Invalid file path"}` AND SHALL NOT call any
   downstream parser, analyzer, or workflow.
6. WHEN the same path-resolution logic is needed in more than one
   endpoint THEN it SHALL be implemented in a single helper function
   (e.g. `_resolve_upload(upload_id, filename) -> str`) and reused.
7. WHEN any frontend asset in this repository sends an analyze request
   THEN it SHALL send `upload_id` and `filename` rather than `filepath`.

### Requirement 2: Werkzeug debugger never exposed to the network

**Finding addressed:** AutoSDE #2.

**User Story:** As an operator, I want the Flask debugger to be off by
default and inaccessible from the network when on, so that the
application cannot be turned into a remote code execution vector.

#### Acceptance Criteria

1. WHEN `app.py` is run as `__main__` THEN debug mode SHALL be
   controlled by the `FLASK_DEBUG` environment variable AND SHALL default
   to `False` if the variable is unset, empty, or any value other than
   the case-insensitive string `"true"`.
2. IF `FLASK_DEBUG` is `"true"` THEN the application SHALL bind to
   `127.0.0.1` only.
3. IF `FLASK_DEBUG` is anything else THEN the application MAY bind to
   `0.0.0.0`.
4. The status of this requirement is **already implemented** locally;
   the acceptance criteria exist so the analyzer pass can confirm green
   on this finding without further code changes.

### Requirement 3: Bounded parser cache with explicit eviction

**Finding addressed:** AutoSDE #4.

**User Story:** As an operator, I want the in-memory parser cache to
have a fixed upper bound and predictable eviction, so that long-running
web sessions cannot exhaust process memory.

#### Acceptance Criteria

1. WHEN `app.py` initializes THEN it SHALL define a module-level
   `MAX_PARSER_CACHE_SIZE` constant (default `10`).
2. WHEN a parser is cached THEN the cache SHALL behave as an LRU: the
   most recently inserted or accessed entry is at the end, and entries
   are evicted from the front when size exceeds the limit.
3. WHEN a parser is added to the cache and the cache size would exceed
   `MAX_PARSER_CACHE_SIZE` THEN the least-recently-used entry SHALL be
   evicted before insertion.
4. WHEN the Word export endpoint finishes consuming a cached parser
   THEN the corresponding cache entry SHALL be removed.
5. The cache key SHALL remain the resolved server-side filepath; the
   contract with internal callers does not change beyond bounding.

### Requirement 4: Remove unreachable / duplicate code in app.py

**Finding addressed:** AutoSDE #6.

**User Story:** As a maintainer, I want `_analyze_cnc_machining` to
contain a single function body, so that future edits cannot diverge
between two copies and the file is shorter and clearer.

#### Acceptance Criteria

1. WHEN the file is read THEN `_analyze_cnc_machining` SHALL contain
   exactly one function body and end with a single terminal `return`.
2. WHEN the file is read THEN there SHALL be no duplicated docstring or
   logic block following the active `return` of `_analyze_cnc_machining`.
3. The behavior of `/api/analyze` for the CNC machining process SHALL
   be identical to the active (non-duplicate) body before this change.

### Requirement 5: Fix invalid Poly3DCollection.set_lightsource calls

**Finding addressed:** AutoSDE #7.

**User Story:** As a user generating 3D visualizations, I want the
visualization code to run without `AttributeError`, so that any rendering
path actually produces output.

#### Acceptance Criteria

1. WHEN `src/cad_visualizer.py` is read THEN the four
   `poly.set_lightsource(...)` calls (currently at lines 184, 375, 518,
   and 653) SHALL be removed.
2. WHEN any of those rendering paths run THEN they SHALL not raise
   `AttributeError` for `set_lightsource`.
3. WHEN the visualization is generated THEN basic shading SHALL still
   be present (provided by the existing `shade=True` argument).
4. NO new compute-face-colors logic is required for this requirement.

### Requirement 6: Remove duplicate definitions in cadquery_feature_extractor.py

**Findings addressed:** AutoSDE #8 and AutoSDE #9.

**User Story:** As a maintainer, I want each function in
`src/cadquery_feature_extractor.py` to be defined exactly once, so that
import order does not silently determine behavior.

#### Acceptance Criteria

1. WHEN the file is read THEN `_surface_type_name` SHALL be defined
   exactly once, retaining the complete definition (currently at line
   261) and removing the stub (currently at lines 244–248).
2. WHEN the function returning `distances` is read THEN it SHALL
   contain exactly one `return distances` statement; the duplicate
   currently at line 556 SHALL be removed.
3. The behavior visible to callers SHALL be identical to that of the
   complete `_surface_type_name` definition prior to this change.

### Requirement 7: Fix corrupted hole-diameter key in die-casting analyzer

**Finding addressed:** AutoSDE #11.

**User Story:** As a user analyzing die-cast parts, I want the report
output to show real hole diameters instead of zero, so that small-hole
DFM evaluations are accurate.

#### Acceptance Criteria

1. WHEN `src/die_casting_enhanced_v2.py` is read THEN any
   `chr(...)`-constructed key used to look up hole diameter from a hole
   dictionary SHALL be replaced with the literal string `'diameter'`.
2. WHEN a part with small cast holes is analyzed THEN each hole's
   diameter in the rendered evaluation string SHALL be the value stored
   on the hole record (formatted to one decimal place), not `0.0`.

### Requirement 8: Remove duplicate nested Hole dataclass in feature_detector

**Finding addressed:** AutoSDE #12.

**User Story:** As a maintainer, I want `Hole` to be a single top-level
dataclass, so that there is no shadow `Hole.Hole` class that confuses
readers and tooling.

#### Acceptance Criteria

1. WHEN `src/feature_detector.py` is read THEN there SHALL
   be exactly one `@dataclass class Hole(Feature)` definition at module
   scope.
2. The nested duplicate (currently at lines 59–88) SHALL be removed.
3. NO callers SHALL need to be updated, because the nested class is
   never instantiated.

### Requirement 9: Wall-thickness raycast direction is inward

**Finding addressed:** AutoSDE #13.

**User Story:** As a user analyzing wall thickness, I want rays cast
from a face to actually hit the opposing wall, so that thickness
measurements reflect real geometry rather than producing infinity or
"no hit" for convex parts.

#### Acceptance Criteria

1. WHEN `src/geometry_analyzer.py` performs a
   wall-thickness raycast from a face point with outward normal `normal`
   THEN `ray_direction` SHALL be `-normal`.
2. WHEN the same routine sets the ray origin THEN it SHALL offset the
   point inward by a small epsilon
   (`ray_origin = point - normal * 0.001`) to avoid self-intersection.
3. The change SHALL be confined to the affected raycast and SHALL NOT
   alter unrelated rendering or analysis paths.

### Requirement 10: Environment-variable override actually overrides config keys

**Finding addressed:** AutoSDE #10.

**User Story:** As an operator, I want `GEOM_ANALYSIS_*` environment
variables to actually take effect for keys that contain underscores, so
that operational overrides work as documented.

#### Acceptance Criteria

1. WHEN `src/config.py` translates an environment-variable
   name to a config-key path THEN it SHALL use double-underscore (`__`)
   as the section separator and preserve single underscores within key
   names.
2. THEREFORE setting `GEOM_ANALYSIS_PARSER__MAX_FILE_SIZE_MB=42` SHALL
   override `parser.max_file_size_mb`.
3. The function/module docstring and any inline examples SHALL be
   updated to describe the `__` convention with a worked example.
4. The tests in `test/test_config.py` (currently at lines 225 and 240)
   SHALL be updated to assert the corrected mapping (override of
   `parser.max_file_size_mb`), not the previously broken behavior.
5. Pre-existing callers that already use `__` (if any) SHALL continue
   to work; any pre-existing callers that relied on the broken behavior
   SHALL be updated as part of this requirement.

### Requirement 11: Restore process_analyzers.py to a parseable, structured module

**Finding addressed:** AutoSDE #14. Also expected to unblock the BEARS
"cpp error" / Build Failed on the CR.

**User Story:** As a maintainer (and as the BEARS build), I want
`src/process_analyzers.py` to import without error and contain four
self-contained analyzer functions, so that the package builds and each
analyzer is independently maintainable.

#### Acceptance Criteria

1. WHEN `python -m py_compile src/process_analyzers.py` is run THEN it
   SHALL exit with status 0.
2. WHEN the module is imported THEN it SHALL expose four top-level
   callables: `analyze_sheet_metal`, `analyze_injection_molding`,
   `analyze_die_casting`, `analyze_wire_forming`.
3. Each of the four analyzer functions SHALL be self-contained: its
   body SHALL not interleave logic from another analyzer, and SHALL end
   with a single coherent return path.
4. WHEN the same analyzer name appears more than once in the original
   file (e.g. `analyze_injection_molding` at lines 136 and 284) THEN the
   restructured module SHALL contain exactly one definition per name,
   merging the intended logic.
5. Specific corruptions called out by AutoSDE SHALL be resolved:
   `warnings.append((` (lines 39–41) is closed correctly before the
   `# Check part size` block; `analyze_sheet_metal` returns only after
   its full logic completes (no premature return at line 111, no
   closing-braces / new-statements mash-up at line 133); corrupted text
   fragments at lines 668, 672, 694, and 699 are replaced with the
   intended source; the missing `assessment =` assignment around line
   755 is restored.
6. The restructure MAY split `process_analyzers.py` into one module per
   analyzer (e.g. `process_analyzers/sheet_metal.py`) only if downstream
   import sites are updated in the same change; otherwise the single-file
   structure SHALL be kept.
7. Any DFM rule values, thresholds, or assessment strings that are
   recoverable from the surrounding context SHALL be preserved; values
   that cannot be recovered SHALL be flagged in code with a `# TODO`
   comment and a conservative default, and listed in the design
   document.
8. The behavior of `/api/analyze` for sheet-metal, injection-molding,
   die-casting, and wire-forming SHALL not regress on a representative
   STEP file; specifically, status, materials list, and rule violations
   SHALL be produced (even if some specific thresholds are marked
   `# TODO`).

### Requirement 12: Inclusive language in tests and Hypothesis usage

**Finding addressed:** InclusiveTechScanner finding on
`test/test_properties_parser.py`.

**User Story:** As a developer, I want our test code and our use of
third-party APIs to use inclusive terminology, so that the
InclusiveTechScanner analyzer can pass and our codebase aligns with
Amazon's inclusive-language guidance.

#### Acceptance Criteria

1. WHEN any file in this repository is read THEN it SHALL NOT contain
   the terms `blacklist`, `whitelist`, `master`/`slave`, `whiteday(s)`,
   or `blackday(s)` in our own identifiers, comments, strings, or
   documentation. Approved replacements: `denylist` / `blocklist`,
   `allowlist`, `primary` / `replica`, `clear day(s)`, `blocked day(s)`.
2. WHEN `test/test_properties_parser.py` calls
   `hypothesis.strategies.characters` THEN it SHALL pass categories using
   the modern `categories` / `exclude_categories` keyword arguments, not
   `whitelist_categories` / `blacklist_categories`.
3. IF the currently pinned Hypothesis version does not support
   `exclude_categories` THEN `requirements.txt` (or the equivalent
   dependency manifest) SHALL be updated to a Hypothesis version that
   does, and the change noted in the task that performs the update.
4. The InclusiveTechScanner finding SHALL not return on the next
   analyzer pass.

### Requirement 13: Cross-cutting acceptance

**User Story:** As a reviewer of CR-27652557, I want a single check at
the end of the work that confirms all analyzers are green, so that I do
not have to re-derive whether earlier requirements were genuinely
satisfied.

#### Acceptance Criteria

1. `python -m py_compile` SHALL succeed for every `.py` file under the
   package source tree.
2. Re-running the CR analyzers SHALL produce zero AutoSDE findings and
   zero InclusiveTechScanner findings on the changed files.
3. The BEARS build for `DFMAnalyzer-1.0` on `AL2_x86_64` SHALL succeed,
   or, if it still fails, the failure SHALL be unrelated to
   `process_analyzers.py` parse errors and SHALL be tracked as a new
   item.
4. The CR's "Merge blockers: 4 required analyzers" indicator SHALL
   resolve to zero.
