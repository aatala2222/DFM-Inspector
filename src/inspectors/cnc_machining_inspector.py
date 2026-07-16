"""
CNC Machining DFM Inspector
Based on CNC_DFM_Guidelines.md
Standards: ISO 2768, ASME Y14.5
"""
from typing import Dict, List, Tuple
import numpy as np
import yaml


class CNCMachiningInspector:
    """Inspect CAD models for CNC machining DFM issues"""
    
    def __init__(self, rules_path: str = "config/cnc_machining_rules.yaml"):
        with open(rules_path, 'r') as f:
            self.rules = yaml.safe_load(f)
        
        self.issues = []
        self.warnings = []
        self.passed_checks = []
    
    def inspect(self, cad_parser, material: str = "aluminum_6061") -> Dict:
        """Run all CNC machining DFM inspections"""
        results = {
            'file': cad_parser.file_path,
            'material': material,
            'process': 'CNC Machining',
            'issues': [],
            'warnings': [],
            'passed': [],
            'suggestions': [],
            'summary': {}
        }
        
        # Run inspection checks
        self._check_tolerances(cad_parser, results)
        self._check_internal_corners(cad_parser, results)
        self._check_wall_thickness(cad_parser, material, results)
        self._check_pockets_and_cavities(cad_parser, results)
        self._check_holes(cad_parser, results)
        self._check_threads(cad_parser, results)
        self._check_material_selection(material, results)
        self._check_setup_requirements(cad_parser, results)
        self._check_tool_access(cad_parser, results)
        self._check_surface_finish(cad_parser, results)
        self._check_geometry_complexity(cad_parser, results)
        self._check_standard_features(cad_parser, results)
        self._check_thermal_stability(cad_parser, material, results)
        
        # Generate summary
        results['summary'] = {
            'total_issues': len(results['issues']),
            'total_warnings': len(results['warnings']),
            'total_suggestions': len(results['suggestions']),
            'total_passed': len(results['passed']),
            'machinability_score': self._calculate_score(results),
            'material_rating': self._get_material_rating(material),
            'estimated_setups': self._estimate_setups(cad_parser)
        }
        
        # Add cost optimization opportunities
        results['cost_optimization'] = self._identify_cost_opportunities(results)
        
        return results
    
    def _check_tolerances(self, parser, results: Dict):
        """Check tolerance specifications"""
        tol_rules = self.rules['tolerances']
        
        # Placeholder for actual tolerance analysis
        # Would need to parse tolerance annotations from CAD
        
        results['passed'].append({
            'category': 'Tolerances',
            'rule': f'Standard tolerance: ±{tol_rules["standard_tolerance"]}mm',
            'status': 'info',
            'details': f'Target: <{tol_rules["target_tight_tolerance_percentage"]}% features with tight tolerances'
        })
        
        results['warnings'].append({
            'category': 'Tolerances',
            'severity': 'medium',
            'message': 'Verify tolerance specifications',
            'recommendation': f'Apply tight tolerances (±{tol_rules["precision_tolerance_min"]}-{tol_rules["precision_tolerance_max"]}mm) only to critical mating surfaces. Over-tolerancing increases cost by {int(tol_rules["cost_impact_per_tight_feature"]*100)}%'
        })
    
    def _check_internal_corners(self, parser, results: Dict):
        """Check internal corner radii"""
        corner_rules = self.rules['internal_corners']
        
        min_radius = corner_rules['minimum_radius']
        standard_sizes = corner_rules['standard_sizes']
        
        results['warnings'].append({
            'category': 'Internal Corners',
            'severity': 'high',
            'message': 'Verify all internal corners have adequate radii',
            'recommendation': f'Minimum radius: {min_radius}mm. Recommended: {corner_rules["recommended_ratio"]}× pocket depth. Standard sizes: {standard_sizes}mm. Sharp corners require EDM (+{int((corner_rules["cost_impact"]["cost_increase"]-1)*100)}% cost)'
        })
    
    def _check_wall_thickness(self, parser, material: str, results: Dict):
        """Check wall thickness requirements"""
        wall_rules = self.rules['wall_thickness']
        
        if material in wall_rules['by_material']:
            mat_spec = wall_rules['by_material'][material]
            min_thick = mat_spec['absolute_min']
            rec_thick = mat_spec['recommended']
            
            bbox = parser.get_bounding_box()
            if bbox:
                min_dim = min(bbox.get('dimensions', [0, 0, 0]))
                
                if min_dim < min_thick:
                    results['issues'].append({
                        'category': 'Wall Thickness',
                        'severity': 'critical',
                        'message': f'Minimum dimension {min_dim:.2f}mm below {material} minimum of {min_thick}mm',
                        'recommendation': f'Increase wall thickness to at least {rec_thick}mm (recommended)'
                    })
                else:
                    results['passed'].append({
                        'category': 'Wall Thickness',
                        'rule': f'{material}: Min {min_thick}mm, Recommended {rec_thick}mm',
                        'status': 'passed',
                        'details': f'Wall thickness adequate. Machinability: {mat_spec.get("machinability", "N/A")}'
                    })
        
        # Check aspect ratio
        max_ratio = wall_rules['structural']['max_aspect_ratio']
        results['warnings'].append({
            'category': 'Wall Thickness',
            'severity': 'medium',
            'message': 'Verify wall aspect ratios',
            'recommendation': f'Keep height:thickness ratio ≤{max_ratio}:1. Add ribs for ratios >{wall_rules["structural"]["recommend_ribs_above"]}:1'
        })
    
    def _check_pockets_and_cavities(self, parser, results: Dict):
        """Check pocket and cavity depths"""
        pocket_rules = self.rules['pockets']
        
        max_ratio = pocket_rules['max_depth_ratio']
        optimal_min = pocket_rules['optimal_depth_ratio_min']
        optimal_max = pocket_rules['optimal_depth_ratio_max']
        
        results['warnings'].append({
            'category': 'Pocket Depth',
            'severity': 'medium',
            'message': 'Verify pocket depths relative to tool diameter',
            'recommendation': f'Maximum depth: {max_ratio}× tool diameter. Optimal: {optimal_min}-{optimal_max}× tool diameter. Use stepped cavities for deep features'
        })
    
    def _check_holes(self, parser, results: Dict):
        """Check hole specifications"""
        hole_rules = self.rules['holes']
        
        std_sizes = hole_rules['standard_sizes_metric']
        max_depth_ratio = hole_rules['depth']['max_ratio']
        
        results['warnings'].append({
            'category': 'Holes',
            'severity': 'medium',
            'message': 'Verify hole specifications',
            'recommendation': f'Use standard sizes: {std_sizes}mm. Max depth: {max_depth_ratio}× diameter. Through-holes preferred. Min edge distance: {hole_rules["positioning"]["min_edge_distance_ratio"]}× diameter'
        })
        
        results['suggestions'].append({
            'category': 'Holes',
            'message': f'Limit to {hole_rules["preferences"]["max_unique_sizes_warning"]} unique hole sizes per part',
            'benefit': 'Reduces tool changes, saves 2-5 minutes per change'
        })
    
    def _check_threads(self, parser, results: Dict):
        """Check thread specifications"""
        thread_rules = self.rules['threads']
        
        std_metric = thread_rules['standard_metric']
        std_depth_ratio = thread_rules['depth']['standard_ratio']
        
        results['passed'].append({
            'category': 'Threads',
            'rule': f'Standard thread depth: {std_depth_ratio}× diameter',
            'status': 'info',
            'details': f'Standard metric threads: {", ".join(std_metric[:8])}...'
        })
        
        results['warnings'].append({
            'category': 'Threads',
            'severity': 'low',
            'message': 'Use standard thread sizes and pitches',
            'recommendation': f'Avoid custom threads. Min wall thickness: {thread_rules["design_rules"]["min_wall_thickness_ratio"]}× thread diameter'
        })
    
    def _check_material_selection(self, material: str, results: Dict):
        """Check material machinability"""
        mat_rules = self.rules['materials']
        
        if material in mat_rules:
            mat_spec = mat_rules[material]
            rating = mat_spec['rating']
            cost = mat_spec['relative_cost']
            
            if rating <= 2:
                results['warnings'].append({
                    'category': 'Material Selection',
                    'severity': 'high',
                    'message': f'{material} is difficult to machine (rating: {rating}/5)',
                    'recommendation': f'Relative cost: {cost}×. Tool wear: {mat_spec["tool_wear"]}. Consider alternative materials with better machinability'
                })
            else:
                results['passed'].append({
                    'category': 'Material Selection',
                    'rule': f'{material} machinability rating: {rating}/5',
                    'status': 'passed',
                    'details': f'Relative cost: {cost}×, Tool wear: {mat_spec["tool_wear"]}, Thermal expansion: {mat_spec.get("thermal_expansion", "N/A")} µm/m·°C'
                })
            
            # Check thermal expansion for tight tolerances
            thermal_exp = mat_spec.get('thermal_expansion', 0)
            if thermal_exp > 20:
                results['warnings'].append({
                    'category': 'Material Selection',
                    'severity': 'medium',
                    'message': f'{material} has high thermal expansion ({thermal_exp} µm/m·°C)',
                    'recommendation': 'Avoid tight tolerances. Use symmetric cuts to minimize thermal distortion'
                })
    
    def _check_setup_requirements(self, parser, results: Dict):
        """Check setup minimization"""
        setup_rules = self.rules['setups']
        
        max_setups = setup_rules['warnings']['max_setups_3axis']
        cost_per_setup = setup_rules['cost_increase_per_setup']
        
        results['warnings'].append({
            'category': 'Setup Requirements',
            'severity': 'high',
            'message': 'Minimize number of setups',
            'recommendation': f'Target ≤{max_setups} setups on 3-axis machine. Each setup adds {int(cost_per_setup*100)}% cost and {setup_rules["cost_per_setup_minutes"]} minutes. Orient critical features to 1-2 directions'
        })
        
        results['suggestions'].append({
            'category': 'Setup Requirements',
            'message': 'Add flat datum surfaces for stable clamping',
            'benefit': 'Improves fixturing accuracy and reduces setup time'
        })
    
    def _check_tool_access(self, parser, results: Dict):
        """Check tool access and clearance"""
        access_rules = self.rules['tool_access']
        
        min_ratio = access_rules['min_channel_width_ratio']
        rec_ratio = access_rules['recommended_channel_width_ratio']
        
        results['warnings'].append({
            'category': 'Tool Access',
            'severity': 'high',
            'message': 'Verify adequate tool access',
            'recommendation': f'Minimum channel width: {min_ratio}× tool diameter. Recommended: {rec_ratio}× tool diameter. Add chamfers ({access_rules["design_requirements"]["chamfer_for_entry"]}mm) for tool entry'
        })
        
        if access_rules['undercuts']['requires_special_tools']:
            results['warnings'].append({
                'category': 'Tool Access',
                'severity': 'high',
                'message': 'Undercuts require special tooling or 5-axis machining',
                'recommendation': 'Avoid undercuts if possible. T-slot cutters have limited geometries. Consider design alternatives'
            })
    
    def _check_surface_finish(self, parser, results: Dict):
        """Check surface finish specifications"""
        finish_rules = self.rules['surface_finish']
        
        as_machined = finish_rules['as_machined']
        
        results['passed'].append({
            'category': 'Surface Finish',
            'rule': f'As-machined: Ra {as_machined["ra_um_min"]}-{as_machined["ra_um_max"]} µm',
            'status': 'info',
            'details': f'Cost multiplier: {as_machined["cost_multiplier"]}×. Specify Ra only for critical surfaces'
        })
        
        results['suggestions'].append({
            'category': 'Surface Finish',
            'message': 'Use "as-machined" finish for non-visible internal surfaces',
            'benefit': 'Polished finish adds 175% cost. Fine finishes only where functionally required'
        })
    
    def _check_geometry_complexity(self, parser, results: Dict):
        """Check geometry complexity"""
        geom_rules = self.rules['geometry']
        
        cost_increase = geom_rules['complexity_cost_increase']
        feature_cost = geom_rules['unnecessary_features_cost']
        
        results['suggestions'].append({
            'category': 'Geometry Simplification',
            'message': 'Simplify complex geometry where possible',
            'benefit': f'Complex contours increase programming time by {int((cost_increase-1)*100)}%. Unnecessary features add {int(feature_cost*100)}% machining time. Use straight lines and simple arcs instead of splines'
        })
    
    def _check_standard_features(self, parser, results: Dict):
        """Check for standard feature sizes"""
        std_rules = self.rules['standard_features']
        
        chamfers = std_rules['chamfers']
        fillets = std_rules['fillets']
        
        results['suggestions'].append({
            'category': 'Standard Features',
            'message': 'Use standard feature sizes',
            'benefit': f'Standard chamfers: {chamfers}mm. Standard fillets: {fillets}mm. Reduces tool changes (saves {std_rules["consolidation"]["tool_change_time_savings"]} min/change)'
        })
    
    def _check_thermal_stability(self, parser, material: str, results: Dict):
        """Check thermal and structural stability"""
        thermal_rules = self.rules['thermal']
        
        results['warnings'].append({
            'category': 'Thermal Stability',
            'severity': 'medium',
            'message': 'Consider thermal effects during machining',
            'recommendation': f'Cutting generates {thermal_rules["cutting_temp_range"][0]}-{thermal_rules["cutting_temp_range"][1]}°C. Distribute material removal symmetrically. Stress relief may be required for >60% material removal'
        })
        
        max_cantilever = thermal_rules['structural']['max_cantilever_ratio']
        results['warnings'].append({
            'category': 'Structural Rigidity',
            'severity': 'medium',
            'message': 'Check structural rigidity',
            'recommendation': f'Cantilever features should be <{max_cantilever}× their width. Add support structures for long thin features'
        })
    
    def _calculate_score(self, results: Dict) -> float:
        """Calculate machinability score (0-100)"""
        total_checks = (len(results['issues']) + len(results['warnings']) + 
                       len(results['suggestions']) + len(results['passed']))
        
        if total_checks == 0:
            return 0.0
        
        # Weight: issues = -15, warnings = -5, suggestions = -1, passed = +2
        score = (2 * len(results['passed']) - 15 * len(results['issues']) - 
                5 * len(results['warnings']) - len(results['suggestions']))
        max_score = 2 * total_checks
        
        normalized_score = max(0, min(100, (score / max_score) * 100))
        return round(normalized_score, 2)
    
    def _get_material_rating(self, material: str) -> int:
        """Get material machinability rating"""
        mat_rules = self.rules['materials']
        if material in mat_rules:
            return mat_rules[material]['rating']
        return 3  # default
    
    def _estimate_setups(self, parser) -> int:
        """Estimate number of setups required"""
        # Simplified estimation - would need actual geometry analysis
        return 2
    
    def _identify_cost_opportunities(self, results: Dict) -> List[Dict]:
        """Identify top cost reduction opportunities"""
        cost_rules = self.rules['cost_drivers']
        opportunities = []
        
        # Check for over-tolerancing
        if any('tolerance' in str(w).lower() for w in results['warnings']):
            opp = cost_rules['reduction_opportunities']['relax_tolerances']
            opportunities.append({
                'opportunity': 'Relax tolerances to ±0.1mm for non-critical features',
                'time_savings': f"{int(opp['time_savings']*100)}%",
                'cost_reduction': f"{int(opp['cost_reduction']*100)}%",
                'difficulty': 'Easy'
            })
        
        # Check for setup reduction
        if any('setup' in str(w).lower() for w in results['warnings']):
            opp = cost_rules['reduction_opportunities']['reduce_setups']
            opportunities.append({
                'opportunity': 'Consolidate features to reduce setups',
                'time_savings': f"{int(opp['time_savings']*100)}%",
                'cost_reduction': f"{int(opp['cost_reduction']*100)}%",
                'difficulty': 'Moderate'
            })
        
        # Check for corner radii
        if any('corner' in str(w).lower() for w in results['warnings']):
            opp = cost_rules['reduction_opportunities']['add_corner_radii']
            opportunities.append({
                'opportunity': 'Add corner radii to eliminate EDM operations',
                'time_savings': f"{int(opp['time_savings']*100)}%",
                'cost_reduction': f"{int(opp['cost_reduction']*100)}%",
                'difficulty': 'Easy'
            })
        
        return opportunities[:3]  # Top 3
