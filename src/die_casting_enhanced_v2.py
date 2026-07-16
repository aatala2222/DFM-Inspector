"""
Enhanced Die Casting Analyzer - V2 (Updated per 930-00166_R01 + NADCA 11th Edition)
Supports: High Pressure Die Casting (HPDC), Low Pressure Die Casting (LPDC), Gravity/Tilt Pour

Key References:
- 930-00166_R01 DESIGN GUIDELINE, HIGH PRESSURE DIE CAST AND GRAVITY CAST PERMANENT MOLD
- NADCA Product Specification Standards for Die Castings - 11th Edition
- Standards for Aluminum Sand and Permanent Mold Castings - 16th Edition 2021
- East West Manufacturing Die Casting Training (2021)
- Milan Lucic, Sr. AME Mobility: Casting DFM AME Presentation (Aug 2023)
"""
from typing import Dict


def analyze_die_casting_enhanced_v2(parser, material, geometry, process_type='hpdc') -> Dict:
    """
    Comprehensive die casting DFM analysis per updated AR guidelines.
    
    Args:
        parser: CAD parser with geometry data
        material: Material name (e.g., 'Aluminum A380', 'AlSi12Fe')
        geometry: Geometry dict with dimensions, thickness, holes, bends, etc.
        process_type: 'hpdc' (High Pressure), 'lpdc' (Low Pressure), or 'gravity' (Gravity/Tilt Pour)
    """
    issues = []
    warnings = []
    suggestions = []
    passed = []
    rationale = []
    all_rules = []
    
    dims = geometry.get('dimensions', {})
    volume = geometry.get('volume', 0)
    surface_area = geometry.get('surface_area', 0)
    min_thickness = geometry.get('estimated_min_thickness', 0)
    holes = geometry.get('holes', [])
    
    # Process-specific parameters per 930-00166
    if process_type == 'hpdc':
        process_name = 'High Pressure Die Casting (HPDC)'
        min_wall = 2.5       # Minimum feature thickness
        nominal_wall = 3.0   # Nominal recommended
        preferred_wall = 4.0 # Preferred for robust parts
        min_draft = 1.5      # degrees
        min_corner_rad = 0.5 # mm
        min_cast_hole_dia = 5.0  # Holes below this should be CNC'd
        machine_stock = 1.0  # mm over-cast material for machining
        min_feature_gap = 3.0  # Minimum mold steel thickness
        tool_cost_range = "$15K-$300K+"
        cycle_time = "60-100 seconds"
        profile_tol = 0.5    # mm typical as-cast profile
    elif process_type == 'lpdc':
        process_name = 'Low Pressure Die Casting (LPDC)'
        min_wall = 3.0
        nominal_wall = 4.0
        preferred_wall = 5.0
        min_draft = 3.0      # Higher draft for LPDC
        min_corner_rad = 0.5
        min_cast_hole_dia = 5.0
        machine_stock = 1.5
        min_feature_gap = 6.0  # Larger gaps for LPDC
        tool_cost_range = "$10K-$60K+"
        cycle_time = "240-280 seconds"
        profile_tol = 1.0
    else:  # gravity / permanent mold
        process_name = 'Gravity Cast / Permanent Mold'
        min_wall = 3.5
        nominal_wall = 5.0   # Thicker nominal for perm mold
        preferred_wall = 6.0
        min_draft = 3.0
        min_corner_rad = 0.5
        min_cast_hole_dia = 5.0
        machine_stock = 3.0  # More stock needed for perm mold
        min_feature_gap = 6.0
        tool_cost_range = "$10K-$60K+"
        cycle_time = "240-280 seconds"
        profile_tol = 2.6
    
    # Material-specific parameters
    material_lower = material.lower()
    if 'a380' in material_lower or 'aluminum' in material_lower:
        material_name = 'A380 Aluminum' if 'a380' in material_lower else 'Aluminum'
        material_note = 'Primary alloy: A380 (8% Si, 4% Cu). Improves flow and machining.'
    elif 'alsi12' in material_lower or 'alsi' in material_lower:
        material_name = 'AlSi12(Fe)'
        material_note = 'Improved thermal conductivity (~30% better than A380) with minor strength trade-off.'
    elif '319' in material_lower:
        material_name = '319.0 Aluminum'
        material_note = 'Primary alloy for permanent mold casting.'
    elif 'zinc' in material_lower:
        material_name = 'Zinc'
        material_note = 'Requires separate investigation per 930-00166.'
    elif 'magnesium' in material_lower:
        material_name = 'Magnesium'
        material_note = 'Requires separate investigation per 930-00166.'
    else:
        material_name = material
        material_note = 'Verify alloy suitability for selected process.'
    
    # RULE 1: Wall Thickness
    rule_name = "Wall Thickness"
    rule_standard = f"{process_name}: Min feature = {min_wall}mm, Nominal = {nominal_wall}mm, Preferred = {preferred_wall}mm per 930-00166"
    
    if min_thickness > 0:
        if min_thickness < min_wall:
            issues.append({
                'category': 'Wall Thickness',
                'message': f'Critical: Wall thickness {min_thickness:.2f}mm below minimum {min_wall}mm',
                'recommendation': f'Increase to nominal {nominal_wall}mm, preferred {preferred_wall}mm',
                'rationale': f'Walls below {min_wall}mm cannot reliably fill in {process_name} — molten aluminum freezes before complete fill, causing cold shuts and misruns.'
            })
            rationale.append(f"❌ Wall thickness {min_thickness:.2f}mm below minimum {min_wall}mm.")
            all_rules.append({
                'name': rule_name, 'standard': rule_standard, 'status': 'FAIL',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall thickness {min_thickness:.2f}mm is below minimum feature size {min_wall}mm for {process_name}',
                'recommendation': f'Increase to minimum {min_wall}mm (absolute), {nominal_wall}mm nominal, {preferred_wall}mm preferred',
                'rationale': f'Walls <{min_wall}mm in {process_name} cause: (1) Cold shuts — molten metal freezes before complete fill, (2) Misruns — incomplete part fill, (3) Porosity from trapped gas in thin sections, (4) Dimensional instability. {material_note}',
                'cost_impact': 'Thin-wall casts: 40-60% scrap rate from fill defects, requires high-pressure cycles + 15-25% cost premium'
            })
        elif min_thickness < nominal_wall:
            warnings.append({
                'category': 'Wall Thickness',
                'message': f'Wall thickness {min_thickness:.2f}mm is marginal for {process_name}',
                'recommendation': f'Increase to nominal {nominal_wall}mm for robust fill',
                'rationale': f'Walls between {min_wall}mm and {nominal_wall}mm are manufacturable but may require premium tooling strategies.'
            })
            rationale.append(f"⚠️ Wall thickness {min_thickness:.2f}mm marginal - nominal is {nominal_wall}mm.")
            all_rules.append({
                'name': rule_name, 'standard': rule_standard, 'status': 'WARNING',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall thickness between minimum ({min_wall}mm) and nominal ({nominal_wall}mm) - manufacturable but marginal',
                'recommendation': f'Increase to nominal {nominal_wall}mm for optimal fill and cost',
                'rationale': f'Marginal walls require premium gating strategies, additional vents, and higher-pressure cycles. {material_note}',
                'cost_impact': '10-20% cost premium for marginal walls. Higher inspection/scrap rate.'
            })
        elif min_thickness > 10 and process_type == 'hpdc':
            warnings.append({
                'category': 'Wall Thickness',
                'message': f'Wall thickness {min_thickness:.2f}mm is thick for HPDC - porosity risk',
                'recommendation': f'Reduce to <10mm or switch to Permanent Mold for thick sections',
                'rationale': 'Thick sections in HPDC trap gas bubbles during rapid cooling, causing shrink porosity.'
            })
            all_rules.append({
                'name': rule_name, 'standard': rule_standard, 'status': 'WARNING',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall {min_thickness:.2f}mm is too thick for HPDC — shrink porosity risk',
                'recommendation': 'Reduce wall thickness <10mm, add coring, or switch to Permanent Mold',
                'rationale': 'HPDC fast cooling causes shrink porosity in thick sections. Permanent Mold with slower cooling handles thick sections better.',
                'cost_impact': 'HPDC thick sections: 30-50% scrap rate from porosity. Consider Perm Mold at 1000+ EAU.'
            })
        else:
            passed.append({'check': 'Wall Thickness', 'status': f'{min_thickness:.2f}mm - Good'})
            rationale.append(f"✓ Wall thickness {min_thickness:.2f}mm meets requirements.")
            all_rules.append({
                'name': rule_name, 'standard': rule_standard, 'status': 'PASS',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Wall thickness {min_thickness:.2f}mm is within optimal range',
                'recommendation': 'No changes needed',
                'rationale': f'Wall thickness meets nominal for {process_name}.',
                'cost_impact': 'Standard casting cost'
            })
    
    # RULE 2: Corner Radii & Fillets
    rule_name = "Corner Radii & Fillets"
    rule_standard = f"Min inside radius: {min_corner_rad}mm. External radius = inside + wall thickness per 930-00166"
    
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Corner radii cannot be fully measured from geometry - manual check required',
        'recommendation': f'All internal corners: minimum {min_corner_rad}mm radius. External = inside + {min_thickness:.2f}mm (wall thickness)',
        'rationale': f'Sharp corners in casts: (1) Impossible to maintain in mold over tool life, (2) Stress concentrators causing part failure, (3) Porosity formation at sharp junctions. Exception: Parting line edges should NOT have radii unless functionally required.',
        'cost_impact': 'Sharp corners: tool failure at 50-75% of expected life (+$5K-$30K tool refurb). Stress cracking in service.'
    })
    suggestions.append({
        'opportunity': f'Add {min_corner_rad}mm minimum fillets to all internal corners',
        'savings': 'Extends tool life 2-3x, reduces stress concentrations',
        'difficulty': 'Easy'
    })
    
    # RULE 3: Draft Angles
    rule_name = "Draft Angles"
    rule_standard = f"{process_name}: Minimum {min_draft}° draft on all vertical walls per 930-00166"
    
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Draft angles cannot be automatically measured - verify in CAD',
        'recommendation': f'Add {min_draft}° minimum draft to ALL walls parallel to mold opening direction. LPDC may require up to 7° depending on draw depth.',
        'rationale': f'Molten aluminum shrinks ~0.5% on cooling and grips the core. Without {min_draft}°+ draft: part sticks on ejection, warps, or breaks. Draft cannot be added easily after mold is cut — critical to address at design time.',
        'cost_impact': 'No-draft walls require side-action slides (+10% tool cost each) or post-CNC (+$5-$15 per feature). 15-25% scrap rate from ejection damage.'
    })
    
    # RULE 4: Cast Hole Diameter
    rule_name = "Cast Hole Diameter"
    rule_standard = f"Minimum as-cast hole diameter: {min_cast_hole_dia}mm. Smaller holes must be CNC'd per 930-00166"
    
    if holes:
        small_cast_holes = [h for h in holes if h.get('diameter', 0) > 0 and h.get('diameter', 0) < min_cast_hole_dia]
        
        if small_cast_holes:
            warnings.append({
                'category': 'Cast Holes',
                'message': f'{len(small_cast_holes)} holes below {min_cast_hole_dia}mm must be post-cast CNC\'d',
                'recommendation': f'For holes <{min_cast_hole_dia}mm: design as CNC features, not as-cast',
                'rationale': f'Holes <{min_cast_hole_dia}mm cannot be cast reliably — mold pins are fragile and break. Post-cast CNC drilling is required.'
            })
            rationale.append(f"⚠️ {len(small_cast_holes)} holes <{min_cast_hole_dia}mm require post-cast CNC.")
            all_rules.append({
                'name': rule_name, 'standard': rule_standard, 'status': 'WARNING',
                'measured_value': f'{len(small_cast_holes)} holes <{min_cast_hole_dia}mm',
                'evaluation': f'''Detected {len(small_cast_holes)} holes below minimum as-cast diameter. Examples: {", ".join(f"Ø{h.get('diameter', 0):.1f}mm" for h in small_cast_holes[:3])}''',
                'recommendation': f'Route these holes through post-cast CNC machining operation',
                'rationale': f'Cast hole pins <{min_cast_hole_dia}mm diameter break under molten metal pressure. Cost to repair broken pins: $500-$2000 per incident. Reliability: 20-30% pin failure rate on small holes.',
                'cost_impact': f'Post-CNC drilling: +$0.50-$2.00 per hole. Broken pins: $500-$2000 per event + 1-2 week delay.'
            })
        else:
            passed.append({'check': 'Cast Hole Diameter', 'status': f'All holes ≥{min_cast_hole_dia}mm'})
            all_rules.append({
                'name': rule_name, 'standard': rule_standard, 'status': 'PASS',
                'measured_value': f'{len(holes)} holes, all ≥{min_cast_hole_dia}mm',
                'evaluation': f'All detected holes meet minimum as-cast diameter {min_cast_hole_dia}mm',
                'recommendation': 'Holes can be cast directly',
                'rationale': 'Hole sizes compatible with standard casting pins.',
                'cost_impact': 'Standard cast cost, no post-CNC required'
            })
    
    # RULE 5: Feature-to-Feature Gap (Mold Steel Thickness)
    rule_name = "Feature-to-Feature Gap"
    rule_standard = f"Minimum {min_feature_gap}mm gap between features for {process_name} tooling per 930-00166"
    
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': 'Cannot auto-detect',
        'evaluation': f'Feature spacing affects mold steel thickness between cavities',
        'recommendation': f'Maintain minimum {min_feature_gap}mm between adjacent cast features (ribs, bosses, pockets)',
        'rationale': f'Thin mold steel between features (<{min_feature_gap}mm) overheats and cracks under thermal cycling. Heat checking appears at 50-75% of tool life as positive "cracks" on cast part.',
        'cost_impact': f'Feature gaps <{min_feature_gap}mm: Tool life reduced 30-50%. Heat check refurbish: ~60% of original tool cost.'
    })
    
    # RULE 6: Machining Stock Allowance
    rule_name = "Machining Stock"
    rule_standard = f"Add {machine_stock}mm over-cast material on surfaces to be CNC'd per 930-00166"
    
    suggestions.append({
        'opportunity': f'Add {machine_stock}mm machine stock on all post-CNC surfaces',
        'savings': 'Prevents dimensional failures from tool wear and shrinkage',
        'difficulty': 'Easy'
    })
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Machine stock cannot be measured from finished geometry',
        'recommendation': f'For surfaces requiring post-CNC: add {machine_stock}mm over-cast material. Do NOT exceed — deeper cuts increase porosity exposure risk.',
        'rationale': f'HPDC: 1mm stock. LPDC/Perm Mold: 3mm. Excess stock exposes internal porosity at depth. Air-cuts can mitigate tolerance issues at max material condition.',
        'cost_impact': 'Insufficient stock: parts fail dimensional inspection (+$50-$200 scrap). Excess stock: +20-40% CNC time.'
    })
    
    # RULE 7: Slides and Undercuts
    rule_name = "Slides and Undercuts"
    rule_standard = "Each slide adds ~10% to tool cost. Avoid undercuts if possible per 930-00166"
    
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Undercuts cannot be auto-detected reliably',
        'recommendation': 'Review part for features parallel to mold opening. Consider post-CNC for undercut features if tool cost savings justify it.',
        'rationale': 'Slides/side-action: adds +10% tool cost each, +maintenance burden. Post-CNC alternative: cost analysis on per-part basis. Simple parts without slides: lower tool cost, higher reliability.',
        'cost_impact': 'Each slide: +10% tool cost, +$2K-$10K. Slide maintenance: +15% over tool life.'
    })
    
    # RULE 8: Parting Line
    rule_name = "Parting Line Complexity"
    rule_standard = "Keep parting line as simple as possible per 930-00166"
    
    suggestions.append({
        'opportunity': 'Design for simple planar parting line',
        'savings': '$5K-$30K tool cost savings, improved tool life',
        'difficulty': 'Medium'
    })
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Parting line defined at mold design phase',
        'recommendation': 'Work with casting supplier DFM to simplify parting line. Avoid complex 3D parting paths.',
        'rationale': 'Complex parting lines: harder to maintain tool life, more expensive trim dies, +0.25mm additional profile tolerance. Planar parting lines: easier fit and finish, longer tool life.',
        'cost_impact': 'Complex parting: +$5K-$30K tool cost, +leadtime, tighter fit tolerances required.'
    })
    
    # RULE 9: Part Size vs Machine Capacity
    rule_name = "Part Size vs Machine Capacity"
    rule_standard = "Max HPDC projected area: 5500 cm² (4400-ton press). Larger parts require Perm Mold per 930-00166"
    
    if dims:
        projected_area_est = dims.get('x', 0) * dims.get('y', 0) / 100  # Rough estimate in cm²
        if process_type == 'hpdc' and projected_area_est > 5500:
            issues.append({
                'category': 'Part Size',
                'message': f'Part projected area {projected_area_est:.0f}cm² exceeds HPDC max (5500cm²)',
                'recommendation': 'Split part into assembly or use Permanent Mold / Gravity casting',
                'rationale': 'Largest HPDC machines (4400-ton) limited to ~5500cm² projected area.'
            })
            all_rules.append({
                'name': rule_name, 'standard': rule_standard, 'status': 'FAIL',
                'measured_value': f'{projected_area_est:.0f}cm² projected',
                'evaluation': f'Part exceeds maximum HPDC size. 4400-ton presses are the largest available.',
                'recommendation': 'Switch to Permanent Mold (no machine tonnage limit) or split into smaller assembly',
                'rationale': 'HPDC requires clamping force = 4 tons per in² of projected area. Max press = 4400 tons.',
                'cost_impact': 'Perm Mold for large parts: similar piece-part cost, 2-3x cycle time.'
            })
        else:
            passed.append({'check': 'Part Size', 'status': f'~{projected_area_est:.0f}cm² projected'})
            all_rules.append({
                'name': rule_name, 'standard': rule_standard, 'status': 'PASS',
                'measured_value': f'{projected_area_est:.0f}cm² projected',
                'evaluation': f'Part size compatible with {process_name}',
                'recommendation': 'No changes needed',
                'rationale': f'Part fits standard {process_name} machine capacity.',
                'cost_impact': 'Standard tooling cost'
            })
    
    # RULE 10: Porosity Risk Assessment
    rule_name = "Porosity Risk"
    rule_standard = "Avoid thick sections >8mm, abrupt thickness transitions, and isolated features per 930-00166"
    
    all_rules.append({
        'name': rule_name, 'standard': rule_standard, 'status': 'INFO',
        'measured_value': 'Design review required',
        'evaluation': 'Porosity risk requires mold flow analysis at DFM phase',
        'recommendation': 'Maintain uniform wall thickness. Bridge isolated features. Avoid sections >8mm. Review mold flow analysis with supplier.',
        'rationale': f'Porosity causes: (1) Hydrogen gas dissolved in aluminum, (2) Air trapped during injection, (3) Shrink as metal cools. Prevention: degassing (supplier), uniform walls, good venting. X-ray inspection catches large pores but misses small ones.',
        'cost_impact': 'Porosity: 5-10% scrap rate typical. X-ray inspection: +$5-$15/part for critical features.'
    })
    
    # Calculate score
    total_checks = len(issues) + len(warnings) + len(passed)
    if total_checks > 0:
        score = (len(passed) * 100 + len(warnings) * 50) / total_checks
    else:
        score = 75.0  # Default for design-consideration rules
    
    score_explanation = f"Score from {len(passed)} passed, {len(warnings)} warnings, {len(issues)} critical"
    
    # Assessment
    if score >= 90:
        assessment = "EXCELLENT - Well-designed for casting"
    elif score >= 75:
        assessment = "GOOD - Minor improvements recommended"
    elif score >= 60:
        assessment = "ACCEPTABLE - Review warnings"
    else:
        assessment = "NEEDS REVISION - Address critical issues"
    
    summary = f"""**Process:** {process_name}
**Material:** {material_name} — {material_note}
**Overall Assessment:** {assessment}
**Manufacturability Score:** {score:.1f}/100

**Analysis Results:** {len(passed)} passed, {len(warnings)} warnings, {len(issues)} critical issues

**Process Capabilities:**
• Profile tolerance: ±{profile_tol}mm typical (across parting line: +0.25-1.0mm additional)
• Cycle time: {cycle_time}
• Tool cost: {tool_cost_range}
• Minimum wall: {min_wall}mm (nominal {nominal_wall}mm, preferred {preferred_wall}mm)
• Minimum draft: {min_draft}°
• Tool life: 100K shots (HPDC) / 60K shots (Perm Mold)

**Key Design Points per 930-00166:**
1. Uniform wall thickness (avoid abrupt changes)
2. All internal corners ≥{min_corner_rad}mm fillet
3. All vertical walls ≥{min_draft}° draft
4. Holes <{min_cast_hole_dia}mm → post-CNC machining
5. Add {machine_stock}mm stock on CNC surfaces
6. Minimize slides (each adds 10% tool cost)

**Standards Compliance:** NADCA 11th Edition, 930-00166_R01
"""
    
    return {
        'success': True,
        'process': process_name,
        'material': material,
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
