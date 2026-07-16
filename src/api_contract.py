"""
Pydantic models for the DFM Inspector API contract v1.

Source of truth:  docs/api-contract.md
Spec:             .kiro/specs/backend-harmony-wireup/

Every response returned by /api/analyze and /api/report/* MUST round-trip
through these models. That gives us:

    1. Runtime validation -- malformed responses fail fast on the server,
       before they hit the frontend.
    2. A single, executable definition of the contract -- the markdown
       doc and these models must stay in sync.
    3. Forward compatibility -- adding optional fields here propagates
       automatically; renaming or removing fields surfaces as a test
       failure rather than a silent frontend break.

Usage:

    from src.api_contract import AnalyzeRequest, ApiAnalyzeResponse

    @app.route("/api/analyze", methods=["POST"])
    def analyze():
        req = AnalyzeRequest.model_validate(request.get_json())
        ...
        response = ApiAnalyzeResponse(...)
        return jsonify(response.model_dump(mode="json"))

The transformation layer that builds an ApiAnalyzeResponse from the
internal analyzer dicts lives in src/api_transform.py (Task 2.x).
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class Severity(str, Enum):
    """Severity tier for a finding. Drives UI badge color and filter chips."""

    CRITICAL = "critical"
    WARNING = "warning"
    SUGGESTION = "suggestion"
    PASSED = "passed"
    INFO = "info"


class ProcessId(str, Enum):
    """Manufacturing process identifier.

    Values mirror the keys in the PROCESSES dict in app.py. When a new
    process is added there, also add it here in the same minor version.
    """

    CNC_MACHINING = "cnc_machining"
    SHEET_METAL = "sheet_metal"
    INJECTION_MOLDING = "injection_molding"
    DIE_CASTING = "die_casting"
    LPDC = "lpdc"
    PERMANENT_MOLD = "permanent_mold"
    INVESTMENT_CASTING = "investment_casting"
    MIM = "mim"
    ROTATIONAL_MOLDING = "rotational_molding"
    WIRE_FORMING = "wire_forming"
    VACUUM_FORMING = "vacuum_forming"
    WELDING = "welding"


class MaterialId(str, Enum):
    """Material identifier. New values may be added in a minor version."""

    ALUMINUM = "aluminum"
    STEEL = "steel"
    STAINLESS_STEEL = "stainless_steel"
    PLASTIC = "plastic"


class LocationKind(str, Enum):
    """Geometry feature class a finding is anchored to."""

    HOLE = "hole"
    EDGE = "edge"
    FACE = "face"
    BEND = "bend"
    CORNER = "corner"
    VERTEX = "vertex"


class QualityRating(str, Enum):
    """Overall geometry quality grade reported in the response."""

    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"
    UNKNOWN = "Unknown"


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


# All models reject unknown fields by default. That gives us early signal
# when the frontend (or a test) starts sending shapes the contract doesn't
# describe, rather than silently dropping data.
_strict = ConfigDict(extra="forbid")


class AnalyzeRequest(BaseModel):
    """Body of POST /api/analyze."""

    model_config = _strict

    upload_id: UUID
    filename: str = Field(min_length=1, max_length=255)
    process: ProcessId
    material: MaterialId


# ---------------------------------------------------------------------------
# Response component models
# ---------------------------------------------------------------------------


class Metadata(BaseModel):
    """Provenance for an analysis."""

    model_config = _strict

    process: str
    process_id: ProcessId
    material: str
    material_id: MaterialId
    filename: str
    analyzed_at: datetime  # serialized as ISO-8601 by model_dump(mode="json")


class Summary(BaseModel):
    """Aggregate counts and narrative for an analysis."""

    model_config = _strict

    score: float = Field(ge=0.0, le=100.0)
    total_rules: int = Field(ge=0)
    passed: int = Field(ge=0)
    warnings: int = Field(ge=0)
    critical: int = Field(ge=0)
    info: int = Field(ge=0)
    narrative: str

    @field_validator("score")
    @classmethod
    def _round_score(cls, v: float) -> float:
        # Display-friendly precision; the underlying calc may produce 78.541237...
        return round(v, 1)

    def check_invariants(self) -> None:
        """Raise if the severity counts don't sum to total_rules.

        Not enforced as a model validator because findings also include
        suggestions, which the contract intentionally excludes from
        total_rules. Callers building a Summary should call this
        explicitly to catch drift.
        """
        expected = self.passed + self.warnings + self.critical + self.info
        if expected != self.total_rules:
            raise ValueError(
                f"Summary invariant violated: total_rules={self.total_rules} "
                f"but passed+warnings+critical+info={expected}"
            )


class Location(BaseModel):
    """3D coordinate marker for a finding."""

    model_config = _strict

    x: float
    y: float
    z: float
    kind: LocationKind


class Finding(BaseModel):
    """A single rule evaluation result."""

    model_config = _strict

    id: str = Field(min_length=1)
    rule_id: str = Field(min_length=1)
    rule_name: str = Field(min_length=1)
    standard: str
    severity: Severity
    title: str = Field(min_length=1)
    description: str
    recommendation: str
    rationale: str
    measured_value: Optional[str] = None
    expected_value: Optional[str] = None
    cost_impact: Optional[str] = None
    location: Optional[Location] = None


class Dimensions(BaseModel):
    """Bounding-box dimensions in mm."""

    model_config = _strict

    x: float = Field(ge=0)
    y: float = Field(ge=0)
    z: float = Field(ge=0)


class Geometry(BaseModel):
    """Top-level geometry summary for the analyzed part."""

    model_config = _strict

    dimensions_mm: Dimensions
    volume_mm3: float = Field(ge=0)
    surface_area_mm2: float = Field(ge=0)
    estimated_min_thickness_mm: float = Field(ge=0)
    holes_count: int = Field(ge=0)
    bends_count: int = Field(ge=0)
    quality_rating: QualityRating


class Exports(BaseModel):
    """Relative URLs for downloading the analysis in different formats.

    Frontend prepends VITE_API_BASE_URL when rendering the actual link.

    Note: the wire-level key is ``json`` but on Python we expose it as
    ``json_`` to avoid shadowing :py:meth:`pydantic.BaseModel.json`.
    Construct with ``Exports(html=..., json=..., docx=...)`` and the
    alias does the right thing on both sides.
    """

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    html: str = Field(min_length=1)
    json_: str = Field(min_length=1, alias="json")
    docx: str = Field(min_length=1)


# ---------------------------------------------------------------------------
# Top-level response model
# ---------------------------------------------------------------------------


class ApiAnalyzeResponse(BaseModel):
    """The complete response from POST /api/analyze."""

    model_config = _strict

    success: Literal[True] = True
    analysis_id: UUID
    metadata: Metadata
    summary: Summary
    findings: list[Finding]
    geometry: Geometry
    exports: Exports

    def to_wire(self) -> dict[str, Any]:
        """Return a JSON-serializable dict in the wire format.

        Always prefer this over plain ``model_dump()``: the ``Exports.json_``
        field uses an alias to keep the wire key ``"json"``, and that only
        kicks in when ``by_alias=True``. ``to_wire`` bakes that in so callers
        never have to remember it.
        """
        return self.model_dump(mode="json", by_alias=True)


# ---------------------------------------------------------------------------
# Error response model
# ---------------------------------------------------------------------------


class ErrorResponse(BaseModel):
    """Standard shape for error responses (non-200 status codes)."""

    model_config = _strict

    success: Literal[False] = False
    error: str = Field(min_length=1)
    code: str = Field(min_length=1)
    details: Optional[dict[str, Any]] = None

    def to_wire(self) -> dict[str, Any]:
        """Return a JSON-serializable dict in the wire format."""
        return self.model_dump(mode="json", by_alias=True)


# ---------------------------------------------------------------------------
# Transformation-layer helper
# ---------------------------------------------------------------------------


class AnalyzeRequestMetadata(BaseModel):
    """Context the transformation layer needs to build a Metadata block.

    Lighter than AnalyzeRequest because by the time we transform a response
    the upload has already been resolved and we only need the human-friendly
    process / material names alongside the ids.
    """

    model_config = _strict

    filename: str
    process_id: ProcessId
    process_display: str
    material_id: MaterialId
    material_display: str


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    # enums
    "Severity",
    "ProcessId",
    "MaterialId",
    "LocationKind",
    "QualityRating",
    # request
    "AnalyzeRequest",
    "AnalyzeRequestMetadata",
    # response components
    "Metadata",
    "Summary",
    "Location",
    "Finding",
    "Dimensions",
    "Geometry",
    "Exports",
    # top-level
    "ApiAnalyzeResponse",
    "ErrorResponse",
]
