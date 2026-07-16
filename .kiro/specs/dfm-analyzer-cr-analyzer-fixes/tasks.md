# Implementation Plan: DFM Analyzer CR Analyzer Fixes

## Overview

Convert the feature design into a series of prompts for a code-generation LLM
that will implement each step with incremental progress. Make sure that each
prompt builds on the previous prompts, and ends with wiring things together.
There should be no hanging or orphaned code that isn't integrated into a
previous step. Focus ONLY on tasks that involve writing, modifying, or
testing code.

This plan implements CR-27652557 analyzer fixes in the **P0 → P3** order
prescribed by the design's "Sequencing" section: rebuild `process_analyzers.py`
first (it blocks BEARS), then land independent correctness fixes, then the
config-separator change, then the larger `app.py` structural changes (upload
token + LRU cache), and finally the inclusive-language one-liner and the
cross-cutting acceptance gate.

The design explicitly omits a "Correctness Properties" section
(see Testing Strategy in `design.md`); these tasks therefore use unit and
integration tests rather than property-based tests, with each test sub-task
marked optional (`*`).

## Tasks

- [x] 1. P0 — Rebuild `src/process_analyzers.py` so the package imports
  - [x] 1.1 Recover or reconstruct the four analyzer functions in a single file
    - Pull the last unbroken version from git history if available
      (`git -P log -- src/process_analyzers.py`); otherwise treat the current
      file as a text spec and unscramble the four interleaved bodies per
      `design.md` § Components and Interfaces / 10. Restoring `src/process_analyzers.py`
    - Define exactly four top-level callables with these signatures:
      `analyze_sheet_metal(parser, material, geometry) -> Dict`,
      `analyze_injection_molding(parser, material, geometry) -> Dict`,
      `analyze_die_casting(parser, material, geometry) -> Dict`,
      `analyze_wire_forming(parser, material, geometry) -> Dict`
    - Each function returns a dict with the standard keys (`success`, `process`,
      `material`, `score`, `score_explanation`, `issues`, `warnings`,
      `suggestions`, `passed`, `geometry_info`, `rationale`, `summary`,
      `details`); `analyze_sheet_metal` additionally returns `all_rules`
    - Preserve all recoverable threshold values verbatim (sheet-metal 0.5/0.9 mm
      thickness gates, 1.5×T bend radius, 4×T+R flange, 2×T+R hole-to-edge,
      1500/2500 mm part-size gates, 6061-T6 vs 5052-H32 messaging, standard
      punch sizes 3.2/6.4/9.5/12.7; injection-molding 0.5/0.75/4/6 mm wall
      gates, 1–3° draft, 60%-of-wall ribs, 0.5×T corner radii, ABS/PC/PP
      messaging; die-casting 0.75/6 mm wall gates, draft, A380/Zamak
      messaging; wire-forming 0.5/1/12 mm diameter gates, 3×D bend radius and
      leg length, 4×D bend spacing, springback table) — see `design.md` step 4
    - Mark every threshold that cannot be recovered with
      `# TODO(CR-27652557): recover original threshold` and use a conservative
      default (assessment ladder cutoffs default to 90/75/60 to match
      `die_casting_enhanced_v2.py` and `cnc_machining_enhanced.py`)
    - Keep the module as a single file (do not split into a package); see
      `design.md` step 3
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7_

  - [x] 1.2 Add stub callables for the four out-of-scope analyzer names
    - Define `analyze_investment_casting`, `analyze_mim`,
      `analyze_rotational_molding`, and `analyze_vacuum_forming` as top-level
      functions in `src/process_analyzers.py` so `app.py`'s lazy imports
      succeed at request time
    - Each stub returns the standard dict shape with `success: False` and a
      "process not yet implemented" rationale (no exceptions raised)
    - _Requirements: 11.2, 11.8_

  - [ ]* 1.3 Write contract test for `process_analyzers` imports and shapes
    - New file `tests/test_process_analyzers.py`
    - Assert `python -m py_compile src/process_analyzers.py` exits 0
      (drive via `py_compile.compile`)
    - Assert all four required analyzers and the four stubs are importable
      from `src.process_analyzers`
    - Smoke-call each of the four required analyzers with a representative
      parser/geometry dict; assert the returned dict contains the standard
      keys (`success`, `process`, `material`, `score`, `summary`, `details`)
    - _Requirements: 11.1, 11.2, 11.3, 11.8_

- [x] 2. P0 Checkpoint — confirm BEARS-blocker is resolved
  - Ensure all tests pass, ask the user if questions arise.

- [x] 3. P2 — Correctness and dead-code fixes (independent, parallelizable)
  - [x] 3.1 Remove duplicate `_analyze_cnc_machining` body in `app.py`
    - Locate the duplicated function body (~lines 1100–1200; see
      `design.md` § Components and Interfaces / 3. Dead-code removal)
    - Delete the second copy plus the orphaned docstring; keep the body
      ending with the authoritative terminal `return`
    - Verify `python -m py_compile app.py` exits 0
    - _Requirements: 4.1, 4.2, 4.3_

  - [x] 3.2 Remove `Poly3DCollection.set_lightsource` calls in `cad_visualizer.py`
    - Delete the four `poly.set_lightsource(...)` calls in
      `src/cad_visualizer.py` at the call sites listed in `design.md` § 4
      (`render_with_highlighted_holes`, `render_with_highlighted_features`,
      the `render_violations_multiview` paths, `render_with_violations`;
      currently lines 184, 375, 518, 653)
    - Keep the existing `Poly3DCollection(..., shade=True)` arguments so basic
      shading is preserved
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 3.3 Deduplicate `_surface_type_name` and trailing `return distances`
    - In `src/cadquery_feature_extractor.py`, delete the stub
      `_surface_type_name` at lines 244–248 and keep the complete definition
      at line 261
    - In `_calc_hole_to_face_edge_distances`, delete the second
      `return distances` (currently line 556) so exactly one terminal return
      remains
    - See `design.md` § 5. CadQuery dedup
    - _Requirements: 6.1, 6.2, 6.3_

  - [x] 3.4 Fix corrupted `'diameter'` key in `die_casting_enhanced_v2.py`
    - Replace the `chr(...)`-built key (which currently resolves to the
      eight-character literal `'"diameter"'`) with the literal string
      `'diameter'` on the hole-record lookup
    - See `design.md` § 6. `'diameter'` key
    - _Requirements: 7.1, 7.2_

  - [x] 3.5 Remove nested `Hole` dataclass in `feature_detector.py`
    - Delete the nested `@dataclass class Hole(Feature):` block (currently
      lines 59–88) inside the top-level `Hole` class
    - Keep exactly one `@dataclass class Hole(Feature)` definition at module
      scope; no callers change
    - _Requirements: 8.1, 8.2, 8.3_

  - [x] 3.6 Flip wall-thickness raycast direction inward in `geometry_analyzer.py`
    - In `measure_wall_thickness`, change `ray_origin = point + normal * 0.001`
      to `ray_origin = point - normal * 0.001` and change
      `ray_direction = normal` to `ray_direction = -normal`
    - Confine the change to that single raycast; do not touch other rays in
      the file (which already use the correct direction)
    - See `design.md` § 8. Wall-thickness raycast direction
    - _Requirements: 9.1, 9.2, 9.3_

  - [ ]* 3.7 Write unit test for `'diameter'` key fix
    - New test in `tests/test_die_casting_enhanced_v2.py` (or extend an
      existing one)
    - Call `analyze_die_casting_enhanced_v2` with a hole record carrying a
      known diameter; assert the rendered `evaluation` string contains the
      actual diameter to one decimal place (and is not `0.0`)
    - _Requirements: 7.2_

  - [ ]* 3.8 Write regression test for nested-Hole removal
    - New test or assertion in `tests/test_feature_detector.py`
    - Assert `not hasattr(Hole, 'Hole')` after import from
      `src.feature_detector`
    - _Requirements: 8.1, 8.2_

  - [ ]* 3.9 Write regression test for wall-thickness raycast direction
    - New test in `tests/test_geometry_analyzer.py` using a thin-walled cube
      mesh fixture
    - Assert `measure_wall_thickness` returns the cube's wall thickness
      within ±0.05 mm (would return ~0/no-hit before the fix)
    - _Requirements: 9.1, 9.2_

- [x] 4. P2 Checkpoint — confirm correctness and dead-code fixes are clean
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. P3 — Environment-variable separator change
  - [x] 5.1 Update `_apply_env_overrides` in `src/config.py` to use `__` separator
    - Change the env-key-to-dotted-key translation so only `__` becomes `.`
      and single underscores within key names are preserved (per
      `design.md` § 9. Env-var separator)
    - Example resolution: `GEOM_ANALYSIS_PARSER__MAX_FILE_SIZE_MB=42` →
      `parser.max_file_size_mb`
    - Update the function/module docstring to describe the `__` convention
      with the worked-example table from `design.md` § 9
    - _Requirements: 10.1, 10.2, 10.3, 10.5_

  - [x] 5.2 Update `tests/test_config.py` to assert the corrected mapping
    - Edit `test_env_override_applied` and `test_env_override_boolean`
      (currently at lines 225 and 240) so they set
      `GEOM_ANALYSIS_PARSER__MAX_FILE_SIZE_MB=200` and
      `GEOM_ANALYSIS_PARSER__FALLBACK_ENABLED` and assert against
      `parser.max_file_size_mb` / `parser.fallback_enabled`
    - Both updated tests must pass against the change in 5.1
    - _Requirements: 10.4_

- [ ] 6. P1 — `app.py` structural changes (upload token + LRU cache)
  - [x] 6.1 Add `_resolve_upload(upload_id, filename) -> str` helper and `_UUID4_RE`
    - In `app.py`, define the module-level UUID-v4 regex
      (`^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$`)
      and the `_resolve_upload` helper exactly as specified in
      `design.md` § Components and Interfaces / 1. Upload helper
    - The helper raises `ValueError` on any of: bad UUID, empty
      `secure_filename`, containment failure (using
      `os.path.realpath` and `startswith(real_root + os.sep)`), or missing
      file
    - _Requirements: 1.4, 1.5, 1.6_

  - [x] 6.2 Replace `filepath` with `upload_id` + `filename` in the three analyze endpoints
    - Update `/api/analyze`, `/api/enhanced-analyze`, and
      `/api/enhanced-dfm-analyze` so each endpoint's first three lines call
      `_resolve_upload(data.get('upload_id'), data.get('filename'))` inside a
      `try/except ValueError` and return HTTP 400 with
      `{"error": "Invalid file path"}` on failure (no parser, analyzer, or
      workflow is invoked on failure)
    - The resolved `filepath` then flows into the existing parsing code
      unchanged
    - _Requirements: 1.3, 1.4, 1.5, 1.6_

  - [x] 6.3 Update `/api/upload` response shape to drop `filepath` and add `upload_id`
    - The endpoint already saves into `UPLOAD_FOLDER/<uuid>/<secure_filename>`
      per `design.md` § 1
    - Change the success JSON from
      `{success, filename, filepath, size}` to
      `{success, filename, upload_id, size}`; do not return the absolute
      server-side path
    - _Requirements: 1.1, 1.2_

  - [x] 6.4 Update frontend payloads in `templates/interface.html` (and `enhanced_test.html`)
    - Change every `fetch` payload that targets the three analyze endpoints
      so it sends `upload_id` + `filename` instead of `filepath`
    - Read the `upload_id` returned by `/api/upload` and store it for the
      subsequent analyze call; do not display or rely on a server-side path
    - _Requirements: 1.7_

  - [x] 6.5 Replace unbounded `_parser_cache` dict with `OrderedDict`-backed LRU
    - In `app.py`, define `MAX_PARSER_CACHE_SIZE = 10` and replace the
      `_parser_cache` dict with `OrderedDict[str, object]`
    - Add `_cache_put(filepath, parser)`, `_cache_get(filepath)`, and
      `_cache_pop(filepath)` helpers exactly as specified in
      `design.md` § 2. LRU-bounded parser cache
    - Replace each existing `_parser_cache[filepath] = parser` insertion in
      the three analyze endpoints with `_cache_put(filepath, parser)`
    - In `/api/word-export`, replace the lookup with `_cache_get(...)` and
      replace the post-export "leave-in-cache" path with `_cache_pop(...)`
      so the parser entry is removed after consumption
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x] 6.6 Verify `FLASK_DEBUG` parsing path is unchanged in `__main__`
    - Read `app.py`'s `__main__` block; confirm debug mode is gated by
      `os.environ.get('FLASK_DEBUG')` matching `"true"` case-insensitively
      and defaults to `False` for unset/empty/anything-else, and that
      `app.run` binds to `127.0.0.1` only when debug is on
    - This requirement is "already implemented" per `design.md`; if the
      check reveals a regression, restore the documented behaviour
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [ ]* 6.7 Write unit tests for `_resolve_upload` failure modes
    - New file `tests/test_app_upload.py`
    - Cover each failure mode separately: bad/missing UUID, empty
      `secure_filename`, traversal (`../`-laden filename), escaped
      containment (symlink or directory traversal that resolves outside
      `UPLOAD_FOLDER`), missing file
    - Assert each returns HTTP 400 with the canonical
      `{"error": "Invalid file path"}` body and that no parser/analyzer is
      invoked
    - Add a happy-path test: upload a fixture, then call an analyze endpoint
      with the returned `upload_id` and `filename`; assert 200
    - _Requirements: 1.4, 1.5, 1.6_

  - [ ]* 6.8 Write unit tests for the LRU parser cache helpers
    - New file `tests/test_app_cache.py`
    - `_cache_put` with 11 distinct keys evicts the first inserted (LRU front)
    - `_cache_get` on an existing key reorders it to the end (most-recent)
    - `_cache_put` on an existing key updates value and moves to end
    - `_cache_pop` removes the entry and returns it; second pop returns None
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 7. P1 Checkpoint — confirm app.py structural changes are clean
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. P3 — Inclusive language Hypothesis swap
  - [x] 8.1 Replace `blacklist_categories` with `exclude_categories` in `tests/test_properties_parser.py`
    - Swap the kwarg in the single occurrence of
      `st.characters(blacklist_categories=('Cs',))` to
      `st.characters(exclude_categories=('Cs',))`
    - The repo contains exactly one occurrence; no other inclusive-language
      remediation is in scope (`design.md` § 11)
    - `requirements.txt` already pins `hypothesis>=6.0.0`, which supports
      `exclude_categories`; do not change the manifest unless 8.2 reveals an
      incompatibility
    - _Requirements: 12.1, 12.2_

  - [x] 8.2 Verify `tests/test_properties_parser.py` runs to completion
    - Run the file under the existing test runner; if Hypothesis rejects
      `exclude_categories` at the pinned version, bump `requirements.txt` to
      a version that supports it (≥ 6.18) and note the bump in this task's
      commit message
    - _Requirements: 12.3, 12.4_

- [x] 9. Cross-cutting acceptance gate
  - [x] 9.1 Run `py_compile` over the package source tree
    - Execute `python -m py_compile` against every `.py` file in the package
      source tree (driven by `git ls-files '*.py'` or equivalent) and assert
      exit status 0
    - Add this command (or its test wrapper) to a CI gate script if one
      exists; otherwise capture it in `tests/test_packaging.py` as a
      single test that walks the source tree
    - _Requirements: 13.1_

  - [ ]* 9.2 Write integration test wiring upload → analyze for one process
    - New test in `tests/test_app_upload.py` (or `tests/test_integration.py`)
    - Use a small STEP fixture; POST to `/api/upload`, capture `upload_id`,
      then POST to `/api/analyze` with `process: "cnc_machining"` and the
      returned `upload_id`/`filename`; assert 200 and a non-error response
    - This validates that Requirement 1, Requirement 3, Requirement 4, and
      the rebuilt `process_analyzers.py` (Requirement 11) work together end
      to end via the test harness (no running of the live app)
    - _Requirements: 1.3, 1.7, 3.5, 4.3, 11.8, 13.4_

- [x] 10. Final checkpoint — confirm CR analyzers will go green
  - Ensure all tests pass, ask the user if questions arise.
  - _Requirements: 13.1, 13.2, 13.3, 13.4_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP.
  All optional tasks here are tests, consistent with the spec workflow.
- Each task references specific sub-requirements from `requirements.md` and
  the relevant section of `design.md`.
- Sequencing follows the **P0 → P3** plan in `requirements.md` § Priority
  and Sequencing and the explicit ordering in `design.md` § Sequencing:
  rebuild `process_analyzers.py` first (1) → independent correctness fixes
  (3) → env-var separator (5) → app.py structural changes (6) → inclusive
  language (8) → cross-cutting acceptance (9).
- Property-based tests are intentionally **not** included: the design's
  Testing Strategy explicitly omits Correctness Properties because the work
  is defensive remediation (deletions, security helper, LRU cache, module
  rebuild) and is better covered by unit and contract tests.
- Checkpoints (tasks 2, 4, 7, 10) mark intermediate states that must remain
  buildable and reviewable per `design.md` § Sequencing, and they map to
  CR-revision boundaries.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "1.3"] },
    { "id": 2, "tasks": ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6"] },
    { "id": 3, "tasks": ["3.7", "3.8", "3.9", "5.1"] },
    { "id": 4, "tasks": ["5.2", "6.1", "6.6"] },
    { "id": 5, "tasks": ["6.2", "6.3", "6.5"] },
    { "id": 6, "tasks": ["6.4", "6.7", "6.8", "8.1"] },
    { "id": 7, "tasks": ["8.2", "9.1"] },
    { "id": 8, "tasks": ["9.2"] }
  ]
}
```
