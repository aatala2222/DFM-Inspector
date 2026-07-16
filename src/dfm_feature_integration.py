"""
DFM Feature Integration - Connect Features to Rule Violations

Integrates feature detection with DFM rule checking to generate
violations with 3D coordinates for visual highlighting.
"""
import logging
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from src.feature_detector import Feature, Hole, Corner, Pocket
from src.geometry_analyzer import GeometryAnalyzer, ThicknessMeasurement

logger = logging.getLogger(__name__)


@dataclass
class DFMViolation:
    """DFM rule violation with 3D location"""
    rule_name: str
    feature_type: str  # 'hole', 'corner', 'wall_thickness', etc.
    severity: str  # 'critical', 'warning', 'suggestion'
    measured_value: float
    required_value: float
    location: Tuple[float, float, float]
    feature: Optional[Feature] = None
    message: str = ""
    recommendation: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'rule_name': self.rule_name,
            'feature_type': self.feature_type,
            'severity': self.severity,
            'measured_value': self.measured_value,
            'required_value': self.required_value,
            'location': self.location,
            'message': self.message,
            'recommendation': self.recommendation
        }


class DFMFeatureIntegration:
    """
    Integrate feature detection with DFM rule checking
    
    Analyzes detected features against manufacturing rules and
    generates violations with 3D coordinates for visualization.
    """
    
    def __init__(self, process: str, material: str):
        """
        Initialize DFM feature integration
        
        Args:
            process: Manufacturing process (cnc_machining, sheet_metal, etc.)
            material: Material name
        """
        self.process = process
        self.material = material
        self.violations = []
        
        # Load process-specific rules
        self.rules = self._load_rules()
        
        logger.info(f"Initialized DFM integration for {process} with {material}")
    
    def _load_rules(self) -> Dict:
        """Load manufacturing rules for the process"""
        rules = {}
        
        if self.process == 'cnc_machining':
            rules = {
                'min_wall_thickness': {
                    'aluminum': 0.8,  # mm
                    'steel': 1.0,
                    'default': 1.0
                },
                'min_hole_diameter': {
                    'aluminum': 1.0,  # mm
                    'steel': 1.5,
                    'default': 1.0
                },
                'max_hole_depth_ratio': 10.0,  # depth/diameter
                'min_corner_radius': {
                    'internal': 0.5,  # mm
                    'external': 0.0
                },
                'min_pocket_corner_radius': 1.0  # mm
            }
        
        elif self.process == 'sheet_metal':
            rules = {
                'min_wall_thickness': {
                    'aluminum': 0.5,
                    'steel': 0.8,
                    'default': 0.8
                },
                'min_bend_radius': {
                    'aluminum': 1.0,
                    'steel': 1.5,
                    'default': 1.0
                },
                'min_hole_to_edge': 2.0  # mm
            }
        
        elif self.process == 'injection_molding':
            rules = {
                'min_wall_thickness': {
                    'abs': 0.8,
                    'polycarbonate': 1.0,
                    'default': 1.0
                },
                'max_wall_thickness': {
                    'abs': 4.0,
                    'polycarbonate': 4.0,
                    'default': 4.0
                },
                'min_draft_angle': 1.0,  # degrees
                'min_corner_radius': 0.5  # mm
            }
        
        else:
            # Default rules
            rules = {
                'min_wall_thickness': {'default': 1.0},
                'min_hole_diameter': {'default': 1.0}
            }
        
        return rules
    
    def check_wall_thickness(self, geometry_analyzer: GeometryAnalyzer,
                            min_thickness_override: Optional[float] = None) -> List[DFMViolation]:
        """
        Check wall thickness against rules
        
        Args:
            geometry_analyzer: GeometryAnalyzer with thickness measurements
            min_thickness_override: Override minimum thickness requirement
            
        Returns:
            List of violations
        """
        violations = []
        
        # Get minimum required thickness
        material_lower = self.material.lower()
        min_required = min_thickness_override
        
        if min_required is None:
            thickness_rules = self.rules.get('min_wall_thickness', {})
            for material_key in thickness_rules:
                if material_key in material_lower:
                    min_required = thickness_rules[material_key]
                    break
            if min_required is None:
                min_required = thickness_rules.get('default', 1.0)
        
        # Check if thickness map exists
        thickness_map = geometry_analyzer.get_thickness_map()
        
        if not thickness_map:
            logger.warning("No thickness measurements available")
            return violations
        
        # Find violations
        for location, thickness in thickness_map.items():
            if thickness < min_required:
                violation = DFMViolation(
                    rule_name='Minimum Wall Thickness',
                    feature_type='wall_thickness',
                    severity='critical' if thickness < min_required * 0.8 else 'warning',
                    measured_value=thickness,
                    required_value=min_required,
                    location=location,
                    message=f'Wall thickness {thickness:.2f}mm is below minimum {min_required:.2f}mm',
                    recommendation=f'Increase wall thickness to at least {min_required:.2f}mm'
                )
                violations.append(violation)
        
        logger.info(f"Found {len(violations)} wall thickness violations")
        return violations
    
    def check_holes(self, holes: List[Hole]) -> List[DFMViolation]:
        """
        Check holes against manufacturing rules
        
        Args:
            holes: List of detected holes
            
        Returns:
            List of violations
        """
        violations = []
        
        # Get rules
        min_diameter = self.rules.get('min_hole_diameter', {}).get('default', 1.0)
        max_depth_ratio = self.rules.get('max_hole_depth_ratio', 10.0)
        
        for hole in holes:
            # Check minimum diameter
            if hole.diameter < min_diameter:
                violation = DFMViolation(
                    rule_name='Minimum Hole Diameter',
                    feature_type='hole',
                    severity='critical',
                    measured_value=hole.diameter,
                    required_value=min_diameter,
                    location=hole.center,
                    feature=hole,
                    message=f'Hole diameter {hole.diameter:.2f}mm is below minimum {min_diameter:.2f}mm',
                    recommendation=f'Increase hole diameter to at least {min_diameter:.2f}mm'
                )
                violations.append(violation)
            
            # Check depth-to-diameter ratio
            if hole.depth > 0 and hole.diameter > 0:
                depth_ratio = hole.depth / hole.diameter
                if depth_ratio > max_depth_ratio:
                    violation = DFMViolation(
                        rule_name='Maximum Hole Depth Ratio',
                        feature_type='hole',
                        severity='warning',
                        measured_value=depth_ratio,
                        required_value=max_depth_ratio,
                        location=hole.center,
                        feature=hole,
                        message=f'Hole depth/diameter ratio {depth_ratio:.1f}:1 exceeds maximum {max_depth_ratio:.1f}:1',
                        recommendation=f'Reduce hole depth or increase diameter to achieve {max_depth_ratio:.1f}:1 ratio'
                    )
                    violations.append(violation)
        
        logger.info(f"Found {len(violations)} hole violations")
        return violations
    
    def check_corners(self, corners: List[Corner]) -> List[DFMViolation]:
        """
        Check corners against manufacturing rules
        
        Args:
            corners: List of detected corners
            
        Returns:
            List of violations
        """
        violations = []
        
        # Get rules
        min_internal_radius = self.rules.get('min_corner_radius', {}).get('internal', 0.5)
        
        for corner in corners:
            # Check internal corners only
            if corner.is_internal and corner.radius < min_internal_radius:
                violation = DFMViolation(
                    rule_name='Minimum Internal Corner Radius',
                    feature_type='corner',
                    severity='warning',
                    measured_value=corner.radius,
                    required_value=min_internal_radius,
                    location=corner.center,
                    feature=corner,
                    message=f'Internal corner radius {corner.radius:.2f}mm is below minimum {min_internal_radius:.2f}mm',
                    recommendation=f'Add {min_internal_radius:.2f}mm radius to internal corners'
                )
                violations.append(violation)
        
        logger.info(f"Found {len(violations)} corner violations")
        return violations
    
    def check_pockets(self, pockets: List[Pocket]) -> List[DFMViolation]:
        """
        Check pockets against manufacturing rules
        
        Args:
            pockets: List of detected pockets
            
        Returns:
            List of violations
        """
        violations = []
        
        # Get rules
        min_corner_radius = self.rules.get('min_pocket_corner_radius', 1.0)
        
        for pocket in pockets:
            # Check corner radii
            if pocket.corner_radii:
                min_radius = min(pocket.corner_radii)
                if min_radius < min_corner_radius:
                    violation = DFMViolation(
                        rule_name='Minimum Pocket Corner Radius',
                        feature_type='pocket',
                        severity='warning',
                        measured_value=min_radius,
                        required_value=min_corner_radius,
                        location=pocket.center,
                        feature=pocket,
                        message=f'Pocket corner radius {min_radius:.2f}mm is below minimum {min_corner_radius:.2f}mm',
                        recommendation=f'Add {min_corner_radius:.2f}mm radius to pocket corners'
                    )
                    violations.append(violation)
        
        logger.info(f"Found {len(violations)} pocket violations")
        return violations
    
    def analyze_all_features(self, geometry_analyzer: Optional[GeometryAnalyzer] = None,
                            holes: Optional[List[Hole]] = None,
                            corners: Optional[List[Corner]] = None,
                            pockets: Optional[List[Pocket]] = None) -> Dict:
        """
        Analyze all features and generate comprehensive violation report
        
        Args:
            geometry_analyzer: GeometryAnalyzer with measurements
            holes: List of detected holes
            corners: List of detected corners
            pockets: List of detected pockets
            
        Returns:
            Dictionary with violations and summary
        """
        logger.info("Starting comprehensive feature analysis...")
        
        all_violations = []
        
        # Check wall thickness
        if geometry_analyzer:
            thickness_violations = self.check_wall_thickness(geometry_analyzer)
            all_violations.extend(thickness_violations)
        
        # Check holes
        if holes:
            hole_violations = self.check_holes(holes)
            all_violations.extend(hole_violations)
        
        # Check corners
        if corners:
            corner_violations = self.check_corners(corners)
            all_violations.extend(corner_violations)
        
        # Check pockets
        if pockets:
            pocket_violations = self.check_pockets(pockets)
            all_violations.extend(pocket_violations)
        
        # Store violations
        self.violations = all_violations
        
        # Generate summary
        summary = {
            'total_violations': len(all_violations),
            'by_severity': {
                'critical': len([v for v in all_violations if v.severity == 'critical']),
                'warning': len([v for v in all_violations if v.severity == 'warning']),
                'suggestion': len([v for v in all_violations if v.severity == 'suggestion'])
            },
            'by_feature_type': {},
            'violations': [v.to_dict() for v in all_violations]
        }
        
        # Count by feature type
        for violation in all_violations:
            feature_type = violation.feature_type
            if feature_type not in summary['by_feature_type']:
                summary['by_feature_type'][feature_type] = 0
            summary['by_feature_type'][feature_type] += 1
        
        logger.info(f"✓ Analysis complete: {len(all_violations)} total violations")
        logger.info(f"  Critical: {summary['by_severity']['critical']}")
        logger.info(f"  Warnings: {summary['by_severity']['warning']}")
        
        return summary
    
    def get_violations_for_visualization(self) -> Dict[str, List[Tuple]]:
        """
        Get violations organized for 3D visualization
        
        Returns:
            Dictionary mapping severity to list of (location, feature_type) tuples
        """
        viz_data = {
            'critical': [],
            'warning': [],
            'suggestion': []
        }
        
        for violation in self.violations:
            viz_data[violation.severity].append({
                'location': violation.location,
                'feature_type': violation.feature_type,
                'measured_value': violation.measured_value,
                'required_value': violation.required_value,
                'message': violation.message
            })
        
        return viz_data
