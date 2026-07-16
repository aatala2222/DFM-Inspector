"""
Enhanced Die Casting Analyzer
Based on 930-00166_R01 - High Pressure Die Cast and Gravity Cast Permanent Mold Design Guidelines
"""
from typing import Dict


def analyze_die_casting_enhanced(parser, material, geometry, process_type='hpdc') -> Dict:
    """
    Comprehensive die casting DFM analysis
    Based on industry standards from 930-00166_R01
    
    Args:
        parser: CAD parser object
        material: Material specification
        geometry: Geometry analysis dictionary
        process_type: 'hpdc' (High Pressure Die Casting) or 'perm_mold' (Permanent Mold)
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
    
    # Determine process-specific parameters
    if 'perm' in process_type.lower() or 'gravity' in process_type.lower():
        process_name = "Permanent Mold (Gravity Cast)"
        min_wall = 3.0
        nominal_wall = 4.0
        min_draft = 3.0
        min_mold_steel = 6.0
        machining_stock = 1.75  # 1.5-2mm
        min_hole_dia = 6.0  # Variable, but conservative estimate
        surface_finish = "250-420 RMS"
        linear_tol = "±0.38mm/25mm"
    else:
        process_name = "High Pressure Die Casting (HPDC)"
        min_wall = 2.0
        nominal_wall = 3.0
        min_draft = 1.5
        min_mold_steel = 3.0
        machining_stock = 1.0
        min_hole_dia = 5.0
        surface_finish = "60-120 RMS"
        linear_tol = "±0.25mm/25mm"
    
    # RULE 1: Wall Thickness (Critical)
    rule_name = "Wall Thickness"
    rule_standard = f"Nominal: {nominal_wall}mm (preferred). Minimum: {min_wall}mm per 930-00166"
    
    if min_thickness > 0:
        if min_thickness < min_wall:
            issues.append({
                'category': 'Wall Thickness',
                'message': f'Critical: Wall thickness {min_thickness:.2f}mm below minimum',
                'recommendation': f'Increase to minimum {min_wall}mm for {process_name}',
                'rationale': f'Walls <{min_wall}mm risk incomplete fill, porosity, and weak sections. Molten aluminum cannot flow reliably through thin sections.'
            })
            rationale.append(f"❌ Wall thickness {min_thickness:.2f}mm below minimum {min_wall}mm.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'FAIL',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Checking criteria: Wall thickness must be ≥{min_wall}mm minimum for {process_name}. Analysis: Measured minimum wall thickness = {min_thickness:.2f}mm from geometry analysis. Result: FAIL - thickness below minimum causes incomplete fill and porosity.',
                'recommendation': f'Increase to {min_wall}mm minimum, {nominal_wall}mm nominal for reliable {process_name}',
                'rationale': f'Walls <{min_wall}mm cause critical failures in {process_name}: (1) Incomplete fill (short shots) - molten aluminum (660°C) freezes rapidly in thin sections before reaching all areas, leaving incomplete parts (40-60% scrap rate). (2) Porosity - rapid cooling traps gas bubbles and shrinkage voids in thin walls, creating weak porous structure. (3) Cold shuts - two flow fronts meet but don\'t fuse properly in thin sections, creating weak seam. (4) Weak sections - insufficient material for structural loads, parts break easily. {"HPDC: High injection velocity (40-60 m/s) helps but cannot overcome physics of thin walls. Minimum 2mm required." if process_type == "hpdc" else "Permanent Mold: Gravity feed (no pressure) makes thin walls even more difficult. Minimum 3mm required for reliable fill."} Nominal {nominal_wall}mm provides safety margin and better flow. Your {min_thickness:.2f}mm is below minimum.',
                'cost_impact': f'Walls <{min_wall}mm: 40-60% scrap rate from incomplete fill, 30-40% scrap from porosity, requires thicker walls (+material cost), potential need for squeeze casting (+150-200% cost)'
            })
        elif min_thickness > 10.0:
            warnings.append({
                'category': 'Wall Thickness',
                'message': f'Thick walls {min_thickness:.2f}mm may cause shrink porosity',
                'recommendation': 'Consider coring out thick sections or adding ribs',
                'rationale': 'Thick sections (>10mm) in die casting develop shrink porosity as interior cools slower than surface. Air bubbles form as material contracts.'
            })
            rationale.append(f"⚠️ Wall thickness {min_thickness:.2f}mm may cause shrink porosity.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Checking criteria: Wall thickness should be ≤10mm to avoid shrink porosity. Analysis: Measured thickness = {min_thickness:.2f}mm exceeds recommended maximum. Result: WARNING - high risk of internal porosity and voids.',
                'recommendation': 'Core out thick sections to 3-4mm nominal wall and add ribs (60% wall thickness) for strength. Maximum 10mm before coring required',
                'rationale': f'Thick walls (>10mm) in die casting develop shrink porosity through directional solidification: (1) Outer surface solidifies first - forms rigid shell when contacting mold (rapid cooling), (2) Interior cools slower - remains molten while surface is solid, (3) Shrinkage voids form - aluminum shrinks 6-7% during solidification, interior contracts creating air pockets (porosity), (4) No feeding path - solid shell prevents molten metal from feeding shrinkage, voids become permanent. {"HPDC especially susceptible: high injection velocity creates turbulence, trapping air bubbles that combine with shrinkage voids." if process_type == "hpdc" else "Permanent Mold less susceptible: slower fill reduces turbulence, but shrinkage porosity still occurs in thick sections."} Solution: Core out to {nominal_wall}mm nominal, add ribs at 60% wall ({nominal_wall * 0.6:.1f}mm) for strength. Ribs provide bending stiffness without thick sections. Your {min_thickness:.2f}mm will have internal voids.',
                'cost_impact': 'Thick walls >10mm: 30-40% scrap rate from porosity (X-ray inspection reveals voids), parts fail pressure testing, longer cycle time (+20-30%), higher material cost, may require vacuum die casting (+$15,000-$40,000 tooling) or HIP treatment (+$50-$200 per part)'
            })
        elif min_thickness < nominal_wall:
            warnings.append({
                'category': 'Wall Thickness',
                'message': f'Wall thickness {min_thickness:.2f}mm below nominal',
                'recommendation': f'Consider increasing to {nominal_wall}mm nominal for better flow',
                'rationale': f'Nominal {nominal_wall}mm provides better material flow, reduced porosity risk, and improved part strength.'
            })
            rationale.append(f"⚠️ Wall thickness {min_thickness:.2f}mm below nominal {nominal_wall}mm.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Checking criteria: Nominal wall thickness should be {nominal_wall}mm for optimal {process_name}. Analysis: Measured thickness = {min_thickness:.2f}mm is above minimum but below nominal. Result: WARNING - castable but not optimal.',
                'recommendation': f'Increase to {nominal_wall}mm nominal for optimal casting quality and reduced scrap rate',
                'rationale': f'Nominal {nominal_wall}mm provides safety margin over minimum {min_wall}mm: (1) Better material flow - thicker walls allow molten aluminum to flow further before freezing (flow length ≈ 150-200× thickness), (2) Reduced porosity risk - more material volume reduces gas entrapment and shrinkage effects, (3) Improved part strength - larger cross-section handles structural loads better, (4) Lower scrap rate - nominal thickness reduces risk of incomplete fill and cold shuts. {"HPDC: Nominal 3mm works well with high injection velocity (40-60 m/s). Below 3mm increases short shot risk." if process_type == "hpdc" else "Permanent Mold: Nominal 4mm compensates for slower gravity fill. Below 4mm significantly increases incomplete fill risk."} Your {min_thickness:.2f}mm is castable but requires careful process control (higher injection temperature, optimized gate location).',
                'cost_impact': '10-20% higher scrap rate below nominal thickness, requires process optimization (higher temperature, careful gating), may need thicker walls for production runs'
            })
        else:
            passed.append({'check': 'Wall Thickness', 'status': f'{min_thickness:.2f}mm - Good range'})
            rationale.append(f"✓ Wall thickness {min_thickness:.2f}mm is within optimal range.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'PASS',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': f'Checking criteria: Wall thickness should be {nominal_wall}-10mm for optimal {process_name}. Analysis: Measured minimum wall thickness = {min_thickness:.2f}mm from geometry. Result: PASS - thickness is within optimal range.',
                'recommendation': 'No changes needed - thickness is optimal for die casting',
                'rationale': f'Wall thickness {min_thickness:.2f}mm is in optimal range ({nominal_wall}-10mm), providing: (1) Complete fill - molten aluminum (660°C) flows completely through part before solidifying, (2) Minimal porosity - adequate thickness prevents gas entrapment and shrinkage voids, (3) Good strength - sufficient cross-section for structural loads, (4) Reasonable cycle time - {"HPDC: 30-90 seconds typical cycle time. Permanent Mold: 2-5 minutes typical." if process_type == "hpdc" else "Permanent Mold: 2-5 minutes typical cycle time."} (5) Standard process - no special techniques required. {"HPDC: High injection velocity (40-60 m/s) and pressure (70-140 MPa) ensure complete fill." if process_type == "hpdc" else "Permanent Mold: Gravity feed (no pressure) works well with this thickness range."} This thickness range represents industry best practice per 930-00166_R01.',
                'cost_impact': 'Standard die casting cost - no premium. Optimal cycle time and minimal scrap rate (5-10% typical for die casting)'
            })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': 'Not measured',
            'evaluation': f'Checking criteria: Wall thickness should be {min_wall}mm minimum, {nominal_wall}mm nominal for {process_name}. Analysis: Wall thickness could not be measured from geometry (requires watertight 3D model). Result: INFO - manual verification required.',
            'recommendation': f'Verify wall thickness manually: minimum {min_wall}mm, nominal {nominal_wall}mm, maximum 10mm before coring required',
            'rationale': f'Wall thickness is critical in die casting - affects fill capability, porosity, strength, and cycle time. {"HPDC: Minimum 2mm (high pressure helps), nominal 3mm (best practice). Permanent Mold: Minimum 3mm (gravity feed), nominal 4mm (reliable fill)." if process_type == "hpdc" else "Permanent Mold: Minimum 3-4mm due to gravity feed (no injection pressure). Thinner walls risk incomplete fill."} Cannot be automatically measured from this geometry. Manual verification essential before tooling ($20,000-$100,000 investment).',
            'cost_impact': 'Improper wall thickness: 40-60% scrap rate for too thin, 30-40% porosity for too thick, +20-30% cycle time for thick walls'
        })
    
    # RULE 2: Draft Angles
    rule_name = "Draft Angles"
    rule_standard = f"Minimum {min_draft}° per side for {process_name} per 930-00166"
    
    warnings.append({
        'category': 'Draft Angles',
        'message': 'Verify all vertical walls have adequate draft',
        'recommendation': f'Add minimum {min_draft}° draft to all walls perpendicular to parting line',
        'rationale': f'Draft enables part ejection from mold. Without {min_draft}° draft: parts stick in mold, require excessive ejection force (causing damage/warpage), increase cycle time 20-30%.'
    })
    rationale.append(f"⚠️ Verify draft angles on all vertical walls ({min_draft}° minimum).")
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'WARNING',
        'measured_value': 'Cannot detect from geometry',
        'evaluation': f'Checking criteria: All walls perpendicular to parting line must have draft angle ≥{min_draft}° for {process_name}. Analysis: Draft angles cannot be automatically detected from STEP geometry - requires manual verification in CAD using draft analysis tools. Result: WARNING - manual verification required.',
        'recommendation': f'Add {min_draft}° minimum draft to all walls in direction of mold open/close. Deeper pockets need more draft (add 0.5° per 25mm depth for HPDC, 1° per 25mm for Permanent Mold)',
        'rationale': f'Draft angles allow easy part ejection from die. Without draft: (1) Shrinkage grip - molten aluminum shrinks when cooling (1.3% linear shrinkage) and grips mold core tightly, (2) Surface friction - as-cast surface roughness creates friction during ejection, (3) Ejection damage - excessive force causes warpage, surface damage, dimensional distortion. {min_draft}° draft for {process_name} ensures clean ejection without damage. Vertical walls (0° draft) require expensive side actions/slides in die (+$5,000-$15,000 per slide) or post-CNC machining. Deep pockets need additional draft: {"add 0.5° per 25mm depth" if process_type == "hpdc" else "add 1° per 25mm depth"}. Example: {"50mm deep pocket needs 1.5° base + 1° depth = 2.5° total" if process_type == "hpdc" else "50mm deep pocket needs 3° base + 2° depth = 5° total"}.',
        'cost_impact': f'No draft: +20-30% cycle time from difficult ejection, 15-25% scrap rate from sticking/warpage, potential die damage ($10,000-$50,000 repair). Side actions for 0° draft: +$5,000-$15,000 per slide'
    })
    
    # RULE 3: Corner Radii
    rule_name = "Corner Radii and Fillets"
    rule_standard = "Minimum internal radius 0.5mm. External radius = internal R + wall thickness per 930-00166"
    
    warnings.append({
        'category': 'Corner Radii',
        'message': 'Verify all internal corners have minimum 0.5mm radius',
        'recommendation': 'Add 0.5mm minimum internal radius, external radius = internal R + wall thickness',
        'rationale': 'Sharp corners are stress concentrators (3-5× normal stress) where cracks initiate. Sharp mold corners impossible to maintain over tool life.'
    })
    rationale.append("⚠️ Verify all corners have appropriate radii (0.5mm minimum internal).")
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'WARNING',
        'measured_value': 'Design consideration',
        'evaluation': 'Checking criteria: Internal corner radius must be ≥0.5mm. External corner radius should equal internal R + wall thickness to maintain uniform wall. Analysis: Corner radii cannot be automatically detected from STEP geometry. Result: WARNING - manual verification required.',
        'recommendation': 'Internal: ≥0.5mm. External: internal R + wall thickness. Example: 3mm wall with 0.5mm internal radius needs 3.5mm external radius. Exception: Parting line edges should not have radii unless functionally required',
        'rationale': 'Sharp corners cause multiple critical failures: (1) Stress concentrations - sharp corners concentrate stress 3-5× normal levels, creating crack initiation points where parts fail under load. Fatigue life reduced 60-80%. (2) Mold wear - sharp corners in die are impossible to maintain over production life (100,000+ shots for HPDC). Corners erode and radius naturally, causing dimensional drift. (3) Flow restrictions - sharp corners restrict molten aluminum flow, causing incomplete filling, cold shuts, and porosity. (4) Cooling issues - sharp external corners opposite internal corners create thick sections that cool slowly, causing shrink porosity. External radius formula: external R = internal R + wall thickness. This maintains uniform wall thickness and prevents thick sections. Example: 3mm wall with 0.5mm internal radius needs 3.5mm external radius (0.5mm + 3mm). Exception: Parting line edges should remain sharp unless function requires radius (sharp edges help hide parting line flash).',
        'cost_impact': 'Sharp corners: 40-60% reduction in part strength, 60-80% reduction in fatigue life, 20-30% shorter tool life from erosion, higher scrap from flow issues (15-25%)'
    })
    
    # RULE 4: Minimum As-Cast Hole Diameter
    rule_name = "Minimum As-Cast Hole Diameter"
    rule_standard = f"Cast holes ≥{min_hole_dia}mm diameter. Smaller holes drilled post-CNC per 930-00166"
    
    suggestions.append({
        'opportunity': f'Cast holes ≥{min_hole_dia}mm, drill holes <{min_hole_dia}mm post-CNC',
        'savings': f'$0.30-$0.80 per hole by casting vs drilling',
        'difficulty': 'Easy',
        'rationale': f'Holes ≥{min_hole_dia}mm can be cast reliably. Smaller holes risk core pin breakage and should be drilled post-CNC.'
    })
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'INFO',
        'measured_value': 'Design guideline',
        'evaluation': f'Checking criteria: Holes ≥{min_hole_dia}mm diameter should be cast with core pins. Holes <{min_hole_dia}mm should be drilled post-CNC. Analysis: Hole diameter and depth ratio determines castability. Result: INFO - design guideline for hole specification.',
        'recommendation': f'Cast holes ≥{min_hole_dia}mm diameter, drill holes <{min_hole_dia}mm post-CNC. Verify hole depth:diameter ratio with supplier (typically ≤4:1 for blind holes)',
        'rationale': f'{"HPDC hole guidelines: Holes ≥5mm diameter can be cast reliably with steel core pins. Smaller holes (<5mm) risk core pin breakage during casting (high injection pressure 10,000-15,000 psi bends thin pins), poor hole quality (pins deflect causing oval holes), and difficult ejection (pins stick in solidified aluminum). Through-holes preferred over blind holes (easier ejection, no trapped air). Blind hole depth:diameter ratio should be ≤4:1 (e.g., 5mm diameter → 20mm max depth). Deeper holes require drilling. Hole position tolerance: ±0.25mm as-cast, tighten with post-CNC if needed." if process_type == "hpdc" else "Permanent Mold hole guidelines: Minimum hole diameter depends on depth and draft angle. Gravity feed (low pressure) limits small hole casting. Consult supplier for specific hole diameter:depth ratios. Through-holes more reliable than blind holes. Core pins must have adequate draft (3°+) for gravity ejection. Holes <6mm typically drilled post-CNC for better quality and tighter tolerances."} Cost analysis: Casting holes saves $0.30-$0.80 per hole vs drilling (eliminates secondary operation, reduces cycle time). However, holes near minimum diameter may have looser tolerances requiring post-CNC reaming for precision fits.',
        'cost_impact': f'Casting holes ≥{min_hole_dia}mm: saves $0.30-$0.80 per hole vs drilling. Holes <{min_hole_dia}mm: must drill (+cost, +lead time). Core pin breakage: $200-$500 per pin replacement + downtime'
    })
    
    # RULE 5: Machining Stock
    rule_name = "Machining Stock (Over-Cast Material)"
    rule_standard = f"Add {machining_stock}mm over-cast material for machined surfaces per 930-00166"
    
    suggestions.append({
        'opportunity': f'Add {machining_stock}mm machining stock to surfaces requiring precision',
        'savings': 'Ensures machinable surface without hitting porosity',
        'difficulty': 'Easy',
        'rationale': f'{"HPDC: 1mm stock ensures sufficient material without going deep into part where porosity risk is higher." if process_type == "hpdc" else "Permanent Mold: 1.5-2mm stock provides adequate material. Less porosity risk than HPDC."}'
    })
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'INFO',
        'measured_value': 'Design guideline',
        'evaluation': f'Checking criteria: Machined surfaces require {machining_stock}mm over-cast material (stock) for {process_name}. Analysis: Machining stock must be specified in design for surfaces requiring precision or finish. Result: INFO - design specification requirement.',
        'recommendation': f'Add {machining_stock}mm over-cast material to all surfaces requiring machining. Mark machined surfaces on drawing with finish symbol and tolerance',
        'rationale': f'{"HPDC machining stock guidelines: Add 1mm stock to machined surfaces. Critical: Do NOT add excess stock - deeper machining increases risk of hitting porosity. HPDC parts have surface porosity (shrink voids) concentrated 1-2mm below surface due to rapid cooling and high pressure. Machining removes 1mm surface layer (good material) to achieve precision and finish. Going deeper (>1.5mm) risks exposing internal porosity (voids, gas pockets) causing: leaks in pressure-tight parts, cosmetic defects, dimensional issues (voids collapse under cutting forces). Stay within 1mm depth for reliable results." if process_type == "hpdc" else "Permanent Mold machining stock guidelines: Add 1.5-2mm stock to machined surfaces. Permanent mold has lower porosity risk than HPDC (slower cooling, lower pressure, better feeding). Excess material less risky but increases CNC time and cost. Thicker stock allows for: surface variation compensation (as-cast surface ±0.3-0.5mm), tool wear compensation, multiple machining passes for tight tolerances."} Machining stock ensures: (1) Sufficient material for precision machining to final dimension, (2) Accounts for as-cast surface variation, (3) Allows for tool wear compensation during production runs. Mark machined surfaces on drawing with finish symbol (Ra value) and dimensional tolerance.',
        'cost_impact': f'Insufficient stock: 20-30% scrap from undersized features, cannot achieve specified dimensions. Excess stock: +10-20% CNC time and cost. {"HPDC: Deep machining (>1.5mm) risks porosity exposure (30-40% scrap rate)." if process_type == "hpdc" else "Permanent Mold: Excess stock less risky but wasteful."}'
    })
    
    # RULE 6: Uniform Wall Thickness
    rule_name = "Uniform Wall Thickness"
    rule_standard = "Maintain consistent wall thickness. Avoid abrupt transitions per 930-00166"
    
    warnings.append({
        'category': 'Wall Uniformity',
        'message': 'Verify uniform wall thickness throughout part',
        'recommendation': 'Maintain consistent thickness, use gradual transitions (3:1 taper minimum)',
        'rationale': 'Non-uniform walls cause differential cooling, warpage, and porosity. Abrupt transitions create turbulence and pressure changes.'
    })
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'WARNING',
        'measured_value': 'Design consideration',
        'evaluation': 'Checking criteria: Wall thickness variation should be minimized. Transitions between different thicknesses must use gradual 3:1 taper (length = 3× thickness change). Analysis: Uniform wall thickness cannot be automatically verified from geometry. Result: WARNING - critical design consideration.',
        'recommendation': 'Maintain consistent wall thickness throughout part. Use gradual 3:1 taper for transitions. Bridge isolated features to adjacent features for better flow',
        'rationale': 'Non-uniform walls cause multiple defects in die casting: (1) Differential cooling rates - thick sections cool slower than thin sections (cooling time proportional to thickness²), creating thermal gradients that cause warpage and residual stress, (2) Porosity at transitions - abrupt thick-to-thin transitions create turbulence and pressure changes in molten metal flow, trapping air bubbles and creating shrinkage voids, (3) Sink marks at thick sections - thick areas shrink more during solidification (aluminum shrinks 6-7%), pulling surface inward creating visible depressions, (4) Flow problems - molten metal flows easily through thick sections but hesitates at thin sections, creating cold shuts (weak seams) and incomplete fill. Design solutions: (1) Keep walls consistent - target single nominal thickness throughout part, (2) Gradual transitions - use 3:1 taper minimum between different thicknesses (changing from 3mm to 6mm requires 9mm taper length), (3) Bridge hanging features - connect isolated features to adjacent features with ribs or webs for better material flow and support, (4) Avoid abrupt changes - step changes create stress concentrations and flow turbulence. Example: Boss on 3mm wall should taper from 3mm to boss diameter over 3× the thickness increase.',
        'cost_impact': 'Non-uniform walls: 25-35% higher scrap rate from warpage and porosity, 15-20% longer cycle time (must wait for thickest section to solidify), parts fail dimensional inspection, X-ray reveals internal voids'
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
        assessment = f"EXCELLENT - Well-designed for {process_name}"
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
• Wall thickness: {"Optimal" if min_thickness >= nominal_wall else "Review required"} (minimum {min_wall}mm, nominal {nominal_wall}mm)
• Draft angles: Verify {min_draft}° minimum on all vertical walls
• Corner radii: Add 0.5mm minimum internal radius
• Uniform thickness: Critical for quality casting
• Machining stock: Add {machining_stock}mm to machined surfaces

**Process Specifications:**
• Surface finish: {surface_finish}
• Linear tolerance: {linear_tol}
• Minimum cast hole: {min_hole_dia}mm diameter

**Recommendation:** {"Design is manufacturable with " + process_name + "." if len(issues) == 0 else "Address critical wall thickness issues before tooling."}

**Based on:** 930-00166_R01 - High Pressure Die Cast and Gravity Cast Permanent Mold Design Guidelines (20 pages)"""
    
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
        'parser': parser,  # Include parser for 3D visualization
        'holes': [],  # Die casting typically doesn't have pre-drilled holes
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
            'cost_savings': suggestions[:5]
        }
    }
