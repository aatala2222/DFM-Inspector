"""
Enhanced Injection Molding Analyzer - V2
Updated per Injection Molding DFM AME Presentation (Shinkansan, Aug 2023)
Author: Bruce Johnson – Sr. AME, Amazon Robotics

Key Updates:
- Material-specific wall thickness ranges
- Toolbound vs Non-toolbound tolerance matrix
- Rib design rules (base width, height, spacing)
- Draft angle requirements per feature type
- Snap fit design guidance
- Undercut handling (slides/lifters)
"""
from typing import Dict

# Material properties database (from Shinkansan presentation Slide 24)
MATERIAL_DATABASE = {
    'pom': {  # Acetal
        'name': 'POM (Acetal)',
        'type': 'crystalline',
        'wall_min': 0.75, 'wall_max': 3.00,
        'shrink': 0.020,  # mm/mm
        'cost_ratio': 1.00,
        'uses': 'gears, bearings, rollers',
        'pros': 'Low friction, chemical resistance, fatigue resistance',
        'cons': 'Low dimensional stability, high shrinkage, releases formaldehyde during processing'
    },
    'nylon': {  # PA, Nylon 6/6
        'name': 'Nylon (PA)',
        'type': 'crystalline',
        'wall_min': 0.25, 'wall_max': 3.00,
        'shrink': 0.015,
        'cost_ratio': 1.22,
        'uses': 'gears, bearings, chemical-resistant parts',
        'pros': 'Low friction, high chemical resistance, high flow rate',
        'cons': 'Hydroscopic (~5% moisture absorption), brittle when dry, dimensional instability'
    },
    'pp': {  # Polypropylene
        'name': 'Polypropylene (PP)',
        'type': 'crystalline',
        'wall_min': 0.60, 'wall_max': 3.80,
        'shrink': 0.018,
        'cost_ratio': 0.51,
        'uses': 'covers, living hinges, chemical-resistant parts',
        'pros': 'Low cost, chemical resistance, flexible (living hinge capable)',
        'cons': 'Very high shrinkage, low dimensional stability, soft surface'
    },
    'pbt': {
        'name': 'PBT (Polyester)',
        'type': 'crystalline',
        'wall_min': 0.60, 'wall_max': 3.20,
        'shrink': 0.016,
        'cost_ratio': 1.00,
        'uses': 'connectors, electronics housings',
        'pros': 'Chemical resistance, recyclable, high HDT (glass filled)',
        'cons': 'Brittle without fiber filler, low dimensional stability'
    },
    'pet': {
        'name': 'PET (Polyester)',
        'type': 'crystalline',
        'wall_min': 0.60, 'wall_max': 3.20,
        'shrink': 0.016,
        'cost_ratio': 0.96,
        'uses': 'connectors, housings',
        'pros': 'Chemical resistance, recyclable',
        'cons': 'Brittle without filler'
    },
    'abs': {
        'name': 'ABS',
        'type': 'amorphous',
        'wall_min': 1.00, 'wall_max': 3.50,
        'shrink': 0.006,
        'cost_ratio': 0.65,
        'uses': 'mechanical parts, case parts, internal parts',
        'pros': 'Low cost, good color matching, dimensional stability',
        'cons': 'Low chemical resistance, high friction coefficient'
    },
    'hips': {  # High-Impact Polystyrene
        'name': 'HIPS (Styrene)',
        'type': 'amorphous',
        'wall_min': 0.60, 'wall_max': 3.80,
        'shrink': 0.006,
        'cost_ratio': 0.57,
        'uses': 'trays, covers, non-critical internal parts',
        'pros': 'Low cost, dimensional stability, color matching',
        'cons': 'Low mechanical properties, low HDT (>70°C)'
    },
    'ppo': {  # Polyphenylene Oxide, also PPE
        'name': 'PPO / PPE (Noryl)',
        'type': 'amorphous',
        'wall_min': 1.00, 'wall_max': 3.50,
        'shrink': 0.007,
        'cost_ratio': 1.23,
        'uses': 'parts requiring high stability and chemical resistance',
        'pros': 'High dimensional stability, chemical resistance',
        'cons': 'Yellows with aging, limited color matching, higher cost'
    },
    'pc': {  # Polycarbonate
        'name': 'Polycarbonate (PC)',
        'type': 'amorphous',
        'wall_min': 1.00, 'wall_max': 3.80,
        'shrink': 0.006,
        'cost_ratio': 1.32,
        'uses': 'case parts, critical internal parts, product chassis, transparent parts',
        'pros': 'High dimensional stability, high impact, transparent',
        'cons': 'Low chemical resistance, scratch sensitive, pre-molding handling critical'
    },
    'pmma': {  # Acrylic
        'name': 'PMMA (Acrylic)',
        'type': 'amorphous',
        'wall_min': 1.00, 'wall_max': 3.80,
        'shrink': 0.004,
        'cost_ratio': 0.78,
        'uses': 'light pipes, windows, lenses, buttons',
        'pros': 'High dimensional stability, transparency, light transmittance',
        'cons': 'Low chemical resistance, high brittleness, notch sensitivity, stress cracks'
    },
    'san': {
        'name': 'SAN (Styrene-Acrylonitrile)',
        'type': 'amorphous',
        'wall_min': 0.80, 'wall_max': 3.80,
        'shrink': 0.004,
        'cost_ratio': 0.99,
        'uses': 'lenses, light pipes, case part windows',
        'pros': 'Low shrinkage, hard surface, transparent, low cost',
        'cons': 'High brittleness, complex geometries sensitive to ejection cracking'
    }
}


def get_material_info(material: str) -> Dict:
    """Look up material properties, fuzzy-matched"""
    material_lower = material.lower().replace(' ', '').replace('(', '').replace(')', '')
    
    # Direct matches
    for key, info in MATERIAL_DATABASE.items():
        if key in material_lower:
            return info
    
    # Aliases
    if 'acetal' in material_lower or 'delrin' in material_lower:
        return MATERIAL_DATABASE['pom']
    if 'polyamide' in material_lower:
        return MATERIAL_DATABASE['nylon']
    if 'polypropylene' in material_lower:
        return MATERIAL_DATABASE['pp']
    if 'polycarbonate' in material_lower:
        return MATERIAL_DATABASE['pc']
    if 'acrylic' in material_lower:
        return MATERIAL_DATABASE['pmma']
    if 'noryl' in material_lower:
        return MATERIAL_DATABASE['ppo']
    
    # Default
    return {
        'name': material,
        'type': 'unknown',
        'wall_min': 1.0, 'wall_max': 3.5,
        'shrink': 0.010,
        'cost_ratio': 1.0,
        'uses': 'General purpose',
        'pros': 'Verify with supplier',
        'cons': 'Material not in database - verify specifications'
    }


def get_tolerance(feature_size_mm: float, toolbound: bool = True, fine: bool = False) -> float:
    """
    Get tolerance per Shinkansan default spec (Slide 29).
    
    Args:
        feature_size_mm: Feature size in mm
        toolbound: True if dimension is within single non-moving tool piece (tighter)
        fine: True for fine tolerance (requires AME approval)
    """
    # Toolbound commercial tolerances
    toolbound_commercial = [
        (10, 0.100), (25, 0.125), (50, 0.150), (75, 0.200),
        (100, 0.225), (150, 0.250), (200, 0.500), (250, 0.650),
        (300, 0.800), (350, 0.950), (400, 1.100), (450, 1.250),
    ]
    # Toolbound fine tolerances
    toolbound_fine = [
        (10, 0.050), (25, 0.075), (50, 0.100), (75, 0.125),
        (100, 0.150), (150, 0.175), (200, 0.275), (250, 0.375),
        (300, 0.475), (350, 0.575), (400, 0.675), (450, 0.775),
    ]
    # Non-toolbound commercial tolerances
    nontb_commercial = [
        (10, 0.200), (25, 0.225), (50, 0.250), (75, 0.300),
        (100, 0.350), (150, 0.400), (200, 0.600), (250, 0.750),
        (300, 0.900), (350, 1.050), (400, 1.200), (450, 1.350),
    ]
    # Non-toolbound fine tolerances
    nontb_fine = [
        (10, 0.100), (25, 0.125), (50, 0.150), (75, 0.175),
        (100, 0.200), (150, 0.225), (200, 0.325), (250, 0.425),
        (300, 0.525), (350, 0.625), (400, 0.725), (450, 0.825),
    ]
    
    if toolbound and fine:
        table = toolbound_fine
    elif toolbound:
        table = toolbound_commercial
    elif fine:
        table = nontb_fine
    else:
        table = nontb_commercial
    
    for size_limit, tol in table:
        if feature_size_mm <= size_limit:
            return tol
    return table[-1][1]  # Use largest if exceeds table


def analyze_injection_molding_enhanced_v2(parser, material, geometry) -> Dict:
    """
    Comprehensive injection molding DFM analysis per Shinkansan Aug 2023 guidelines.
    """
    issues = []
    warnings = []
    suggestions = []
    passed = []
    rationale = []
    all_rules = []
    
    dims = geometry.get('dimensions', {})
    volume = geometry.get('volume', 0)
    min_thickness = geometry.get('estimated_min_thickness', 0)
    holes = geometry.get('holes', [])
    
    # Get material info
    mat = get_material_info(material)
    
    # RULE 1: Wall Thickness - Material-specific
    rule_name = "Wall Thickness (material-specific)"
    rule_standard = f"{mat['name']}: {mat['wall_min']}-{mat['wall_max']}mm per typical range. Shinkansan Aug 2023."
    
    if min_thickness > 0:
        if min_thickness < mat['wall_min']:
            issues.append({
                'category': 'Wall Thickness',
                'message': f'Wall {min_thickness:.2f}mm below {mat["name"]} minimum {mat["wall_min"]}mm',
                'recommendation': f'Increase to {mat["wall_min"]}-{mat["wall_max"]}mm range',
                'rationale': f'{mat["name"]} requires {mat["wall_min"]}mm minimum wall for proper fill. Thinner walls cause short shots and sink marks.'
            })
            rationale.append(f"❌ Wall {min_thickness:.2f}mm < {mat['name']} minimum {mat['wall_min']}mm")
            all_rules.append({
                'name': rule_name, 'standard': rule_standard, 'status': 'FAIL',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall thickness {min_thickness:.2f}mm is below {mat["name"]} minimum {mat["wall_min"]}mm',
                'recommendation': f'Increase to typical range {mat["wall_min"]}-{mat["wall_max"]}mm for {mat["name"]}',
                'rationale': f'{mat["name"]} properties: {mat["pros"]}. Key challenges: {mat["cons"]}. Shrinkage: {mat["shrink"]*100:.2f}%. Wall thickness affects flow length, cooling, and shrinkage uniformity.',
                'cost_impact': f'Thin walls: short shots (25-40% scrap), sink marks, requires higher injection pressure (+machine wear)'
            })
        elif min_thickness > mat['wall_max']:
            warnings.append({
                'category': 'Wall Thickness',
                'message': f'Wall {min_thickness:.2f}mm above {mat["name"]} typical max {mat["wall_max"]}mm',
                'recommendation': f'Core out thick sections or reduce to {mat["wall_max"]}mm',
                'rationale': 'Thick walls cause sink marks, void formation, longer cycle times.'
            })
            all_rules.append({
                'name': rule_name, 'standard': rule_standard, 'status': 'WARNING',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall {min_thickness:.2f}mm exceeds typical max {mat["wall_max"]}mm for {mat["name"]}',
                'recommendation': f'Core out thick sections (add cored pockets) to maintain uniform wall ≤{mat["wall_max"]}mm',
                'rationale': 'Thick walls: (1) Sink marks from non-uniform cooling, (2) Void formation in core, (3) 30-60% longer cycle time, (4) Warpage from differential shrinkage.',
                'cost_impact': 'Thick walls: +30-60% cycle time (+$0.10-$0.30/part), sink marks require cosmetic rework.'
            })
        else:
            passed.append({'check': 'Wall Thickness', 'status': f'{min_thickness:.2f}mm optimal'})
            all_rules.append({
                'name': rule_name, 'standard': rule_standard, 'status': 'PASS',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall {min_thickness:.2f}mm is within {mat["name"]} optimal range',
                'recommendation': 'No changes needed',
                'rationale': f'Wall thickness optimal for {mat["name"]}. Material type: {mat["type"]}. Shrinkage: {mat["shrink"]*100:.2f}%.',
                'cost_impact': 'Standard cycle time'
            })
    
    # RULE 2: Uniform Wall Thickness
    rule_name = "Uniform Wall Thickness"
    rule_standard = "Maintain uniform wall thickness. Abrupt changes cause sink, warpage, weld lines."
    
    suggestions.append({
        'opportunity': 'Maintain wall thickness within ±10% across the part',
        'savings': 'Reduces sink, warpage, and rejection rate',
        'difficulty': 'Medium'
    })
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Wall thickness variation requires CAD review',
        'recommendation': 'Core out thick sections. Avoid abrupt transitions - use gradual tapers. Keep rib base thickness 50-60% of wall.',
        'rationale': 'Non-uniform walls: (1) Differential shrinkage → warpage, (2) Sink marks over thick areas, (3) Weld lines at flow fronts from different thicknesses, (4) Internal stress.',
        'cost_impact': 'Non-uniform walls: 15-25% higher scrap, cosmetic issues, may require secondary operations'
    })
    
    # RULE 3: Draft Angles
    rule_name = "Draft Angles"
    rule_standard = "3° minimum draft on all vertical walls. 5° on shutoffs (Shinkansan Slides 35-37)"
    
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Draft angles cannot be automatically measured - verify in CAD',
        'recommendation': 'All vertical walls: 3° minimum draft. Shutoff surfaces (steel-to-steel cavity/core contact): 5° minimum. Rib sides: 0.5° minimum.',
        'rationale': 'Without draft: parts stick to core (cold plastic shrinks onto core), causing: warpage, ejection damage, drag marks. Draft on ribs enables proper release. Shutoff draft prevents mold damage.',
        'cost_impact': 'No-draft walls: 20-40% ejection failures, require post-CNC or side-action tooling (+10-30% tool cost)'
    })
    
    # RULE 4: Rib Design
    rule_name = "Rib Design"
    rule_standard = "Rib base = 50-60% of wall thickness, height ≤ 3T, spacing ≥ 3T (Shinkansan Slide 38)"
    
    if min_thickness > 0:
        rib_base_max = 0.6 * min_thickness
        rib_base_min = 0.5 * min_thickness
        rib_height_max = 3.0 * min_thickness
        rib_spacing_min = 3.0 * min_thickness
        
        suggestions.append({
            'opportunity': f'Design ribs: base {rib_base_min:.2f}-{rib_base_max:.2f}mm, height ≤{rib_height_max:.1f}mm, spacing ≥{rib_spacing_min:.1f}mm',
            'savings': 'Prevents sink marks, ensures moldability',
            'difficulty': 'Easy'
        })
        all_rules.append({
            'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
            'measured_value': 'Design consideration',
            'evaluation': f'Rib design rules for {min_thickness:.2f}mm walls:',
            'recommendation': f'Rib base: {rib_base_min:.2f}-{rib_base_max:.2f}mm (50-60% of wall). Rib height: ≤{rib_height_max:.1f}mm (3×T). Rib spacing: ≥{rib_spacing_min:.1f}mm (3×T). Rib draft: 0.5° min. Base fillet: 0.4mm min.',
            'rationale': 'Rib base >60% wall: sink marks visible. Height >3×T: difficult fill, sticks in mold. Spacing <3×T: mold steel overheats between ribs and breaks.',
            'cost_impact': 'Incorrect rib design: cosmetic sink marks, mold damage, 20-30% scrap rate'
        })
    
    # RULE 5: Fillets and Radii
    rule_name = "Fillets and Radii"
    rule_standard = "External R = internal r + wall thickness. Internal r = 25-60% of wall, minimum 0.4mm (Shinkansan Slide 39)"
    
    if min_thickness > 0:
        min_fillet = max(0.4, 0.25 * min_thickness)
        max_fillet = 0.6 * min_thickness
        
        all_rules.append({
            'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
            'measured_value': 'Design consideration',
            'evaluation': f'Fillet rules for {min_thickness:.2f}mm walls:',
            'recommendation': f'Internal fillets: {min_fillet:.2f}-{max_fillet:.2f}mm (25-60% of wall, min 0.4mm). External radius = internal + {min_thickness:.2f}mm (wall thickness).',
            'rationale': 'Sharp corners: (1) Stress concentrations causing cracking, (2) Difficult mold fabrication, (3) Flow hesitation. Uniform wall at corners requires external R = internal r + T.',
            'cost_impact': 'Sharp corners: part cracking in service, mold wear. Proper radii: standard mold life.'
        })
    
    # RULE 6: Shrinkage and Warpage
    rule_name = "Shrinkage Considerations"
    rule_standard = f"{mat['name']} shrinkage: {mat['shrink']*100:.2f}% in flow direction"
    
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': f'{mat["shrink"]*100:.2f}%',
        'evaluation': f'Account for {mat["name"]} shrinkage in tolerances and mating features',
        'recommendation': f'Tool dimensions must account for {mat["shrink"]*100:.2f}% shrinkage. Glass-filled variants reduce shrinkage. {mat["type"].capitalize()} polymer — {"fillers affect shrinkage direction" if mat["type"]=="crystalline" else "low shrinkage anisotropy"}.',
        'rationale': f'{mat["type"].capitalize()} polymers: {"higher shrinkage, anisotropic (different in flow vs cross-flow)" if mat["type"]=="crystalline" else "lower shrinkage, more isotropic"}. Adjust tool by supplier calculation.',
        'cost_impact': 'Incorrect shrink allowance: parts out of tolerance, requires mold rework ($5K-$30K)'
    })
    
    # RULE 7: Undercuts and Slides
    rule_name = "Undercuts and Side Action"
    rule_standard = "External undercuts require slides, internal require lifters. Each adds tool cost/maintenance."
    
    suggestions.append({
        'opportunity': 'Review design for features parallel to mold opening',
        'savings': 'Eliminating 1 slide saves ~10% tool cost ($2K-$15K)',
        'difficulty': 'Medium'
    })
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Undercuts cannot be auto-detected reliably',
        'recommendation': 'External undercuts: consider slides (side-action) or redesign. Internal undercuts: use lifters or pass cores when possible. Shallow undercuts sometimes moldable with flex.',
        'rationale': 'Slides: adds tooling complexity (+10% tool cost each), more maintenance. Lifters: similar complexity. Pass cores: simpler but require parting line access.',
        'cost_impact': 'Each slide/lifter: +$2K-$15K tool cost, +15% maintenance over tool life'
    })
    
    # RULE 8: Snap Fit Design
    rule_name = "Snap Fit Design"
    rule_standard = "Snaps should not be loaded in snapped position (creep). Taper beam. Use pass core."
    
    suggestions.append({
        'opportunity': 'Design snap fits with no steady-state load',
        'savings': 'Prevents creep failure over time',
        'difficulty': 'Medium'
    })
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Snap fit features require manual design review',
        'recommendation': 'Snaps not under load when snapped (creep causes relaxation). Use pass cores for hooks when possible. Taper snap beam for even stress distribution.',
        'rationale': 'Plastic creep under sustained load: snap fits lose engagement force over weeks/months. Tapered beams: more uniform stress. Pass cores eliminate need for slides on hooks.',
        'cost_impact': 'Poor snap design: field failures (warranty claims $$), tool complexity for alternatives'
    })
    
    # RULE 9: Tolerance Specification
    rule_name = "Tolerance Specification"
    rule_standard = "Use toolbound commercial tolerances where possible. Fine tolerances require AME approval."
    
    if dims:
        max_dim = max(dims.values())
        tb_commercial = get_tolerance(max_dim, toolbound=True, fine=False)
        ntb_commercial = get_tolerance(max_dim, toolbound=False, fine=False)
        
        all_rules.append({
            'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
            'measured_value': f'Max dim {max_dim:.1f}mm',
            'evaluation': f'Default tolerances for {max_dim:.1f}mm features (Shinkansan Slide 29):',
            'recommendation': f'Toolbound commercial: ±{tb_commercial:.3f}mm. Non-toolbound commercial: ±{ntb_commercial:.3f}mm. Use fine tolerances only where critical.',
            'rationale': 'Toolbound: dimensions within single non-moving tool piece (tighter). Non-toolbound: across parting line, lifters, slides, cavity-to-core (looser). Tightening beyond fine tolerances prohibited without AME approval.',
            'cost_impact': 'Tight tolerances: 20-40% cost premium per dimension. Over-tolerancing is #1 cost driver.'
        })
    
    # Calculate score
    total_checks = len(issues) + len(warnings) + len(passed)
    if total_checks > 0:
        score = (len(passed) * 100 + len(warnings) * 50) / total_checks
    else:
        score = 75.0
    
    score_explanation = f"Score: {len(passed)} passed, {len(warnings)} warnings, {len(issues)} critical"
    
    if score >= 90:
        assessment = "EXCELLENT - Well-designed for injection molding"
    elif score >= 75:
        assessment = "GOOD - Minor improvements recommended"
    elif score >= 60:
        assessment = "ACCEPTABLE - Review warnings"
    else:
        assessment = "NEEDS REVISION - Address critical issues"
    
    summary = f"""**Process:** Injection Molding
**Material:** {mat['name']} ({mat['type'].capitalize()} thermoplastic)
**Overall Assessment:** {assessment}
**Manufacturability Score:** {score:.1f}/100

**Material Properties:**
• Wall thickness range: {mat['wall_min']}-{mat['wall_max']}mm
• Shrinkage: {mat['shrink']*100:.2f}% in flow direction
• Cost ratio: {mat['cost_ratio']}x baseline
• Typical uses: {mat['uses']}
• Advantages: {mat['pros']}
• Considerations: {mat['cons']}

**Analysis Results:** {len(passed)} passed, {len(warnings)} warnings, {len(issues)} critical

**Key Design Points per Shinkansan Aug 2023:**
1. Uniform wall thickness ({mat['wall_min']}-{mat['wall_max']}mm for {mat['name']})
2. All walls: 3° minimum draft (5° on shutoffs)
3. Ribs: base 50-60% wall, height ≤3T, spacing ≥3T
4. Fillets: internal 0.4mm+ (25-60% of wall), external = internal + T
5. Snap fits: no steady-state load, taper beam
6. Minimize slides/lifters (each +10% tool cost)

**Reference:** Injection Molding DFM AME Presentation, Bruce Johnson, Shinkansan Aug 2023
"""
    
    return {
        'success': True,
        'process': 'Injection Molding',
        'material': mat['name'],
        'score': round(score, 1),
        'score_explanation': score_explanation,
        'issues': len(issues),
        'warnings': len(warnings),
        'suggestions': len(suggestions),
        'passed': len(passed),
        'all_rules': all_rules,
        'parser': parser,
        'holes': holes,
        'geometry': {
            'dimensions': dims,
            'volume': volume,
            'min_thickness': min_thickness,
            'holes': holes
        },
        'geometry_info': {
            'dimensions': f"{dims.get('x', 0):.1f} x {dims.get('y', 0):.1f} x {dims.get('z', 0):.1f} mm",
            'volume': f"{volume:.2f} mm³",
            'min_thickness': f"{min_thickness:.2f} mm" if min_thickness > 0 else 'N/A',
            'holes_detected': len(holes)
        },
        'rationale': rationale,
        'summary': summary,
        'details': {
            'critical_issues': issues[:5],
            'warnings': warnings[:5],
            'cost_savings': suggestions[:5]
        }
    }
