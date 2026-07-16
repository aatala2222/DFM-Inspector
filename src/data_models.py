"""
Data Models for Enhanced 3D Geometry Analysis and Visualization

This module defines all dataclasses for geometric entities, features, measurements,
and violations used throughout the enhanced geometry analysis system.

Requirements: All requirements (data structures used throughout)
Design Reference: Section "Data Models"
"""

from dataclasses import dataclass, field, asdict
from typing import List, Tuple, Optional, Dict, Any
import numpy as np
import json
from datetime import datetime


# ============================================================================
# Base Geometric Entities
# ============================================================================

@dataclass
class GeometricEntity:
    """Base class for geometric entities"""
    entity_id: str
    entity_type: str  # 'vertex', 'edge', 'face', 'surface'
    coordinates: np.ndarray = field(repr=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        if isinstance(self.coordinates, np.ndarray):
            data['coordinates'] = self.coordinates.tolist()
        return data


@dataclass
class Vertex(GeometricEntity):
    """3D point"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def __post_init__(self):
        """Initialize coordinates array from x, y, z"""
        if not isinstance(self.coordinates, np.ndarray):
            self.coordinates = np.array([self.x, self.y, self.z])
        else:
            self.x, self.y, self.z = self.coordinates


@dataclass
class Edge(GeometricEntity):
    """Line segment between two vertices"""
    v1_id: int = 0
    v2_id: int = 0
    length: float = 0.0


@dataclass
class Face(GeometricEntity):
    """Triangular face"""
    v1_id: int = 0
    v2_id: int = 0
    v3_id: int = 0
    normal: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    area: float = 0.0


@dataclass
class Surface(GeometricEntity):
    """Parametric surface"""
    surface_type: str = 'plane'  # 'plane', 'cylinder', 'sphere', 'cone', 'torus'
    parameters: Dict[str, float] = field(default_factory=dict)
    face_ids: List[int] = field(default_factory=list)


# ============================================================================
# Measurements
# ============================================================================

@dataclass
class Measurement:
    """Generic measurement with location"""
    measurement_type: str
    value: float
    unit: str = 'mm'
    location: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    confidence: float = 100.0  # 0-100%
    method: str = 'unknown'  # 'ray_casting', 'surface_fitting', 'edge_detection'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class WallThicknessMeasurement(Measurement):
    """Wall thickness measurement"""
    sample_point: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    opposing_point: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    normal_direction: Tuple[float, float, float] = (0.0, 0.0, 1.0)


# ============================================================================
# Features
# ============================================================================

@dataclass
class Feature:
    """Base class for detected features"""
    feature_id: str
    feature_type: str
    center: Tuple[float, float, float]
    dimensions: Dict[str, float] = field(default_factory=dict)
    coordinates: List[Tuple[float, float, float]] = field(default_factory=list)
    confidence: float = 100.0  # 0-100%
    detection_method: str = 'geometric_analysis'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class Hole(Feature):
    """Cylindrical hole feature"""
    diameter: float = 0.0
    depth: float = 0.0
    axis: Tuple[float, float, float] = (0.0, 0.0, 1.0)
    is_through: bool = False
    is_threaded: bool = False
    thread_pitch: Optional[float] = None
    min_edge_distance: float = 0.0
    edge_distances: Dict[str, float] = field(default_factory=dict)


@dataclass
class Pocket(Feature):
    """Cavity feature"""
    width: float = 0.0
    length: float = 0.0
    depth: float = 0.0
    corner_radii: List[float] = field(default_factory=list)
    is_open: bool = True
    is_deep: bool = False  # depth > 3 * width


@dataclass
class Corner(Feature):
    """Corner or edge feature"""
    radius: float = 0.0
    angle: float = 0.0  # Degrees
    is_internal: bool = True
    is_fillet: bool = True  # True=fillet, False=chamfer
    chamfer_distance: Optional[float] = None


@dataclass
class Boss(Feature):
    """Raised cylindrical protrusion"""
    diameter: float = 0.0
    height: float = 0.0


@dataclass
class Rib(Feature):
    """Thin wall protrusion"""
    thickness: float = 0.0
    height: float = 0.0
    length: float = 0.0
    is_tall: bool = False  # height > 3 * thickness


# ============================================================================
# Violations
# ============================================================================

@dataclass
class Violation:
    """DFM rule violation"""
    violation_id: str
    rule_name: str
    rule_standard: str = ''  # e.g., "ISO 2768-m"
    feature: Optional[Feature] = None
    measured_value: float = 0.0
    required_value: float = 0.0
    severity: str = 'warning'  # 'critical', 'warning', 'info'
    coordinates: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    message: str = ''
    recommendation: str = ''
    rationale: str = ''
    cost_impact: str = ''
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        if self.feature:
            data['feature'] = self.feature.to_dict()
        return data


# ============================================================================
# Feature Report
# ============================================================================

@dataclass
class FeatureReport:
    """Complete feature detection report"""
    part_name: str
    analysis_date: str = field(default_factory=lambda: datetime.now().isoformat())
    walls: List[WallThicknessMeasurement] = field(default_factory=list)
    holes: List[Hole] = field(default_factory=list)
    pockets: List[Pocket] = field(default_factory=list)
    corners: List[Corner] = field(default_factory=list)
    bosses: List[Boss] = field(default_factory=list)
    ribs: List[Rib] = field(default_factory=list)
    measurements: Dict[str, Measurement] = field(default_factory=dict)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    
    def to_json(self) -> str:
        """Export to JSON format"""
        data = {
            'part_name': self.part_name,
            'analysis_date': self.analysis_date,
            'walls': [w.to_dict() for w in self.walls],
            'holes': [h.to_dict() for h in self.holes],
            'pockets': [p.to_dict() for p in self.pockets],
            'corners': [c.to_dict() for c in self.corners],
            'bosses': [b.to_dict() for b in self.bosses],
            'ribs': [r.to_dict() for r in self.ribs],
            'measurements': {k: v.to_dict() for k, v in self.measurements.items()},
            'confidence_scores': self.confidence_scores
        }
        return json.dumps(data, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'FeatureReport':
        """Import from JSON format"""
        data = json.loads(json_str)
        
        # Reconstruct wall measurements
        walls = [
            WallThicknessMeasurement(**w) for w in data.get('walls', [])
        ]
        
        # Reconstruct holes
        holes = [
            Hole(**h) for h in data.get('holes', [])
        ]
        
        # Reconstruct pockets
        pockets = [
            Pocket(**p) for p in data.get('pockets', [])
        ]
        
        # Reconstruct corners
        corners = [
            Corner(**c) for c in data.get('corners', [])
        ]
        
        # Reconstruct bosses
        bosses = [
            Boss(**b) for b in data.get('bosses', [])
        ]
        
        # Reconstruct ribs
        ribs = [
            Rib(**r) for r in data.get('ribs', [])
        ]
        
        # Reconstruct measurements
        measurements = {
            k: Measurement(**v) for k, v in data.get('measurements', {}).items()
        }
        
        return cls(
            part_name=data['part_name'],
            analysis_date=data.get('analysis_date', datetime.now().isoformat()),
            walls=walls,
            holes=holes,
            pockets=pockets,
            corners=corners,
            bosses=bosses,
            ribs=ribs,
            measurements=measurements,
            confidence_scores=data.get('confidence_scores', {})
        )
