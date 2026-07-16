"""
Welding DFM Inspector - Based on AWS Standards and 960-00169_R01
Checks CAD models for weldability and welding design issues
"""
from typing import Dict, List, Tuple
import numpy as np
import yaml


class WeldingInspector:
    """Inspect CAD models for welding DFM issues based on AWS standards"""
    
    def __init__(self, rules_path: str = "config/welding_rules.yaml"):
        with open(rules_path, 'r') as f:
            self.rules = yaml.safe_load(f)
        
        self.issues = []
        self.warnings = []
        self.passed_checks = []
    
    def inspect(self, cad_parser, material_type: str = "carbon_steel") -> Dict:
        """Run all welding DFM inspections"""
        results = {
            'file': cad_parser.file_path,
            'material': material_type,
            'issues': [],
            'warnings': [],
            'passed': [],
            'summary': {}
        }
        
        # Run inspection checks
        self._check_material_thickness(cad_parser, material_type, results)
        self._check_groove_angles(cad_parser, material_type, results)
        self._check_skewed_joints(cad_parser, results)
        self._check_weld_access(cad_parser, results)
        self._check_joint_design(cad_parser, results)
        self._check_design_features(cad_parser, results)
        
        # Generate summary
        results['summary'] = {
            'total_issues': len(results['issues']),
            'total_warnings': len(results['warnings']),
            'total_passed': len(results['passed']),
            'weldability_score': self._calculate_score(results)
        }
        
        return results
    
    def _check_material_thickness(self, parser, material_type: str, results: Dict):
        """Check if material thickness meets AWS standards"""
        thickness_rules = self.rules['material_thickness']
        
        # Get bounding box to estimate thickness
        bbox = parser.get_bounding_box()
        
        if not bbox:
            results['warnings'].append({
                'category': 'Material Thickness',
                'severity': 'medium',
                'message': 'Unable to determine material thickness',
                'recommendation': 'Verify thickness meets AWS standards for selected material'
            })
            return
        
        # Simplified thickness check (would need actual wall thickness analysis)
        min_dimension = min(bbox.get('dimensions', [0, 0, 0]))
        
        # Check based on material type
        if material_type == "steel_structural":
            min_req = thickness_rules['steel_structural']['min_thickness']
            standard = thickness_rules['steel_structural']['applicable_standard']
            
            if min_dimension < min_req:
                results['issues'].append({
                    'category': 'Material Thickness',
                    'severity': 'critical',
                    'message': f'Minimum dimension {min_dimension:.2f}mm below {standard} requirement of {min_req}mm',
                    'recommendation': f'Increase material thickness to at least {min_req}mm for structural steel welding'
                })
            else:
                results['passed'].append({
                    'category': 'Material Thickness',
                    'rule': f'{standard}: Min {min_req}mm',
                    'status': 'passed',
                    'details': f'Material thickness adequate for {material_type}'
                })
    
    def _check_groove_angles(self, parser, material_type: str, results: Dict):
        """Check groove angles for proper weld penetration"""
        groove_rules = self.rules['joint_design']['groove_angles']
        
        # Map material types
        material_map = {
            'steel_structural': 'carbon_steel',
            'stainless_steel': 'stainless_steel',
            'aluminum_structural': 'aluminum'
        }
        
        material_key = material_map.get(material_type, 'carbon_steel')
        
        if material_key in groove_rules:
            angle_spec = groove_rules[material_key]
            min_angle = angle_spec['min_angle']
            max_angle = angle_spec['max_angle']
            recommended = angle_spec['recommended']
            
            # Placeholder for actual angle detection
            # Would need to analyze edge angles in CAD model
            
            check = {
                'category': 'Groove Angle',
                'rule': f'{material_key.replace("_", " ").title()}: {min_angle}° - {max_angle}°',
                'status': 'info',
                'details': f'Recommended groove angle: {recommended}° for optimal fusion and penetration'
            }
            results['passed'].append(check)
    
    def _check_skewed_joints(self, parser, results: Dict):
        """Check for skewed joints and proper beveling requirements"""
        skewed_rules = self.rules['skewed_joints']
        threshold = skewed_rules['inclination_angle_threshold']
        
        # Placeholder for skewed joint detection
        # Would need to analyze joint angles in CAD model
        
        info = {
            'category': 'Skewed Joints',
            'rule': f'Beveling required if inclination angle β > {threshold}°',
            'status': 'info',
            'details': 'Review joint angles: β ≤ 10° = fillet weld OK, β > 10° = beveling required'
        }
        results['passed'].append(info)
        
        # Add critical design rules
        results['warnings'].append({
            'category': 'Skewed Joints',
            'severity': 'medium',
            'message': 'Verify skewed joint angles if present',
            'recommendation': 'For α between 30°-40°: Not recommended, welding tests needed. For α < 30° with γ ≥ 60°: Use fillet weld'
        })
    
    def _check_weld_access(self, parser, results: Dict):
        """Check for adequate welding gun access"""
        access_rules = self.rules['weld_access']
        
        # Critical access requirements
        critical_checks = [
            'Welding gun access to joint',
            'Proper welding angles for fusion/penetration',
            'Adequate stickout distance',
            'Arc accessibility and visibility to weld pool'
        ]
        
        results['warnings'].append({
            'category': 'Weld Access',
            'severity': 'high',
            'message': 'Verify adequate access for welding operations',
            'recommendation': 'Good Design = Good Access = Good Quality Weld. Review: gun access, welding angles, stickout, arc visibility'
        })
    
    def _check_joint_design(self, parser, results: Dict):
        """Check joint design parameters"""
        joint_rules = self.rules['joint_design']
        
        # Root opening check
        results['passed'].append({
            'category': 'Root Opening',
            'rule': 'Gap required for penetration',
            'status': 'info',
            'details': 'Verify root opening (gap) is specified for proper fusion and penetration'
        })
        
        # Root face check
        root_face_rules = joint_rules['root_face']
        results['passed'].append({
            'category': 'Root Face',
            'rule': f'Min {root_face_rules["min_for_bevel_angle_30_plus"]}mm for bevel ≥ 30°',
            'status': 'info',
            'details': 'Root face not required for bevel angles < 30°'
        })
    
    def _check_design_features(self, parser, results: Dict):
        """Check for required design features"""
        design_rules = self.rules['design_considerations']
        
        # Drain holes
        results['warnings'].append({
            'category': 'Design Features',
            'severity': 'medium',
            'message': 'Verify drain holes and out-gassing provisions',
            'recommendation': 'Add drain holes for cleaning process and out-gassing holes for all-around welds'
        })
        
        # Fixturing
        results['warnings'].append({
            'category': 'Fixturing',
            'severity': 'medium',
            'message': 'Review fixturing and tooling requirements',
            'recommendation': 'Ensure fixturing based on datum structure, add tooling/location holes, consider warpage for long welds'
        })
        
        # Finishing
        results['passed'].append({
            'category': 'Finishing',
            'rule': 'Paint/powder coating considerations',
            'status': 'info',
            'details': 'Review hang locations and tooling holes for finishing operations'
        })
    
    def _calculate_score(self, results: Dict) -> float:
        """Calculate weldability score (0-100)"""
        total_checks = len(results['issues']) + len(results['warnings']) + len(results['passed'])
        
        if total_checks == 0:
            return 0.0
        
        # Weight: issues = -10, warnings = -3, passed = +1
        score = (len(results['passed']) - 10 * len(results['issues']) - 3 * len(results['warnings']))
        max_score = total_checks
        
        normalized_score = max(0, min(100, (score / max_score) * 100))
        return round(normalized_score, 2)
    
    def get_applicable_standards(self, material_type: str) -> List[str]:
        """Get applicable AWS standards for material type"""
        thickness_rules = self.rules['material_thickness']
        
        if material_type in thickness_rules:
            return [thickness_rules[material_type].get('applicable_standard', 'AWS D1.1')]
        
        return self.rules['general']['applicable_standards']
    
    def get_filler_material_recommendation(self, material_type: str, process: str = "gmaw") -> str:
        """Get recommended filler material"""
        filler_rules = self.rules['filler_materials']
        
        if material_type in ['steel_structural', 'sheet_steel']:
            return filler_rules['steel'].get(process, 'ER70S-6')
        elif material_type == 'aluminum_structural':
            return "ER4043 (preferred) or ER5356"
        
        return "Consult AWS A5 series standards"
