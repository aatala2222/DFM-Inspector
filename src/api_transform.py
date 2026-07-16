"""
Transformation layer: internal analyzer dict -> API wire format.

Source of truth for the wire format: docs/api-contract.md and src/api_contract.py.
Spec: .kiro/specs/backend-harmony-wireup/

The DFM analyzers (sheet_metal_enhanced, cnc_machining_enhanced, etc.) return
heterogeneous dicts that have grown organically. This module is the single
place that maps those dicts to the stable API contract. The internal shapes
can keep evolving; the wire format stays put.

Internal shape (observed across analyzers, abridged):

    {
        'success': True,
        'process': 'Sheet Metal',
        'material': 'aluminum',
        'score': 78.5,
        'issues':      <int count>,
        'warnings':    <int count>,
        'suggestions': <int count>,
        'passed':      <int count>,
        'all_rules': [
            {'name': str, 'standard': str, 'status': 'PASS|WARNING|FAIL|INFO',
             'measured_value': str, 'evaluation': str, 'recommendation': str,
             'rationale': str, 'cost_impact': str},
            ...
        ],
        'geometry': {'dimensions': {x, y, z}, 'volume': float, ...},
        'geometry_info': {'dimensions': '...', 'volume': '...', ...},
        'details': {
            'cost_savings': [<suggestion dicts>],
            ...
        },
        ...
    }

Usage:

    from src.api_contract import AnalyzeRequestMetadata
    from src.api_transform import to_api_response

    metadata = AnalyzeRequestMetadata(
        filename='bracket.step',
        process_id=ProcessId.SHEET_METAL,
        process_display='Sheet Metal',
        material_id=MaterialId.ALUMINUM,
        material_display='Aluminum 6061-T6',
    )
    response = to_api_response(internal_result, metadata)
    return jsonify(response.to_wire())
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4

from src.api_contract import (
    AnalyzeRequestMetadata,
    ApiAnalyzeResponse,
    Dimensions,
    Exports,
    Finding,
    Geometry,
    Location,
    Metadata,
    QualityRating,
    Severity,
    Summary,
)


# ---------------------------------------------------------------------------
# Status -> Severity mapping
# ---------------------------------------------------------------------------

_STATUS_TO_SEVERITY: dict[str, Severity] = {
    "FAIL": Severity.CRITICAL,
    "WARNING": Severity.WARNING,
    "PASS": Severity.PASSED,
    "INFO": Severity.INFO,
}


def _status_to_severity(status: str | None) -> Severity:
    """Map an internal rule status to a wire-format severity.

    Unknown or missing statuses default to INFO so analyses don't fail
    hard on quirky analyzer output; we'd rather surface a degraded finding
    than 500 the whole request.
    """
    if status is None:
        return Severity.INFO
    return _STATUS_TO_SEVERITY.get(status.upper(), Severity.INFO)


# ---------------------------------------------------------------------------
# Rule-id synthesis
# ---------------------------------------------------------------------------

_RULE_ID_STRIP = re.compile(r"[^a-z0-9]+")


def _synthesize_rule_id(process_id: str, rule_name: str) -> str:
    """Build a stable, machine-readable rule id from a human rule name.

    "Material Thickness" + "sheet_metal" -> "sheet_metal.material_thickness"

    Stability matters: the frontend may use rule_id as a key for opening
    rule-specific deep links or attaching user notes, so the same human
    name should always map to the same id.
    """
    snake = _RULE_ID_STRIP.sub("_", (rule_name or "unnamed").strip().lower()).strip("_")
    return f"{process_id}.{snake or 'unnamed'}"


# ---------------------------------------------------------------------------
# Title shortening
# ---------------------------------------------------------------------------

_TITLE_MAX_CHARS = 140


def _truncate(text: str, limit: int = _TITLE_MAX_CHARS) -> str:
    """Trim a sentence to one display line without cutting mid-word."""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text.rfind(" ", 0, limit - 1)
    if cut < limit // 2:
        cut = limit - 1
    return text[:cut].rstrip(",.;: ") + "..."


# ---------------------------------------------------------------------------
# Quality rating from score
# ---------------------------------------------------------------------------

def _quality_rating(score: float | None) -> QualityRating:
    """Bucket the 0-100 score into a coarse rating.

    Thresholds chosen to roughly match how the analyzers describe parts in
    their summary narratives. Tunable; not load-bearing.
    """
    if score is None:
        return QualityRating.UNKNOWN
    if score >= 85:
        return QualityRating.EXCELLENT
    if score >= 70:
        return QualityRating.GOOD
    if score >= 50:
        return QualityRating.FAIR
    if score >= 0:
        return QualityRating.POOR
    return QualityRating.UNKNOWN


# ---------------------------------------------------------------------------
# Builders for each wire-format block
# ---------------------------------------------------------------------------

def _build_metadata(
    request_metadata: AnalyzeRequestMetadata,
    analyzed_at: datetime,
) -> Metadata:
    return Metadata(
        process=request_metadata.process_display,
        process_id=request_metadata.process_id,
        material=request_metadata.material_display,
        material_id=request_metadata.material_id,
        filename=request_metadata.filename,
        analyzed_at=analyzed_at,
    )


def _build_findings(
    internal: Mapping[str, Any],
    process_id: str,
) -> list[Finding]:
    """Convert internal all_rules + suggestions into a flat wire-format list.

    The dedup contract: when both ``all_rules`` and one of the legacy
    ``details.*`` arrays mention the same rule_name with the same severity,
    we keep the ``all_rules`` entry because it carries the richer payload.
    """
    findings: list[Finding] = []
    seen: set[tuple[str, Severity]] = set()
    counter = 0

    # 1) Primary source: all_rules
    for rule in internal.get("all_rules") or []:
        if not isinstance(rule, Mapping):
            continue
        severity = _status_to_severity(rule.get("status"))
        rule_name = str(rule.get("name") or "Unnamed Rule")
        key = (rule_name, severity)
        if key in seen:
            continue
        seen.add(key)
        counter += 1

        evaluation = str(rule.get("evaluation") or "")
        findings.append(
            Finding(
                id=f"f-{counter:03d}",
                rule_id=_synthesize_rule_id(process_id, rule_name),
                rule_name=rule_name,
                standard=str(rule.get("standard") or ""),
                severity=severity,
                title=_truncate(evaluation) or rule_name,
                description=evaluation,
                recommendation=str(rule.get("recommendation") or ""),
                rationale=str(rule.get("rationale") or ""),
                measured_value=rule.get("measured_value") or None,
                expected_value=None,  # analyzers don't emit a discrete field today
                cost_impact=rule.get("cost_impact") or None,
                location=None,  # analyzers don't supply (x,y,z) yet
            )
        )

    # 2) Suggestions: appended as the SUGGESTION severity.
    # Suggestions live separately in details.cost_savings and aren't tracked
    # in all_rules. They're optional optimization hints, distinct from
    # rule pass/fail evaluations.
    details = internal.get("details") or {}
    for sugg in (details.get("cost_savings") or []):
        if not isinstance(sugg, Mapping):
            continue
        rule_name = str(
            sugg.get("opportunity") or sugg.get("category") or "Optimization"
        )
        key = (rule_name, Severity.SUGGESTION)
        if key in seen:
            continue
        seen.add(key)
        counter += 1

        body = str(sugg.get("message") or sugg.get("description") or "")
        findings.append(
            Finding(
                id=f"f-{counter:03d}",
                rule_id=_synthesize_rule_id(process_id, rule_name),
                rule_name=rule_name,
                standard=str(sugg.get("standard") or ""),
                severity=Severity.SUGGESTION,
                title=_truncate(body) or rule_name,
                description=body,
                recommendation=str(sugg.get("recommendation") or ""),
                rationale=str(sugg.get("rationale") or ""),
                measured_value=sugg.get("measured_value") or None,
                expected_value=None,
                cost_impact=sugg.get("cost_impact") or sugg.get("savings") or None,
                location=None,
            )
        )

    # 3) Fallback: if all_rules is empty AND legacy lists exist, fill from them.
    # This keeps older analyzers (or analyzer stubs) from producing empty
    # responses.
    if not findings:
        legacy_pairs = [
            (details.get("critical_issues") or [], Severity.CRITICAL),
            (details.get("warnings") or [], Severity.WARNING),
        ]
        for items, severity in legacy_pairs:
            for item in items:
                if not isinstance(item, Mapping):
                    continue
                rule_name = str(item.get("category") or "Unnamed")
                key = (rule_name, severity)
                if key in seen:
                    continue
                seen.add(key)
                counter += 1
                body = str(item.get("message") or "")
                findings.append(
                    Finding(
                        id=f"f-{counter:03d}",
                        rule_id=_synthesize_rule_id(process_id, rule_name),
                        rule_name=rule_name,
                        standard="",
                        severity=severity,
                        title=_truncate(body) or rule_name,
                        description=body,
                        recommendation=str(item.get("recommendation") or ""),
                        rationale=str(item.get("rationale") or ""),
                        measured_value=None,
                        expected_value=None,
                        cost_impact=None,
                        location=None,
                    )
                )

    return findings


def _build_summary(
    internal: Mapping[str, Any],
    findings: list[Finding],
) -> Summary:
    """Build the Summary block.

    Counts come from the findings list itself (single source of truth)
    rather than from the internal counts, so a transformation bug can't
    let summary and findings disagree on the wire.
    """
    critical = sum(1 for f in findings if f.severity is Severity.CRITICAL)
    warnings = sum(1 for f in findings if f.severity is Severity.WARNING)
    passed = sum(1 for f in findings if f.severity is Severity.PASSED)
    info = sum(1 for f in findings if f.severity is Severity.INFO)
    total_rules = critical + warnings + passed + info

    score = internal.get("score")
    if not isinstance(score, (int, float)):
        score = 0.0
    # Clamp to the contract range; some analyzers may emit slightly out-of-range
    # values during edge cases (e.g. all-info parts).
    score = max(0.0, min(100.0, float(score)))

    narrative = (
        internal.get("summary")
        or internal.get("score_explanation")
        or _default_narrative(critical, warnings, passed)
    )

    summary = Summary(
        score=score,
        total_rules=total_rules,
        passed=passed,
        warnings=warnings,
        critical=critical,
        info=info,
        narrative=str(narrative),
    )
    # Internal sanity check; if violated the transformation has a bug.
    summary.check_invariants()
    return summary


def _default_narrative(critical: int, warnings: int, passed: int) -> str:
    if critical:
        return f"{critical} critical violation(s) require attention before manufacturing."
    if warnings:
        return f"{warnings} warning(s) flagged; review recommended."
    if passed:
        return "All evaluated rules pass."
    return "Analysis complete; no rules were evaluated."


def _build_geometry(internal: Mapping[str, Any], score: float | None) -> Geometry:
    """Build the Geometry block.

    Internal analyzer outputs vary on which fields they populate. We accept
    several aliases and fall back to zero rather than failing the response.
    """
    raw_geo = internal.get("geometry") or {}
    if not isinstance(raw_geo, Mapping):
        raw_geo = {}

    dims_in = raw_geo.get("dimensions") or {}
    if not isinstance(dims_in, Mapping):
        dims_in = {}

    dimensions = Dimensions(
        x=_to_float(dims_in.get("x")),
        y=_to_float(dims_in.get("y")),
        z=_to_float(dims_in.get("z")),
    )

    holes = raw_geo.get("holes") or []
    holes_count = (
        len(holes) if isinstance(holes, list)
        else _to_int(raw_geo.get("holes_count"))
    )

    bends = raw_geo.get("bends") or []
    bends_count = (
        len(bends) if isinstance(bends, list)
        else _to_int(raw_geo.get("bends_count"))
    )

    min_thickness = _to_float(
        raw_geo.get("min_thickness")
        or raw_geo.get("material_thickness")
        or raw_geo.get("estimated_min_thickness")
    )

    return Geometry(
        dimensions_mm=dimensions,
        volume_mm3=_to_float(raw_geo.get("volume")),
        surface_area_mm2=_to_float(raw_geo.get("surface_area")),
        estimated_min_thickness_mm=min_thickness,
        holes_count=holes_count,
        bends_count=bends_count,
        quality_rating=_quality_rating(score),
    )


def _build_exports(analysis_id: str) -> Exports:
    base = f"/api/v1/report/{analysis_id}"
    return Exports(
        html=f"{base}/html",
        json=f"{base}/json",
        docx=f"{base}/docx",
    )


def _to_float(value: Any) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return 0.0
    # Clamp negatives -- internal extractors occasionally emit -0.0 or noise.
    return max(0.0, out)


def _to_int(value: Any) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def to_api_response(
    internal_result: Mapping[str, Any],
    request_metadata: AnalyzeRequestMetadata,
    *,
    analyzed_at: datetime | None = None,
    analysis_id: str | None = None,
) -> ApiAnalyzeResponse:
    """Convert an analyzer's internal dict into a validated ApiAnalyzeResponse.

    Parameters
    ----------
    internal_result
        The dict returned by one of the ``analyze_*`` functions in the
        ``src/`` analyzers. Treated as read-only; never mutated.
    request_metadata
        Captured request context (process / material display names and ids,
        filename). The Flask layer assembles this from ``AnalyzeRequest``
        plus the ``PROCESSES`` lookup table.
    analyzed_at
        Override the timestamp on the response (mostly for tests). Defaults
        to current UTC.
    analysis_id
        Override the analysis id (mostly for tests). Defaults to a fresh
        UUIDv4.

    Returns
    -------
    ApiAnalyzeResponse
        A pydantic model that passes ``model_validate``. Caller serializes
        with ``response.to_wire()``.
    """
    if not isinstance(internal_result, Mapping):
        raise TypeError(
            f"internal_result must be a mapping; got {type(internal_result).__name__}"
        )

    now = analyzed_at or datetime.now(timezone.utc)
    aid = analysis_id or str(uuid4())

    metadata = _build_metadata(request_metadata, now)
    findings = _build_findings(internal_result, request_metadata.process_id.value)
    summary = _build_summary(internal_result, findings)
    geometry = _build_geometry(internal_result, summary.score)
    exports = _build_exports(aid)

    return ApiAnalyzeResponse(
        analysis_id=aid,
        metadata=metadata,
        summary=summary,
        findings=findings,
        geometry=geometry,
        exports=exports,
    )


__all__ = ["to_api_response"]
