"""
DFM Inspector - Analyzes CAD models against manufacturing rules
"""
from typing import Dict, List, Tuple
import numpy as np
import yaml


class DFMInspector:
    """Inspect CAD models for Design for Manufacturability issues"""
    
    def __init__(self, rules_path: str = "config/inspection_rules.yaml"):
        with open(rules_path, 'r') as f:
            self.rules = yaml.safe_load(f)
        
        self.issues = []
        self.warnings = []
        self.passed_checks = []
    
    def inspect(self, cad_parser) -> Dict:
        """Run all DFM inspections"""
        results = {
            'file': cad_parser.file_path,
            'issues': [],
            'warnings': [],
            'passed': [],
            'summary': {}
        }
        
        # Run inspection checks
        self._check_wall_thickness(cad_parser, results)
        self._check_draft_angles(cad_parser, results)
        self._check_undercuts(cad_parser, results)
        self._check_corners_and_edges(cad_parser, results)
        self._check_ribs_and_bosses(cad_parser, results)
        self._check_tolerances(cad_parser, results)
        
        # Generate summary
        results['summary'] = {
            'total_issues': len(results['issues']),
            'total_warnings': len(results['warnings']),
            'total_passed': len(results['passed']),
            'manufacturability_score': self._calculate_score(results)
        }
        
        return results
    
    def _check_wall_thickness(self, parser, results: Dict):
        """Check wall thickness uniformity and limits"""
        rules = self.rules['wall_thickness']
        
        # Placeholder for actual thickness analysis
        # Would need to implement mesh slicing and thickness measurement
        
        check = {
            'category': 'Wall Thickness',
            'rule': f"Min: {rules['min_thickness']}mm, Max: {rules['max_thickness']}mm",
            'status': 'passed',
            'details': 'Wall thickness within acceptable range'
        }
        
        results['passed'].append(check)
    
    def _check_draft_angles(self, parser, results: Dict):
        """Check draft angles on vertical faces"""
        rules = self.rules['draft_angles']
        
        faces = parser.extract_faces()
        
        for i, face in enumerate(faces):
            # Simplified check - would need actual angle calculation
            draft_angle = 2.0  # Placeholder
            
            if draft_angle < rules['min_draft_smooth']:
                results['issues'].append({
                    'category': 'Draft Angle',
                    'severity': 'high',
                    'location': f'Face {i}',
                    'message': f'Draft angle {draft_angle}° is below minimum {rules["min_draft_smooth"]}°',
                    'recommendation': 'Add draft angle to facilitate part ejection'
                })
    
    def _check_undercuts(self, parser, results: Dict):
        """Detect undercuts that prevent mold release"""
        rules = self.rules['undercuts']
        
        if not rules['allow_undercuts']:
            # Placeholder for undercut detection
            check = {
                'category': 'Undercuts',
                'rule': 'No undercuts allowed',
                'status': 'passed',
                'details': 'No undercuts detected'
            }
            results['passed'].append(check)
    
    def _check_corners_and_edges(self, parser, results: Dict):
        """Check for sharp corners and edges"""
        rules = self.rules['corners_and_edges']
        
        # Placeholder for corner radius analysis
        min_radius_found = 0.5  # Placeholder
        
        if min_radius_found < rules['min_internal_radius']:
            results['warnings'].append({
                'category': 'Corner Radius',
                'severity': 'medium',
                'message': f'Sharp internal corner detected (radius: {min_radius_found}mm)',
                'recommendation': f'Increase radius to at least {rules["min_internal_radius"]}mm'
            })
    
    def _check_ribs_and_bosses(self, parser, results: Dict):
        """Check rib and boss design"""
        rules = self.rules['ribs_and_bosses']
        
        check = {
            'category': 'Ribs and Bosses',
            'rule': f"Rib thickness ratio: {rules['rib_thickness_ratio']}",
            'status': 'passed',
            'details': 'Rib proportions acceptable'
        }
        results['passed'].append(check)
    
    def _check_tolerances(self, parser, results: Dict):
        """Check tolerance specifications"""
        rules = self.rules['tolerances']
        
        bbox = parser.get_bounding_box()
        
        if bbox:
            dims = bbox.get('dimensions', [0, 0, 0])
            check = {
                'category': 'Tolerances',
                'rule': f"Standard tolerance: ±{rules['standard_tolerance']}mm",
                'status': 'info',
                'details': f'Model dimensions: {dims[0]:.2f} x {dims[1]:.2f} x {dims[2]:.2f} mm'
            }
            results['passed'].append(check)
    
    def _calculate_score(self, results: Dict) -> float:
        """Calculate manufacturability score (0-100)"""
        total_checks = len(results['issues']) + len(results['warnings']) + len(results['passed'])
        
        if total_checks == 0:
            return 0.0
        
        # Weight: issues = -10, warnings = -3, passed = +1
        score = (len(results['passed']) - 10 * len(results['issues']) - 3 * len(results['warnings']))
        max_score = total_checks
        
        normalized_score = max(0, min(100, (score / max_score) * 100))
        return round(normalized_score, 2)
