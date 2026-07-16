"""
Manufacturing rules based on industry standards and best practices
Content rephrased for compliance with licensing restrictions
"""
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ManufacturingRule:
    """Represents a single manufacturing rule"""
    name: str
    category: str
    severity: str  # 'critical', 'warning', 'info'
    description: str
    threshold: float
    unit: str
    recommendation: str


class ManufacturingRules:
    """Collection of manufacturing rules based on industry standards"""
    
    # Based on ISO standards and industry best practices
    # Content rephrased for compliance with licensing restrictions
    
    INJECTION_MOLDING_RULES = [
        ManufacturingRule(
            name="min_wall_thickness",
            category="Wall Thickness",
            severity="critical",
            description="Minimum wall thickness for structural integrity",
            threshold=1.5,
            unit="mm",
            recommendation="Increase wall thickness to prevent weak points and ensure proper material flow"
        ),
        ManufacturingRule(
            name="wall_thickness_uniformity",
            category="Wall Thickness",
            severity="warning",
            description="Wall thickness variation ratio",
            threshold=2.0,
            unit="ratio",
            recommendation="Maintain uniform wall thickness to prevent warping and sink marks"
        ),
        ManufacturingRule(
            name="min_draft_angle",
            category="Draft Angle",
            severity="critical",
            description="Minimum draft angle for part ejection",
            threshold=1.0,
            unit="degrees",
            recommendation="Add draft angle to vertical surfaces for easier mold release"
        ),
        ManufacturingRule(
            name="min_internal_radius",
            category="Corner Radius",
            severity="warning",
            description="Minimum internal corner radius",
            threshold=0.5,
            unit="mm",
            recommendation="Add radius to sharp corners to reduce stress concentration"
        ),
        ManufacturingRule(
            name="rib_thickness_ratio",
            category="Ribs",
            severity="warning",
            description="Rib thickness as ratio of nominal wall",
            threshold=0.6,
            unit="ratio",
            recommendation="Keep rib thickness at 50-60% of nominal wall thickness"
        ),
    ]
    
    CNC_MACHINING_RULES = [
        ManufacturingRule(
            name="min_tool_radius",
            category="Tool Access",
            severity="critical",
            description="Minimum internal corner radius for tool access",
            threshold=1.0,
            unit="mm",
            recommendation="Increase corner radius to match available tool sizes"
        ),
        ManufacturingRule(
            name="min_hole_diameter",
            category="Holes",
            severity="warning",
            description="Minimum hole diameter for drilling",
            threshold=0.5,
            unit="mm",
            recommendation="Use standard drill sizes for cost-effective manufacturing"
        ),
        ManufacturingRule(
            name="hole_depth_ratio",
            category="Holes",
            severity="warning",
            description="Maximum hole depth to diameter ratio",
            threshold=10.0,
            unit="ratio",
            recommendation="Limit hole depth to 10x diameter for standard drilling"
        ),
    ]
    
    ROBOTICS_SPECIFIC_RULES = [
        ManufacturingRule(
            name="load_bearing_thickness",
            category="Structural",
            severity="critical",
            description="Minimum thickness for load-bearing components",
            threshold=3.0,
            unit="mm",
            recommendation="Increase thickness for components under mechanical stress"
        ),
        ManufacturingRule(
            name="safety_factor",
            category="Safety",
            severity="critical",
            description="Minimum safety factor for structural components",
            threshold=2.0,
            unit="factor",
            recommendation="Apply appropriate safety factor based on ISO 3691-4 standards"
        ),
        ManufacturingRule(
            name="fatigue_critical_radius",
            category="Fatigue",
            severity="warning",
            description="Minimum radius for fatigue-critical areas",
            threshold=1.0,
            unit="mm",
            recommendation="Increase radius in high-cycle loading areas"
        ),
    ]
    
    @classmethod
    def get_rules_by_process(cls, process: str) -> List[ManufacturingRule]:
        """Get rules for specific manufacturing process"""
        process_map = {
            'injection_molding': cls.INJECTION_MOLDING_RULES,
            'cnc_machining': cls.CNC_MACHINING_RULES,
            'robotics': cls.ROBOTICS_SPECIFIC_RULES,
        }
        return process_map.get(process.lower(), [])
    
    @classmethod
    def get_all_rules(cls) -> List[ManufacturingRule]:
        """Get all manufacturing rules"""
        return (cls.INJECTION_MOLDING_RULES + 
                cls.CNC_MACHINING_RULES + 
                cls.ROBOTICS_SPECIFIC_RULES)
    
    @classmethod
    def get_rule_by_name(cls, name: str) -> ManufacturingRule:
        """Get specific rule by name"""
        for rule in cls.get_all_rules():
            if rule.name == name:
                return rule
        return None
