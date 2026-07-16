#!/usr/bin/env python3
"""
Integration script to merge enhanced DFM rules into the system
Incorporates Process Specs requirements into active inspection rules
"""

import yaml
import os
from pathlib import Path
from datetime import datetime

def load_yaml(filepath):
    """Load YAML file"""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def save_yaml(data, filepath):
    """Save YAML file"""
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def merge_injection_molding_rules():
    """Merge enhanced injection molding rules"""
    print("\n" + "="*70)
    print("INTEGRATING INJECTION MOLDING RULES")
    print("="*70)
    
    enhanced = load_yaml('config/injection_molding_rules_enhanced.yaml')
    current = load_yaml('config/inspection_rules.yaml')
    
    # Update wall thickness rules
    current['wall_thickness'] = {
        'nominal_minimum': 3.0,
        'nominal_preferred': 3.5,
        'critical_minimum': 2.0,
        'min_thickness': 3.0,
        'max_thickness': 10.0,
        'uniform_variation_max': 1.5,
        'transition_gradient_max': 0.2,
        'notes': 'Based on 930-00164_R01'
    }
    
    # Update draft angles
    current['draft_angles'] = {
        'min_draft_smooth': 1.5,
        'min_draft_textured': 2.0,
        'recommended_draft': 2.0,
        'notes': 'Injection molding requires 1.5° minimum'
    }
    
    # Add injection molding specific rules
    current['injection_molding'] = {
        'process_name': 'Thermoplastic Injection Molding',
        'specification': '930-00164_R01',
        'wall_thickness': {
            'nominal': 3.0,
            'preferred': 3.5,
            'minimum': 2.0
        },
        'draft_angle': {
            'minimum': 1.5,
            'recommended': 2.0
        },
        'radii': {
            'inside_minimum': 0.5,
            'inside_preferred': 1.0,
            'external_formula': 'inside_radius + wall_thickness'
        },
        'parting_line': 'Keep as simple as possible',
        'gates': 'Optimize for material flow',
        'ribs': {
            'thickness_ratio': 0.5,
            'height_max_ratio': 3.0
        },
        'bosses': {
            'height_max_ratio': 3.0,
            'diameter_ratio': 1.5
        },
        'tolerances': {
            'fractional': '±0.031 in (±0.79 mm)',
            'decimal': '±0.010 in (±0.25 mm)',
            'angular': '±1° to ±2°'
        }
    }
    
    print("✓ Injection molding rules updated")
    return current

def merge_die_casting_rules():
    """Merge enhanced die casting rules"""
    print("\n" + "="*70)
    print("INTEGRATING DIE CASTING RULES")
    print("="*70)
    
    enhanced = load_yaml('config/die_casting_rules_enhanced.yaml')
    current = load_yaml('config/inspection_rules.yaml')
    
    # Add die casting specific rules
    current['die_casting'] = {
        'process_name': 'High Pressure Die Casting & Permanent Mold',
        'specification': '930-00166_R01',
        'process_selection': {
            'hpdc': {
                'max_projected_area': 5500,
                'min_wall_thickness': 3.0,
                'max_wall_thickness': 10.0,
                'draft_angle_minimum': 1.5,
                'profile_tolerance': '0.5-1.5 mm',
                'surface_finish': '60-120 RMS',
                'cycle_time': '60-100 seconds',
                'strength_advantage': '30-50% vs gravity casting'
            },
            'permanent_mold': {
                'min_wall_thickness': 4.0,
                'draft_angle_minimum': 3.0,
                'profile_tolerance': '2.6-3.6 mm',
                'surface_finish': '250-420 RMS',
                'cycle_time': '240-280 seconds',
                'tooling_cost_lower': True
            }
        },
        'wall_thickness': {
            'hpdc_nominal': 3.0,
            'hpdc_max': 10.0,
            'permanent_mold_nominal': 4.0
        },
        'draft_angle': {
            'hpdc_minimum': 1.5,
            'permanent_mold_minimum': 3.0
        },
        'radii': {
            'inside_minimum': 0.5,
            'inside_preferred': 1.0
        },
        'undercuts': 'Minimize or use side action (10% tooling cost)',
        'machining_stock': {
            'hpdc': 1.0,
            'permanent_mold': 1.5
        },
        'tolerances': {
            'hpdc_profile': '0.5-1.5 mm',
            'hpdc_dimensional': '0.002 mm/mm',
            'permanent_mold_profile': '2.6-3.6 mm',
            'permanent_mold_dimensional': '0.38 mm + 0.002 mm/mm'
        }
    }
    
    print("✓ Die casting rules updated")
    return current

def merge_sheet_metal_rules():
    """Merge enhanced sheet metal rules"""
    print("\n" + "="*70)
    print("INTEGRATING SHEET METAL RULES")
    print("="*70)
    
    enhanced = load_yaml('config/sheet_metal_rules_enhanced.yaml')
    current = load_yaml('config/inspection_rules.yaml')
    
    # Add sheet metal specific rules
    current['sheet_metal'] = {
        'process_name': 'Sheet Metal Fabrication',
        'specification': '930-00172_R01',
        'processes': {
            'turret_press': 'Prototypes, low volume',
            'laser_cutting': 'Complex geometry, no tooling',
            'hand_brake': 'Low cost, manual',
            'progressive_die': 'High volume, automated',
            'multi_slide': 'Complex parts, high volume',
            'fine_blanking': 'Precision, tight tolerances'
        },
        'bend_radius': {
            'minimum_standard': 1.0,
            'minimum_low_carbon': 0.5,
            'formula': 'max(1.0T, 0.6mm)'
        },
        'bend_relief': {
            'required': 'When bend close to edge',
            'depth_minimum': 'Greater than bend radius',
            'width_minimum': 'Material thickness'
        },
        'hole_distance_from_bend': {
            'minimum_a': '2.0T + R',
            'recommended_b': '3T + R'
        },
        'slot_distance_from_bend': {
            'short_slot_l_less_50mm': '3T + R',
            'long_slot_l_greater_50mm': '4T + R'
        },
        'feature_spacing': {
            'hole_to_hole': '1.2T',
            'extrusion_spacing': '6T',
            'extrusion_to_edge': '3T + 2R',
            'extrusion_to_bend': '3T + R'
        },
        'dimples': {
            'max_diameter': '6T',
            'max_height': '4T',
            'min_height': 'D * 0.3',
            'to_hole_distance': '3T',
            'to_dimple_distance': '4T + D',
            'to_bend_distance': '2T',
            'to_edge_distance': '3T + D/2',
            'angle_minimum': 30
        },
        'tolerances': {
            'turret_press': '±0.10 in',
            'laser_cutting': '±0.10 in',
            'hand_brake': '±0.5 in (fold-fold)',
            'progressive_die': '±0.05 in',
            'multi_slide': '±0.05 in',
            'fine_blanking': '±0.03 in'
        }
    }
    
    print("✓ Sheet metal rules updated")
    return current

def merge_welding_rules():
    """Merge enhanced welding rules"""
    print("\n" + "="*70)
    print("INTEGRATING WELDING RULES")
    print("="*70)
    
    enhanced = load_yaml('config/welding_rules_enhanced.yaml')
    current = load_yaml('config/inspection_rules.yaml')
    
    # Add welding specific rules
    current['welding'] = {
        'process_name': 'Weldments',
        'specification': '960-00169_R01',
        'standards': {
            'aws_d1_1': 'Carbon and low alloy steels (≥3mm)',
            'aws_d1_2': 'Aluminum structural alloys',
            'aws_d1_3': 'Structural sheet steels (<5mm)',
            'aws_d1_6': 'Stainless steel (≥1.5mm)'
        },
        'weld_access': {
            'gun_access_required': True,
            'angle_optimization': 'Critical for fusion',
            'visibility_required': True
        },
        'groove_angle': {
            'carbon_steel': '50-60°',
            'aluminum': '60-65°',
            'stainless_steel': '55-60°'
        },
        'root_opening': 'Affects fusion and penetration',
        'root_face': {
            'bevel_angle_le_30': 0,
            'bevel_angle_gt_30': 1.0
        },
        'fillet_weld': {
            'leg_size_adequate': True,
            'effective_throat_calculated': True
        },
        'skewed_joints': {
            'inclination_lt_10': 'Use fillet weld',
            'inclination_ge_10': 'Beveling mandatory'
        },
        'qualification': {
            'wps_required': True,
            'pqr_required': True,
            'wpqr_required': True
        },
        'design_for_manufacturing': {
            'drain_holes': 'For cleaning',
            'outgassing_holes': 'For all-around welds',
            'fixturing_reviewed': True,
            'hang_locations_identified': True
        }
    }
    
    print("✓ Welding rules updated")
    return current

def main():
    """Main integration function"""
    print("\n" + "="*70)
    print("ENHANCED DFM RULES INTEGRATION")
    print("="*70)
    print(f"Integration Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load current rules
    current_rules = load_yaml('config/inspection_rules.yaml')
    
    # Merge all enhanced rules
    current_rules = merge_injection_molding_rules()
    current_rules = merge_die_casting_rules()
    current_rules = merge_sheet_metal_rules()
    current_rules = merge_welding_rules()
    
    # Add integration metadata
    current_rules['integration_metadata'] = {
        'date': datetime.now().isoformat(),
        'version': '2.0',
        'source_documents': [
            '930-00164_R01 - Injection Molding',
            '930-00166_R01 - Die Casting & Permanent Mold',
            '930-00172_R01 - Sheet Metal',
            '960-00169_R01 - Weldments'
        ],
        'enhancements': [
            'Process selection logic',
            'Undercut handling',
            'Machining stock allowance',
            'Bend relief requirements',
            'Feature spacing rules',
            'Weld access design',
            'Groove angle specifications',
            'Skewed joint handling'
        ]
    }
    
    # Save updated rules
    save_yaml(current_rules, 'config/inspection_rules.yaml')
    
    print("\n" + "="*70)
    print("INTEGRATION COMPLETE")
    print("="*70)
    print("\n✓ Enhanced rules integrated into config/inspection_rules.yaml")
    print("✓ Ready for next DFM inspection run")
    print("\nKey Updates:")
    print("  • Injection Molding: Wall thickness, draft, radii, parting line")
    print("  • Die Casting: Process selection, undercuts, machining stock")
    print("  • Sheet Metal: Bend relief, feature spacing, dimple design")
    print("  • Welding: Weld access, groove angles, skewed joints")
    print("\nNext Steps:")
    print("  1. Run DFM inspection on your next CAD model")
    print("  2. Review enhanced rule checks in the report")
    print("  3. Verify compliance with Process Specs")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
