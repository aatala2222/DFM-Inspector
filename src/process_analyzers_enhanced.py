"""
Enhanced Manufacturing Process Analyzers - Part 2
Injection Molding, Die Casting, and other processes with comprehensive DFM rules
"""
from typing import Dict


def analyze_injection_molding(parser, material, geometry) -> Dict:
    """Analyze for injection molding with comprehensive DFM rules"""
    issues = []
    warnings = []
    suggestions = []
    passed = []
    rationale = []
    
    dims = geometry.get('dimensions', {})
    volume = geometry.get('volume', 0)
    min_thickness = geometry.get('estimated_min_thickness', 0)
    
    # RULE 1: Wall Thickness (SPI Standards)
    if min_thickness > 0:
        if min_thickness < 0.5:
            issues.append({
                'category': 'Wall Thickness',
                'message': f'Critical: Wall thickness {min_thickness:.2f}mm too thin',
                'recommendation': 'Increase to 0.75-3.0mm range for injection molding',
                'rationale': f'Walls thinner than 0.5mm are difficult to fill completely, causing short shots and incomplete parts. Plastic flow resistance increases exponentially below 0.5mm. Minimum practical thickness: 0.5mm for small parts, 0.75mm for larger parts.'
            })
            rationale.append(f"❌ Wall thickness {min_thickness:.2f}mm below minimum for injection molding (0.5mm).")
        elif min_thickness > 6.0:
            warnings.append({
                'category': 'Wall Thickness',
                'message': f'Thick walls {min_thickness:.2f}mm will cause sink marks and warpage',
                'recommendation': 'Reduce to 3-4mm maximum or core out thick sections',
                'rationale': f'Thick walls ({min_thickness:.2f}mm) cool unevenly, causing visible sink marks on surface, internal voids, and warpage. Cycle time increases proportionally to wall thickness squared. Thick sections should be cored out with ribs for support. Maximum recommended: 4mm for most plastics.'
            })
            rationale.append(f"⚠️ Wall thickness {min_thickness:.2f}mm will cause sink marks, voids, and long cycle times.")
        else:
            passed.append({'check': 'Wall Thickness', 'status': f'{min_thickness:.2f}mm - Optimal range'})
            rationale.append(f"✓ Wall thickness {min_thickness:.2f}mm is within optimal range (0.75-4mm) for injection molding.")
    
    # RULE 2: Wall Thickness Uniformity
    # Standard: Variation should be <25% of nominal thickness
    if min_thickness > 0:
        warnings.append({
            'category': 'Wall Uniformity',
            'message': 'Verify wall thickness variation is <25% of nominal',
            'recommendation': f'Maintain uniform {min_thickness:.2f}mm ±{min_thickness*0.25:.2f}mm throughout part',
            'rationale': f'Non-uniform walls cause differential cooling rates, leading to warpage, sink marks, and internal stresses. Thick-to-thin transitions should be gradual (3:1 taper ratio). Uniform walls ensure even cooling, minimal warpage, and consistent part quality. Target variation: <25% of nominal thickness.'
        })
        rationale.append(f"⚠️ Maintain uniform wall thickness within ±25% ({min_thickness*0.25:.2f}mm) to prevent warpage.")
    
    # RULE 3: Draft Angles
    # Standard: 1° minimum, 2-3° recommended per side
    warnings.append({
        'category': 'Draft Angles',
        'message': 'Verify draft angles on all vertical walls',
        'recommendation': 'Add 1-3° draft per side on all walls parallel to mold opening direction',
        'rationale': 'Draft angles allow easy part ejection from mold without damage. Minimum: 0.5° for shallow features, 1° standard, 2-3° recommended for textured surfaces. Without draft, parts stick in mold, requiring excessive ejection force that damages part or mold. Each additional degree of draft reduces ejection force by 5-10%.'
    })
    rationale.append("⚠️ Add 1-3° draft angles to all vertical walls for easy part ejection.")
    
    # RULE 4: Rib Design
    # Standard: Rib thickness = 50-60% of nominal wall, height ≤3× wall thickness
    if min_thickness > 0:
        rib_thickness = min_thickness * 0.6
        max_rib_height = min_thickness * 3
        
        suggestions.append({
            'opportunity': f'Design ribs at {rib_thickness:.2f}mm thickness (60% of wall)',
            'savings': 'Prevents sink marks while maintaining strength',
            'difficulty': 'Easy',
            'rationale': f'Ribs should be 50-60% of nominal wall thickness to avoid sink marks on opposite surface. For {min_thickness:.2f}mm walls: rib thickness = {rib_thickness:.2f}mm, maximum height = {max_rib_height:.1f}mm (3× wall). Thicker ribs cause visible sink marks. Add draft to ribs: 0.5-1° per side.'
        })
        rationale.append(f"Design ribs at {rib_thickness:.2f}mm thick (60% of wall) to prevent sink marks.")
    
    # RULE 5: Corner Radii
    # Standard: Inside radius = 0.5× wall thickness minimum, outside radius = inside + wall thickness
    if min_thickness > 0:
        min_inside_radius = min_thickness * 0.5
        outside_radius = min_inside_radius + min_thickness
        
        warnings.append({
            'category': 'Corner Radii',
            'message': f'Add radii to all corners: inside ≥{min_inside_radius:.2f}mm',
            'recommendation': f'Use {min_inside_radius:.2f}mm inside radius, {outside_radius:.2f}mm outside radius',
            'rationale': f'Sharp corners create stress concentrations, causing part failure and mold wear. Minimum inside radius = 0.5× wall thickness ({min_inside_radius:.2f}mm for {min_thickness:.2f}mm walls). Outside radius = inside radius + wall thickness = {outside_radius:.2f}mm. Generous radii improve plastic flow and part strength.'
        })
        rationale.append(f"⚠️ Add {min_inside_radius:.2f}mm minimum inside radius to all corners.")
    
    # RULE 6: Boss Design
    # Standard: Boss wall = 60% of nominal wall, height ≤2.5× outer diameter
    if min_thickness > 0:
        boss_wall = min_thickness * 0.6
        
        suggestions.append({
            'opportunity': f'Design bosses with {boss_wall:.2f}mm wall thickness',
            'savings': 'Prevents sink marks and ensures proper screw retention',
            'difficulty': 'Medium',
            'rationale': f'Boss wall thickness should be 60% of nominal wall ({boss_wall:.2f}mm for {min_thickness:.2f}mm walls) to prevent sink marks. Boss height ≤2.5× outer diameter. Add gussets or ribs to support tall bosses. Use through-holes for self-tapping screws, blind holes for heat-set inserts. Minimum boss OD = 2× screw diameter.'
        })
    
    # RULE 7: Undercuts and Side Actions
    suggestions.append({
        'opportunity': 'Eliminate undercuts to avoid side actions',
        'savings': '$5,000-$15,000 per side action eliminated from mold cost',
        'difficulty': 'Medium',
        'rationale': 'Undercuts require side actions (slides/lifters) in mold, adding $5,000-15,000 per action to mold cost and 2-5 seconds to cycle time. Alternatives: (1) Split part into assembly, (2) Redesign feature to allow straight pull, (3) Use bumpoffs for small undercuts (<0.5mm), (4) Hand-load inserts. Each side action increases mold complexity and maintenance.'
    })
    
    # RULE 8: Gate Location and Size
    # Standard: Gate thickness = 50-70% of wall thickness
    if min_thickness > 0:
        gate_thickness = min_thickness * 0.6
        
        warnings.append({
            'category': 'Gate Design',
            'message': f'Gate thickness should be {gate_thickness:.2f}mm (60% of wall)',
            'recommendation': 'Position gate at thickest section, away from cosmetic surfaces',
            'rationale': f'Gate is the injection point where plastic enters mold. Gate thickness = 50-70% of wall thickness ({gate_thickness:.2f}mm for {min_thickness:.2f}mm walls). Position at thickest section for best flow. Gate leaves visible mark - locate on non-cosmetic surface. Undersized gates cause high injection pressure and long fill times.'
        })
        rationale.append(f"⚠️ Position gate at thickest section, size at {gate_thickness:.2f}mm (60% of wall).")
    
    # RULE 9: Part Size and Tonnage
    if dims and volume > 0:
        max_dim = max(dims.values())
        # Estimate projected area (simplified)
        projected_area_cm2 = (dims.get('x', 0) * dims.get('y', 0)) / 100  # Convert mm² to cm²
        required_tonnage = projected_area_cm2 * 5  # Rule of thumb: 5 tons per cm² projected area
        
        if required_tonnage > 500:
            warnings.append({
                'category': 'Part Size',
                'message': f'Large part requires ~{required_tonnage:.0f} ton press',
                'recommendation': 'Consider splitting into smaller parts or verify press availability',
                'rationale': f'Part requires approximately {required_tonnage:.0f} tons clamping force (5 tons/cm² × {projected_area_cm2:.1f}cm² projected area). Presses over 500 tons are less common and more expensive ($150-300/hr vs $50-100/hr for smaller presses). Consider splitting into assembly of smaller parts.'
            })
            rationale.append(f"⚠️ Part requires ~{required_tonnage:.0f} ton press - limited availability, higher cost.")
        else:
            passed.append({'check': 'Part Size', 'status': f'Fits standard presses (~{required_tonnage:.0f} tons)'})
            rationale.append(f"✓ Part fits standard injection molding presses (~{required_tonnage:.0f} tons required).")
    
    # RULE 10: Material-Specific Considerations
    if 'abs' in material.lower():
        passed.append({'check': 'Material Selection', 'status': 'ABS - Excellent for injection molding'})
        rationale.append("✓ ABS offers excellent flow, impact strength, and surface finish. Mold temp: 50-80°C, melt temp: 220-250°C.")
        suggestions.append({
            'opportunity': 'Material Selection - ABS',
            'savings': 'Good balance of cost ($2-3/lb), strength, and processability',
            'difficulty': 'N/A',
            'rationale': 'ABS is ideal for injection molding: excellent flow, good impact strength, easy to process, and accepts paint/plating well. Shrinkage: 0.5-0.7%. Best for housings, enclosures, and structural parts. Consider ABS+PC blend for higher heat resistance.'
        })
    elif 'polycarbonate' in material.lower() or 'pc' in material.lower():
        warnings.append({
            'category': 'Material Processing',
            'message': 'Polycarbonate requires high mold temperatures and drying',
            'recommendation': 'Ensure mold can handle 80-100°C, dry resin 4hrs at 120°C',
            'rationale': 'PC requires high mold temps (80-100°C) vs 50-80°C for ABS, increasing cycle time 20-30%. Must be dried before molding (4hrs at 120°C) or will have bubbles/weak spots. Melt temp: 280-320°C. Benefits: excellent impact strength and clarity. Use for applications requiring toughness.'
        })
        rationale.append("⚠️ Polycarbonate requires high mold temps (80-100°C) and pre-drying - 20-30% longer cycles.")
    elif 'polypropylene' in material.lower() or 'pp' in material.lower():
        passed.append({'check': 'Material Selection', 'status': 'PP - Excellent flow and low cost'})
        rationale.append("✓ Polypropylene offers excellent flow, chemical resistance, and low cost ($1-2/lb). Shrinkage: 1.5-2.5% (higher than ABS).")
        warnings.append({
            'category': 'Material Shrinkage',
            'message': 'PP has high shrinkage (1.5-2.5%)',
            'recommendation': 'Account for shrinkage in mold design, use glass-filled PP for tighter tolerances',
            'rationale': 'PP shrinks 1.5-2.5% during cooling (vs 0.5-0.7% for ABS), making tight tolerances difficult. Use glass-filled PP (20-30% glass) to reduce shrinkage to 0.5-1.0%. PP is semi-crystalline, causing higher shrinkage than amorphous plastics (ABS, PC).'
        })
    elif 'nylon' in material.lower() or 'pa' in material.lower():
        warnings.append({
            'category': 'Material Processing',
            'message': 'Nylon is hygroscopic and requires drying',
            'recommendation': 'Dry resin 4-6hrs at 80°C, use glass-filled for dimensional stability',
            'rationale': 'Nylon absorbs moisture from air, causing bubbles and weak parts if not dried (4-6hrs at 80°C). Hygroscopic nature also causes dimensional changes in humid environments. Use glass-filled nylon (30-33% glass) for better dimensional stability and reduced moisture absorption.'
        })
        rationale.append("⚠️ Nylon requires pre-drying and absorbs moisture - dimensional changes in humid environments.")
    
    # RULE 11: Tolerances
    suggestions.append({
        'opportunity': 'Apply commercial tolerances (±0.13mm / ±0.005")',
        'savings': '15-25% cost reduction vs tight tolerances',
        'difficulty': 'Easy',
        'rationale': 'Commercial injection molding tolerances: ±0.13mm (±0.005") for dimensions up to 25mm, ±0.25mm up to 100mm. Tighter tolerances require mold modifications, secondary operations, or engineering-grade resins. Only specify tight tolerances where functionally required. Each tight tolerance dimension adds 10-20% to part cost.'
    })
    
    # RULE 12: Cycle Time Optimization
    if min_thickness > 0:
        estimated_cycle_time = (min_thickness ** 2) * 2  # Simplified: cycle time ≈ 2× (wall thickness)²
        
        suggestions.append({
            'opportunity': 'Optimize wall thickness for cycle time',
            'savings': f'Current wall ({min_thickness:.2f}mm) = ~{estimated_cycle_time:.0f}s cycle time',
            'difficulty': 'Medium',
            'rationale': f'Cycle time is proportional to wall thickness squared. Reducing wall from {min_thickness:.2f}mm to {min_thickness*0.8:.2f}mm (-20%) reduces cycle time by 36%. Cycle time = cooling time + fill time + ejection time. Cooling dominates (70-80% of cycle). Thinner walls = faster cooling = lower part cost. Balance with strength requirements.'
        })
    
    # Calculate score
    total_checks = len(issues) + len(warnings) + len(passed)
    score = (len(passed) * 100 + len(warnings) * 50) / total_checks if total_checks > 0 else 85.0
    score_explanation = f"Based on {len(passed)} passed checks, {len(warnings)} warnings, {len(issues)} critical issues"
    
    # Generate summary
    if score >= 90:
        assessment = "EXCELLENT - Well-suited for injection molding"
    elif score >= 75:
        assessment = "GOOD - Minor optimization recommended"
    elif score >= 60:
        assessment = "ACCEPTABLE - Review warnings carefully"
    else:
        assessment = "NEEDS REVISION - Address critical issues"
    
    summary = f"""**Overall Assessment:** {assessment}
**Manufacturability Score:** {score:.1f}/100

**Analysis Results:** {len(passed)} checks passed, {len(warnings)} warnings, {len(issues)} critical issues

**Key Findings:**
• Wall thickness: {min_thickness:.2f}mm - {"Optimal (0.75-4mm)" if 0.75 <= min_thickness <= 4.0 else "Review required"}
• Add 1-3° draft angles to all vertical walls
• Maintain uniform wall thickness (±25%)
• Design ribs at 60% of wall thickness

**Recommendation:** {"Design is manufacturable. Address warnings to optimize quality and cost." if len(issues) == 0 else "Address critical wall thickness issues before tooling."}"""
    
    return {
        'success': True,
        'process': 'Injection Molding',
        'material': material,
        'score': round(score, 1),
        'score_explanation': score_explanation,
        'issues': len(issues),
        'warnings': len(warnings),
        'suggestions': len(suggestions),
        'passed': len(passed),
        'geometry_info': {
            'dimensions': f"{dims.get('x', 0):.1f} x {dims.get('y', 0):.1f} x {dims.get('z', 0):.1f} mm",
            'volume': f"{volume:.2f} mm³",
            'min_thickness': f"{min_thickness:.2f} mm" if min_thickness > 0 else 'N/A'
        },
        'rationale': rationale,
        'summary': summary,
        'details': {
            'critical_issues': issues[:5],
            'warnings': warnings[:5],
            'cost_savings': suggestions[:4]
        }
    }
