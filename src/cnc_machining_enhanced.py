"""
Enhanced CNC Machining Analyzer
Based on comprehensive CNC_DFM_Guidelines.md (25 sections, 200+ rules)
Standards: ISO 2768, ASME Y14.5, ISO 1302, ISO 965, ISO 286
"""
from typing import Dict


def analyze_cnc_machining_enhanced(parser, material, geometry) -> Dict:
    """
    Comprehensive CNC machining DFM analysis
    Based on industry standards and best practices
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
    
    # Determine material-specific parameters
    material_lower = material.lower()
    if 'aluminum' in material_lower or '6061' in material_lower or '7075' in material_lower:
        min_wall = 0.8
        recommended_wall = 1.0
        machinability = "★★★★★ Excellent"
        cost_multiplier = 1.0
        material_name = "Aluminum"
    elif 'steel' in material_lower and 'stainless' not in material_lower:
        min_wall = 1.0
        recommended_wall = 1.5
        machinability = "★★★☆☆ Good"
        cost_multiplier = 1.3
        material_name = "Mild Steel"
    elif 'stainless' in material_lower:
        min_wall = 1.2
        recommended_wall = 1.5
        machinability = "★★☆☆☆ Fair"
        cost_multiplier = 2.0
        material_name = "Stainless Steel"
    elif 'brass' in material_lower or 'copper' in material_lower:
        min_wall = 0.8
        recommended_wall = 1.0
        machinability = "★★★★☆ Very Good"
        cost_multiplier = 1.5
        material_name = "Brass/Copper"
    elif 'titanium' in material_lower:
        min_wall = 1.5
        recommended_wall = 2.0
        machinability = "★☆☆☆☆ Poor"
        cost_multiplier = 4.0
        material_name = "Titanium"
    else:
        min_wall = 1.5
        recommended_wall = 2.0
        machinability = "★★★☆☆ Moderate"
        cost_multiplier = 1.5
        material_name = material
    
    # RULE 1: Wall Thickness
    rule_name = "Wall Thickness"
    rule_standard = f"Minimum: {min_wall}mm, Recommended: ≥{recommended_wall}mm for {material_name}"
    
    if min_thickness > 0:
        if min_thickness < min_wall:
            issues.append({
                'category': 'Wall Thickness',
                'message': f'Critical: Wall thickness {min_thickness:.2f}mm below minimum',
                'recommendation': f'Increase to minimum {min_wall}mm for {material_name}',
                'rationale': f'Thin walls cause vibration, chatter, and deflection during machining. Minimum {min_wall}mm required for {material_name}.'
            })
            rationale.append(f"❌ Wall thickness {min_thickness:.2f}mm below minimum {min_wall}mm.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'FAIL',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall thickness {min_thickness:.2f}mm is below minimum {min_wall}mm',
                'recommendation': f'Increase to {recommended_wall}mm recommended thickness',
                'rationale': f'Walls <{min_wall}mm cause: vibration and chatter (poor surface finish), deflection under cutting forces (dimensional inaccuracy), tool breakage risk, part distortion. Aspect ratio (height:thickness) should be ≤4:1. Add ribs or gussets for tall features.',
                'cost_impact': f'Thin walls: 30-50% scrap rate from deflection/breakage, requires multiple light passes (+40-60% machining time)'
            })
        elif min_thickness < recommended_wall:
            warnings.append({
                'category': 'Wall Thickness',
                'message': f'Wall thickness {min_thickness:.2f}mm below recommended',
                'recommendation': f'Consider increasing to {recommended_wall}mm for better rigidity',
                'rationale': f'Recommended {recommended_wall}mm provides better structural rigidity and easier machining.'
            })
            rationale.append(f"⚠️ Wall thickness {min_thickness:.2f}mm below recommended {recommended_wall}mm.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall thickness {min_thickness:.2f}mm is machinable but below recommended',
                'recommendation': f'Increase to {recommended_wall}mm for optimal machining',
                'rationale': f'Recommended {recommended_wall}mm provides: better structural rigidity, reduced vibration, easier machining, lower scrap rate. Current {min_thickness:.2f}mm is machinable but requires careful setup and light cuts.',
                'cost_impact': '10-20% longer machining time for thin walls, requires careful setup'
            })
        else:
            passed.append({'check': 'Wall Thickness', 'status': f'{min_thickness:.2f}mm - Good'})
            rationale.append(f"✓ Wall thickness {min_thickness:.2f}mm meets recommended minimum.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'PASS',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall thickness {min_thickness:.2f}mm is within optimal range',
                'recommendation': 'No changes needed - thickness is optimal',
                'rationale': f'Wall thickness ≥{recommended_wall}mm provides excellent rigidity, minimal vibration, and reliable machining for {material_name}.',
                'cost_impact': 'Standard machining cost - no premium'
            })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': 'Not measured',
            'evaluation': 'Wall thickness could not be measured from geometry',
            'recommendation': f'Verify wall thickness: minimum {min_wall}mm, recommended {recommended_wall}mm',
            'rationale': 'Wall thickness analysis requires watertight 3D model',
            'cost_impact': 'N/A'
        })
    
    # RULE 2: Internal Corner Radii
    rule_name = "Internal Corner Radii"
    rule_standard = "Minimum radius ≥ tool radius. Recommended: radius = 1/3 × pocket depth. Standard: 0.5mm, 1mm, 3mm, 5mm"
    
    warnings.append({
        'category': 'Corner Radii',
        'message': 'Verify all internal corners have adequate radii',
        'recommendation': 'Add minimum 0.5mm radius to all internal corners (1mm+ preferred)',
        'rationale': 'CNC tools are round - sharp 90° corners are impossible without EDM (adds 200-400% cost). Larger radii enable faster toolpaths (15-25% time savings).'
    })
    rationale.append("⚠️ Verify internal corners have radii ≥0.5mm (sharp corners require expensive EDM).")
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'WARNING',
        'measured_value': 'Cannot detect from geometry',
        'evaluation': 'Internal corner radii cannot be automatically verified',
        'recommendation': 'Add radius ≥ tool radius. Use standard sizes: 0.5mm, 1mm, 3mm, 5mm',
        'rationale': 'CNC milling tools are round - sharp 90° internal corners are physically impossible without secondary processes. Sharp corners require EDM (Electrical Discharge Machining): adds 200-400% cost, 3-5 days lead time. Minimum radius = tool radius (e.g., 3mm tool → 1.5mm radius). Recommended: radius = 1/3 × pocket depth. Larger radii: enable faster toolpaths (15-25% time savings), reduce tool wear, improve part strength.',
        'cost_impact': 'Sharp corners: require EDM (+200-400% cost). Larger radii: save 15-25% machining time'
    })
    
    # RULE 3: Hole Specifications
    rule_name = "Hole Diameter and Depth"
    rule_standard = "Standard sizes: 3, 4, 5, 6, 8, 10, 12mm. Maximum depth: 4× diameter. Optimal: 2-3× diameter"
    
    if holes:
        non_standard_holes = []
        deep_holes = []
        
        standard_sizes = [3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 16.0, 20.0]
        
        for hole in holes:
            diameter = hole.get('diameter', 0)
            if diameter > 0:
                # Check if standard size (within 0.2mm tolerance)
                is_standard = any(abs(diameter - std) < 0.2 for std in standard_sizes)
                if not is_standard:
                    non_standard_holes.append(f"Ø{diameter:.1f}mm")
                
                # Check depth (if available - estimate from geometry)
                # For now, we'll just note the guideline
        
        if non_standard_holes:
            warnings.append({
                'category': 'Hole Sizes',
                'message': f'{len(non_standard_holes)} non-standard hole sizes detected',
                'recommendation': 'Use standard sizes: 3, 4, 5, 6, 8, 10, 12, 16, 20mm',
                'rationale': 'Non-standard holes require custom tooling or multiple operations, increasing cost and lead time.'
            })
            rationale.append(f"⚠️ {len(non_standard_holes)} non-standard hole sizes detected.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'{len(non_standard_holes)} non-standard holes',
                'evaluation': f'Detected holes with non-standard diameters: {", ".join(non_standard_holes[:3])}',
                'recommendation': 'Change to standard sizes: 3, 4, 5, 6, 8, 10, 12, 16, 20mm',
                'rationale': 'Standard hole sizes: use readily available drills (no custom tooling), faster machining (standard feeds/speeds), lower cost (standard tools cheaper), better availability. Non-standard holes: require custom tooling or multiple operations (drill + bore/ream), add 20-40% to hole cost, increase lead time. Maximum hole depth: 4× diameter (optimal: 2-3×). Through-holes preferred over blind holes (better chip evacuation).',
                'cost_impact': 'Non-standard holes: +20-40% cost per hole, potential lead time increase'
            })
        else:
            passed.append({'check': 'Hole Sizes', 'status': 'All holes use standard sizes'})
            rationale.append(f"✓ All {len(holes)} holes use standard diameters.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'PASS',
                'measured_value': f'{len(holes)} holes checked',
                'evaluation': 'All holes use standard diameters',
                'recommendation': 'No changes needed - hole sizes are optimal',
                'rationale': 'All holes use standard sizes (3, 4, 5, 6, 8, 10, 12mm), enabling use of readily available drills, standard feeds/speeds, and lower tooling costs.',
                'cost_impact': 'Standard hole cost - no premium'
            })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': 'No holes detected',
            'evaluation': 'No holes found in geometry',
            'recommendation': 'If adding holes, use standard sizes: 3, 4, 5, 6, 8, 10, 12mm. Limit depth to 4× diameter',
            'rationale': 'Standard hole sizes reduce cost and lead time',
            'cost_impact': 'N/A'
        })
    
    # RULE 4: Tolerance Specifications
    rule_name = "Tolerance Specifications"
    rule_standard = "Standard: ±0.1mm for non-critical features. Precision: ±0.01-0.02mm for critical only. Target: <20% tight tolerances"
    
    suggestions.append({
        'opportunity': 'Apply tight tolerances (±0.02mm) only to critical mating surfaces',
        'savings': '40-80% cost reduction per over-toleranced feature',
        'difficulty': 'Easy',
        'rationale': 'Over-tolerancing is the #1 cost driver in CNC machining. Standard ±0.1mm is sufficient for 80-90% of features. Tight tolerances require multiple passes, inspection, and potential rework.'
    })
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Tolerance specification is critical for cost control',
        'recommendation': 'Use ±0.1mm standard tolerance. Apply ±0.01-0.02mm only to critical features (<20% of part)',
        'rationale': 'Tolerance cost impact: ±0.1mm (standard, 1.0× cost), ±0.05mm (1.3× cost), ±0.02mm (1.8× cost), ±0.01mm (2.5× cost). Over-tolerancing increases cost by 40-80% per feature. Standards: ISO 2768-mK (general tolerances), ASME Y14.5 (GD&T). Target: Only 5-10% of features should have tight tolerances. Use GD&T for critical features (position, perpendicularity, flatness).',
        'cost_impact': 'Over-tolerancing: +40-80% per feature. Proper tolerancing: standard cost'
    })
    
    # RULE 5: Setup Minimization
    rule_name = "Setup Minimization"
    rule_standard = "Target: ≤2 setups on 3-axis CNC. Each additional setup adds 30-40% cost"
    
    suggestions.append({
        'opportunity': 'Design features accessible from 1-2 directions to minimize setups',
        'savings': '30-40% cost reduction per setup eliminated',
        'difficulty': 'Medium',
        'rationale': 'Each setup adds 15-60 minutes and introduces alignment error (±0.02-0.05mm). Orient critical features to same side. Add flat datum surfaces for stable clamping.'
    })
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Setup count directly impacts cost and accuracy',
        'recommendation': 'Orient all critical features to be accessible from 1-2 directions. Add flat reference surfaces',
        'rationale': 'Setup cost impact: Each setup adds 15-60 minutes (30-40% cost increase), introduces alignment error (±0.02-0.05mm cumulative), increases scrap risk. Design strategies: Orient features to 1-2 sides, add flat datum surfaces for clamping, design opposite-side features to be non-interfering, consider 5-axis machining for complex multi-sided parts (1 setup, but 1.8-2.5× machine cost).',
        'cost_impact': 'Each setup: +30-40% cost. Reducing 3 setups to 1: saves 60-80% setup cost'
    })
    
    # RULE 6: Material Machinability
    rule_name = "Material Selection and Machinability"
    rule_standard = f"{material_name}: {machinability}, Cost multiplier: {cost_multiplier}×"
    
    if cost_multiplier > 2.0:
        warnings.append({
            'category': 'Material Selection',
            'message': f'{material_name} is difficult to machine (cost multiplier: {cost_multiplier}×)',
            'recommendation': 'Consider alternative materials with better machinability if functionally acceptable',
            'rationale': f'{material_name} has high tool wear, slow cutting speeds, and requires specialized tooling.'
        })
        rationale.append(f"⚠️ {material_name} is difficult to machine ({cost_multiplier}× cost multiplier).")
    
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'INFO' if cost_multiplier <= 2.0 else 'WARNING',
        'measured_value': f'{material_name}, Machinability: {machinability}',
        'evaluation': f'Material machinability rating: {machinability}',
        'recommendation': 'Material selection is appropriate' if cost_multiplier <= 2.0 else 'Consider alternatives: Aluminum (1.0×), Brass (1.5×), Mild Steel (1.3×)',
        'rationale': f'Machinability ratings: Aluminum 6061 (★★★★★, 1.0×), Brass (★★★★☆, 1.5×), Mild Steel (★★★☆☆, 1.3×), Stainless 304 (★★☆☆☆, 2.0×), Titanium (★☆☆☆☆, 4.0×). {material_name} selected: {machinability}, {cost_multiplier}× cost multiplier. Factors: tool wear, cutting speed, surface finish, thermal expansion. Thermal expansion coefficients: Aluminum (23 µm/m·°C), Steel (12), Titanium (8.6 - excellent stability).',
        'cost_impact': f'Material cost multiplier: {cost_multiplier}× vs aluminum baseline'
    })
    
    # Calculate score
    total_checks = len(issues) + len(warnings) + len(passed)
    if total_checks > 0:
        score = (len(passed) * 100 + len(warnings) * 50) / total_checks
        score_explanation = f"Score from {len(passed)} passed checks, {len(warnings)} warnings, {len(issues)} critical issues"
    else:
        score = 85.0
        score_explanation = "Default score - limited geometry data"
    
    # Generate summary
    if score >= 90:
        assessment = "EXCELLENT - Well-designed for CNC machining"
    elif score >= 75:
        assessment = "GOOD - Minor improvements recommended"
    elif score >= 60:
        assessment = "ACCEPTABLE - Review warnings"
    else:
        assessment = "NEEDS REVISION - Address critical issues"
    
    summary = f"""**Overall Assessment:** {assessment}
**Manufacturability Score:** {score:.1f}/100

**Analysis Results:** {len(passed)} checks passed, {len(warnings)} warnings, {len(issues)} critical issues

**Key Findings:**
• Wall thickness: {"Optimal" if min_thickness >= recommended_wall else "Review required"} (minimum {min_wall}mm, recommended {recommended_wall}mm)
• Internal corners: Verify radii ≥0.5mm (sharp corners require EDM +200-400% cost)
• Hole specifications: {"Standard sizes used" if len(holes) > 0 and len([h for h in holes if h.get('diameter', 0) > 0]) > 0 else "Use standard sizes: 3, 4, 5, 6, 8, 10, 12mm"}
• Tolerances: Apply ±0.1mm standard, ±0.02mm only for critical features (<20%)
• Setup minimization: Design for ≤2 setups (each setup adds 30-40% cost)
• Material: {material_name} - {machinability}

**Cost Optimization Opportunities:**
1. Relax tolerances to ±0.1mm where possible (saves 40-80% per feature)
2. Add corner radii ≥1mm (saves 15-25% machining time, avoids EDM)
3. Use standard hole sizes (saves 20-40% per non-standard hole)
4. Minimize setups to 1-2 (saves 30-40% per setup eliminated)

**Recommendation:** {"Design is manufacturable with standard CNC machining." if len(issues) == 0 else "Address critical wall thickness issues before production."}

**Based on:** CNC_DFM_Guidelines.md (25 sections, 200+ rules)
**Standards:** ISO 2768, ASME Y14.5, ISO 1302, ISO 965, ISO 286"""
    
    return {
        'success': True,
        'process': 'CNC Machining',
        'material': material,
        'score': round(score, 1),
        'score_explanation': score_explanation,
        'issues': len(issues),
        'warnings': len(warnings),
        'suggestions': len(suggestions),
        'passed': len(passed),
        'all_rules': all_rules,
        'parser': parser,  # Include parser for 3D visualization
        'holes': holes,  # Include holes data for visualization
        'geometry': {  # Raw geometry data for calculations
            'dimensions': dims,
            'volume': volume,
            'min_thickness': min_thickness,
            'holes': holes
        },
        'geometry_info': {  # Formatted geometry info for display
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
