"""
Enhanced Manufacturing Process Analyzers with Comprehensive Industry-Standard DFM Rules
Includes specific geometric relationships and measurable criteria for all processes.

NOTE (CR-27652557): This module was rebuilt from a corrupted source per
.kiro/specs/dfm-analyzer-cr-analyzer-fixes/design.md § 10. All recoverable
threshold values are preserved verbatim; values that could not be recovered
from surrounding context are marked with `# TODO(CR-27652557): recover
original threshold` and use a conservative default. Assessment-ladder cutoffs
default to 90/75/60 to match die_casting_enhanced_v2.py and
cnc_machining_enhanced.py.
"""
from typing import Dict


# ---------------------------------------------------------------------------
# Sheet metal
# ---------------------------------------------------------------------------
def analyze_sheet_metal(parser, material, geometry) -> Dict:
    """Analyze for sheet metal fabrication with comprehensive DFM rules."""
    issues = []
    warnings = []
    suggestions = []
    passed = []
    rationale = []
    all_rules = []  # Complete rule-by-rule breakdown

    dims = geometry.get('dimensions', {}) or {}
    volume = geometry.get('volume', 0)
    min_thickness = geometry.get('estimated_min_thickness', 0)

    # ----- RULE 1: Material thickness ------------------------------------
    rule_name = "Material Thickness"
    rule_standard = (
        "Minimum 0.5mm (20 gauge) steel, 0.8mm aluminum. Optimal: 0.9-3.0mm"
    )
    if min_thickness > 0:
        if min_thickness < 0.5:  # 0.020"
            issues.append({
                'category': 'Material Thickness',
                'message': f'Thickness {min_thickness:.2f}mm too thin for reliable bending',
                'recommendation': 'Increase to minimum 0.5mm (0.020") for sheet metal',
                'rationale': (
                    'Very thin material is prone to tearing during bending and '
                    'difficult to handle in press brake operations.'
                ),
            })
            rationale.append(
                f"❌ Material thickness {min_thickness:.2f}mm is below minimum "
                f"for sheet metal fabrication."
            )
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'FAIL',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': (
                    f'Material thickness of {min_thickness:.2f}mm is below the '
                    f'minimum requirement of 0.5mm'
                ),
                'recommendation': 'Increase to minimum 0.5mm for steel or 0.8mm for aluminum',
                'rationale': (
                    'Material below 0.5mm tears during bending, is difficult to '
                    'handle in press brake operations, and distorts easily under '
                    'forming pressure. Press brake tooling cannot reliably grip '
                    'and form material this thin without tearing or wrinkling.'
                ),
                'cost_impact': (
                    'Parts with material <0.5mm will likely be rejected by '
                    'fabricators or require 150-200% cost premium for '
                    'specialized micro-forming'
                ),
            })
        elif min_thickness < 0.9:  # 0.036"
            warnings.append({
                'category': 'Material Thickness',
                'message': f'Thickness {min_thickness:.2f}mm is below the optimal 0.9-3.0mm range',
                'recommendation': 'Verify formability with fabricator; consider 0.9mm+ if possible',
                'rationale': (
                    'Material between 0.5mm and 0.9mm is formable but more '
                    'sensitive to tearing at tight bend radii and to handling '
                    'damage. Most fabricators prefer 0.9mm and above for '
                    'consistent quality.'
                ),
            })
            rationale.append(
                f"⚠️ Material thickness {min_thickness:.2f}mm is below optimal — "
                f"verify formability."
            )
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': (
                    f'Material thickness of {min_thickness:.2f}mm is formable '
                    f'but below the 0.9mm optimal threshold'
                ),
                'recommendation': 'Increase to ≥0.9mm where possible for consistent forming',
                'rationale': (
                    'Material below 0.9mm is more sensitive to tearing at tight '
                    'bend radii and to handling damage; many fabricators prefer '
                    '≥0.9mm for repeatable quality.'
                ),
                'cost_impact': '10-20% premium typical for thin-gauge forming and handling',
            })
        else:
            passed.append({
                'check': 'Material Thickness',
                'status': f'{min_thickness:.2f}mm - Optimal',
            })
            rationale.append(
                f"✓ Material thickness {min_thickness:.2f}mm is within optimal "
                f"range for sheet metal fabrication."
            )
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'PASS',
                'measured_value': f'{min_thickness:.2f}mm',
                'evaluation': (
                    f'Material thickness of {min_thickness:.2f}mm is within '
                    f'optimal range for sheet metal fabrication'
                ),
                'recommendation': 'No changes needed - thickness is optimal',
                'rationale': (
                    'Material thickness in the 0.9-6.0mm range provides good '
                    'formability, adequate strength, and can be processed with '
                    'standard press brake equipment and tooling. This range '
                    'accommodates most sheet metal applications efficiently.'
                ),
                'cost_impact': 'Standard fabrication cost - no premium',
            })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': 'Not measured',
            'evaluation': 'Material thickness could not be measured from CAD geometry',
            'recommendation': 'Verify material thickness manually in CAD software',
            'rationale': (
                'Thickness analysis requires a watertight 3D model. Ensure your '
                'CAD file is properly exported.'
            ),
            'cost_impact': 'N/A',
        })

    # ----- RULE 2: Bend radius to thickness ratio ------------------------
    rule_name = "Bend Radius to Thickness Ratio"
    rule_standard = (
        "Minimum bend radius = 1× thickness (steel), 1.5× thickness (aluminum). "
        "Standard: 1.5-2× thickness"
    )
    if min_thickness > 0:
        min_bend_radius = min_thickness * 1.5  # Standard for most materials
        warnings.append({
            'category': 'Bend Radius',
            'message': f'Minimum bend radius should be {min_bend_radius:.2f}mm (1.5× thickness)',
            'recommendation': f'Use {min_bend_radius:.2f}mm minimum radius for all bends',
            'rationale': (
                'Bend radius below 1× thickness causes cracking. Standard '
                'practice: 1.5-2× thickness for reliable forming without '
                'material failure.'
            ),
        })
        rationale.append(
            f"⚠️ Verify bend radii meet minimum {min_bend_radius:.2f}mm "
            f"(1.5× thickness)."
        )
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'WARNING',
            'measured_value': f'Material thickness: {min_thickness:.2f}mm',
            'evaluation': (
                f'For {min_thickness:.2f}mm material, minimum bend radius must '
                f'be {min_bend_radius:.2f}mm'
            ),
            'recommendation': (
                f'Ensure all bends have minimum {min_bend_radius:.2f}mm '
                f'radius (1.5× thickness)'
            ),
            'rationale': (
                f'Bend radius below 1× thickness causes material cracking and '
                f'failure. Tight bends require higher tonnage and may crack '
                f'during forming. Standard practice: 1.5-2× thickness provides '
                f'reliable forming without material failure. For '
                f'{min_thickness:.2f}mm material: minimum {min_bend_radius:.2f}mm '
                f'radius.'
            ),
            'cost_impact': (
                f'Using {min_bend_radius:.2f}mm radius: standard cost. Tighter '
                f'radii: +40-60% cost due to specialized tooling and higher '
                f'reject rates'
            ),
        })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': 'Not applicable',
            'evaluation': 'Bend radius cannot be verified without material thickness',
            'recommendation': 'Manually verify bend radii meet 1.5× thickness minimum',
            'rationale': (
                'This rule requires material thickness measurement. Ensure all '
                'bends have appropriate radii.'
            ),
            'cost_impact': 'N/A',
        })

    # ----- RULE 3: Minimum flange length ---------------------------------
    rule_name = "Minimum Flange Length"
    rule_standard = (
        "Minimum flange length = 4× thickness + bend radius. "
        "Absolute minimum: 12.7mm (0.5\")"
    )
    if min_thickness > 0:
        min_flange = max(4 * min_thickness + (min_thickness * 1.5), 12.7)
        warnings.append({
            'category': 'Flange Length',
            'message': f'Minimum flange length should be {min_flange:.1f}mm',
            'recommendation': f'Ensure all flanges are at least {min_flange:.1f}mm long',
            'rationale': (
                'Short flanges are difficult to hold during bending and may '
                'slip or distort. Minimum: 4× thickness + bend radius, or '
                '12.7mm absolute minimum.'
            ),
        })
        rationale.append(
            f"⚠️ Verify flange lengths meet minimum {min_flange:.1f}mm."
        )
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'WARNING',
            'measured_value': f'Material thickness: {min_thickness:.2f}mm',
            'evaluation': (
                f'For {min_thickness:.2f}mm material, minimum flange length '
                f'is {min_flange:.1f}mm'
            ),
            'recommendation': (
                f'Ensure all flanges are at least {min_flange:.1f}mm long'
            ),
            'rationale': (
                f'Short flanges are difficult to hold during bending and may '
                f'slip, twist, or distort under forming pressure. The press '
                f'brake tooling needs sufficient material to grip. Formula: '
                f'4× thickness + bend radius. For {min_thickness:.2f}mm '
                f'material: {min_flange:.1f}mm minimum. Absolute minimum for '
                f'any thickness: 12.7mm (0.5").'
            ),
            'cost_impact': (
                'Short flanges require custom fixtures ($500-1500) and '
                'increase setup time by 30-50%'
            ),
        })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': 'Not applicable',
            'evaluation': 'Flange length cannot be calculated without material thickness',
            'recommendation': 'Manually verify flange lengths meet minimum requirements',
            'rationale': (
                'Ensure all flanges meet the 4× thickness + bend radius '
                'formula, with 12.7mm absolute minimum.'
            ),
            'cost_impact': 'N/A',
        })

    # ----- RULE 4: Hole-to-edge distance --------------------------------
    rule_name = "Hole-to-Edge Distance"
    rule_standard = (
        "Minimum distance from hole edge to part edge = 2× thickness + bend "
        "radius, or 2.5mm minimum"
    )
    if min_thickness > 0 and dims:
        min_edge_distance = max(2 * min_thickness + (min_thickness * 1.5), 2.5)
        # Estimate if holes might be near edges (simplified check based on part size)
        min_dim = min(dims.values())
        if min_dim < min_edge_distance * 3:  # If part is small, holes likely near edges
            issues.append({
                'category': 'Hole-to-Edge Distance',
                'message': (
                    f'Holes may be too close to edges (minimum distance: '
                    f'{min_edge_distance:.1f}mm)'
                ),
                'recommendation': (
                    f'Maintain {min_edge_distance:.1f}mm minimum from hole '
                    f'edge to part edge'
                ),
                'rationale': (
                    f'Holes too close to edges cause material tearing during '
                    f'punching and distortion during bending. Minimum: 2× '
                    f'thickness + bend radius = {min_edge_distance:.1f}mm '
                    f'for {min_thickness:.2f}mm material.'
                ),
            })
            rationale.append(
                f"❌ Holes detected near edges - minimum distance "
                f"{min_edge_distance:.1f}mm required."
            )
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'FAIL',
                'measured_value': 'Part size suggests holes near edges',
                'evaluation': (
                    f'Holes appear to be closer than {min_edge_distance:.1f}mm '
                    f'to part edges'
                ),
                'recommendation': (
                    f'Move holes to maintain {min_edge_distance:.1f}mm '
                    f'minimum distance from hole edge to part edge'
                ),
                'rationale': (
                    f'Holes too close to edges cause material tearing during '
                    f'punching operations and distortion during bending. The '
                    f'thin web of material between hole and edge cannot '
                    f'withstand forming forces. Formula: 2× thickness + bend '
                    f'radius. For {min_thickness:.2f}mm material: '
                    f'{min_edge_distance:.1f}mm minimum. Absolute minimum '
                    f'for any thickness: 2.5mm.'
                ),
                'cost_impact': (
                    'Holes too close to edges result in 30-50% scrap rate '
                    'during production. May require redesign or secondary '
                    'operations (+50-100% cost)'
                ),
            })
        else:
            passed.append({
                'check': 'Hole-to-Edge Distance',
                'status': 'Adequate clearance',
            })
            rationale.append(
                f"✓ Hole-to-edge distances appear adequate (minimum "
                f"{min_edge_distance:.1f}mm)."
            )
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'PASS',
                'measured_value': 'Part geometry suggests adequate clearance',
                'evaluation': 'Holes appear to maintain adequate distance from part edges',
                'recommendation': 'Verify all holes meet minimum edge distance requirements',
                'rationale': (
                    f'Holes with adequate edge distance ({min_edge_distance:.1f}mm '
                    f'minimum for {min_thickness:.2f}mm material) can be '
                    f'punched cleanly without tearing and will not distort '
                    f'during bending operations. The material web between '
                    f'hole and edge is strong enough to withstand forming '
                    f'forces.'
                ),
                'cost_impact': 'Standard punching cost - no premium',
            })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': 'Not applicable',
            'evaluation': 'Hole-to-edge distance cannot be verified from geometry',
            'recommendation': 'Manually verify all holes maintain minimum edge distance',
            'rationale': (
                'Ensure holes meet the 2× thickness + bend radius formula, '
                'with 2.5mm absolute minimum.'
            ),
            'cost_impact': 'N/A',
        })

    # ----- RULE 8: Part size --------------------------------------------
    rule_name = "Part Size"
    rule_standard = (
        "Standard press brake capacity: 1500mm × 3000mm. Optimal: <1000mm. "
        "Oversize threshold: 2500mm (100\")"
    )
    if dims:
        max_dim = max(dims.values())
        if max_dim > 2500:  # 100" — exceeds standard press brake envelope
            issues.append({
                'category': 'Part Size',
                'message': (
                    f'Oversized: {max_dim:.1f}mm exceeds standard press brake '
                    f'capacity'
                ),
                'recommendation': (
                    'Redesign to fit 2500mm (100") envelope or split into a '
                    'welded assembly'
                ),
                'rationale': (
                    # TODO(CR-27652557): recover original threshold
                    # Original message body was truncated in the source; this
                    # paraphrases sheet_metal_enhanced.py's oversize warning.
                    'Parts over 2500mm exceed the working envelope of standard '
                    'press brakes; specialty fabricators or split-and-weld '
                    'assemblies are required, with 200-400% cost increase.'
                ),
            })
            rationale.append(
                f"❌ Part size {max_dim:.1f}mm exceeds standard press brake "
                f"capacity - 200-400% cost increase."
            )
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'FAIL',
                'measured_value': f'{max_dim:.1f}mm maximum dimension',
                'evaluation': (
                    f'Part dimension of {max_dim:.1f}mm exceeds the 2500mm '
                    f'oversize threshold'
                ),
                'recommendation': 'Split into welded assembly or use specialty fabricator',
                'rationale': (
                    'Parts over 2500mm require non-standard equipment and '
                    'add significant cost and lead time.'
                ),
                'cost_impact': '200-400% cost increase typical for oversize parts',
            })
        elif max_dim > 1500:  # 60"
            warnings.append({
                'category': 'Part Size',
                'message': (
                    f'Large dimension {max_dim:.1f}mm requires large press brake'
                ),
                'recommendation': 'Verify fabricator has 2000mm+ press brake capacity',
                'rationale': (
                    'Parts over 1500mm require large-format press brakes which '
                    'are less common and more expensive; setup costs increase '
                    '30-50%.'
                ),
            })
            rationale.append(
                f"⚠️ Part size {max_dim:.1f}mm requires large press brake "
                f"equipment - 30-50% cost premium."
            )
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'{max_dim:.1f}mm maximum dimension',
                'evaluation': (
                    f'Part dimension of {max_dim:.1f}mm requires a '
                    f'large-format press brake'
                ),
                'recommendation': 'Confirm fabricator has 2000mm+ press brake capacity',
                'rationale': (
                    'Large-format press brakes are less common; expect 30-50% '
                    'setup cost premium.'
                ),
                'cost_impact': '30-50% cost premium for large-format forming',
            })
        else:
            passed.append({
                'check': 'Part Size',
                'status': 'Fits standard press brakes',
            })
            rationale.append(
                f"✓ Part size fits standard press brake capacity "
                f"(1500mm bed length)."
            )
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'PASS',
                'measured_value': f'{max_dim:.1f}mm maximum dimension',
                'evaluation': (
                    f'Part dimension of {max_dim:.1f}mm fits within standard '
                    f'press brake capacity'
                ),
                'recommendation': 'No changes needed - part size is optimal',
                'rationale': (
                    'Parts under 1500mm can be processed on standard press '
                    'brakes, maximizing shop compatibility and minimizing cost.'
                ),
                'cost_impact': 'Standard fabrication cost - no premium',
            })

    # ----- RULE 9: Material-specific formability -------------------------
    if 'aluminum' in material.lower() and '6061' in material:
        warnings.append({
            'category': 'Material Formability',
            'message': '6061-T6 aluminum has limited formability',
            'recommendation': (
                'Use 5052-H32 for complex bends, or anneal 6061 before forming'
            ),
            'rationale': (
                '6061-T6 is prone to cracking at tight bend radii. 5052-H32 '
                'offers excellent formability.'
            ),
        })
        rationale.append(
            "⚠️ 6061-T6 aluminum selected - limited formability, prone to "
            "cracking at bends."
        )
        all_rules.append({
            'name': 'Material Formability',
            'standard': (
                '5052-H32 aluminum recommended for sheet metal. 6061-T6 has '
                'poor formability'
            ),
            'status': 'WARNING',
            'measured_value': material,
            'evaluation': (
                '6061-T6 aluminum has limited formability and is prone to '
                'cracking'
            ),
            'recommendation': (
                'Use 5052-H32 for complex bends, or anneal 6061 to O-temper '
                'before forming'
            ),
            'rationale': (
                '6061-T6 is heat-treated for strength but has poor ductility '
                '(8% elongation). Cracks at tight bend radii. 5052-H32 offers '
                'excellent formability (25% elongation). Alternative: Anneal '
                '6061 to O-temper before forming, then heat-treat after.'
            ),
            'cost_impact': (
                'Annealing and re-heat-treating adds $50-100 per part. High '
                'scrap rate (20-30%) if formed in T6 condition.'
            ),
        })
    elif 'aluminum' in material.lower() and '5052' in material:
        passed.append({
            'check': 'Material Selection',
            'status': 'Excellent formability',
        })
        rationale.append(
            "✓ 5052 aluminum offers excellent formability for sheet metal "
            "operations."
        )
        all_rules.append({
            'name': 'Material Formability',
            'standard': (
                '5052-H32 aluminum recommended for sheet metal. 6061-T6 has '
                'poor formability'
            ),
            'status': 'PASS',
            'measured_value': material,
            'evaluation': (
                '5052 aluminum offers excellent formability for sheet metal '
                'operations'
            ),
            'recommendation': 'No changes needed - material choice is optimal',
            'rationale': (
                '5052-H32 aluminum offers excellent formability (25% '
                'elongation), good corrosion resistance, and can handle tight '
                'bend radii without cracking. Industry standard for sheet '
                'metal fabrication.'
            ),
            'cost_impact': 'Standard material cost - no premium',
        })
    elif 'steel' in material.lower() and 'stainless' in material.lower():
        warnings.append({
            'category': 'Material Formability',
            'message': 'Stainless steel requires larger bend radii',
            'recommendation': 'Use 2× material thickness minimum bend radius for stainless',
            'rationale': (
                'Stainless steel work-hardens during bending and requires '
                'larger radii than mild steel. Minimum radius = 2× thickness '
                '(vs 1× for mild steel). 304 stainless has moderate '
                'formability; 316 is more difficult. Expect 20-30% higher '
                'forming costs vs mild steel.'
            ),
        })
        rationale.append(
            "⚠️ Stainless steel requires 2× thickness bend radius - 20-30% "
            "cost premium."
        )
        all_rules.append({
            'name': 'Material Formability',
            'standard': '5052-H32 aluminum or mild steel recommended for sheet metal',
            'status': 'WARNING',
            'measured_value': material,
            'evaluation': 'Stainless steel work-hardens; requires larger bend radii',
            'recommendation': 'Use 2× thickness minimum bend radius',
            'rationale': (
                'Stainless steel work-hardens and requires 2× thickness bend '
                'radii. Expect 20-30% higher forming cost vs mild steel.'
            ),
            'cost_impact': '20-30% cost premium vs mild steel',
        })
    elif 'steel' in material.lower():
        passed.append({
            'check': 'Material Selection',
            'status': 'Excellent formability',
        })
        rationale.append(
            f"✓ {material} (mild steel) offers excellent formability for "
            f"sheet metal operations."
        )
        all_rules.append({
            'name': 'Material Formability',
            'standard': '5052-H32 aluminum or mild steel recommended for sheet metal',
            'status': 'PASS',
            'measured_value': material,
            'evaluation': 'Mild steel offers excellent formability for sheet metal',
            'recommendation': 'No changes needed - material choice is appropriate',
            'rationale': 'Mild steel forms reliably with 1× thickness bend radius.',
            'cost_impact': 'Standard material cost - no premium',
        })
    else:
        all_rules.append({
            'name': 'Material Formability',
            'standard': '5052-H32 aluminum or mild steel recommended for sheet metal',
            'status': 'INFO',
            'measured_value': material,
            'evaluation': 'Material formability depends on specific alloy and temper',
            'recommendation': 'Verify material is suitable for bending operations',
            'rationale': (
                'Different materials and tempers have different formability. '
                'Consult material datasheets for minimum bend radius and '
                'elongation values.'
            ),
            'cost_impact': 'Varies by material',
        })

    # ----- RULE 10: Bend sequence and tooling access ---------------------
    suggestions.append({
        'opportunity': 'Design for bend sequence - avoid interference',
        'savings': '15-25% by eliminating custom tooling and secondary operations',
        'difficulty': 'Medium',
        'rationale': (
            # TODO(CR-27652557): recover original threshold
            # Original rationale was truncated mid-sentence ("Complex bend
            # sequences may s brake tooling."); paraphrased to match intent.
            'Complex bend sequences may interfere with standard press brake '
            'tooling. Design parts so bends can be formed in a logical '
            'sequence without interference. Avoid bends that create enclosed '
            'channels or require special tooling. Each custom tool setup '
            'adds $200-500.'
        ),
    })

    # Cost optimization suggestions
    suggestions.append({
        'opportunity': 'Use standard bend radius (0.76mm / 0.030" or 1.5mm)',
        'savings': 'Eliminates custom tooling costs ($2,000-$5,000 per tool)',
        'difficulty': 'Easy',
        'rationale': (
            # TODO(CR-27652557): recover original threshold
            # Original rationale was truncated ("Standard ng:"); paraphrased.
            'Standard press brake tooling: 0.76mm (0.030"), 1.5mm, 3.0mm '
            'radius. Non-standard radii require custom tooling '
            '($2,000-5,000) and longer setup times. Use standard radii '
            'unless functionally required.'
        ),
    })

    suggestions.append({
        'opportunity': 'Standardize hole sizes to common punches',
        'savings': '20-30% by using turret punch vs drilling',
        'difficulty': 'Easy',
        'rationale': (
            # TODO(CR-27652557): recover original threshold
            # Original rationale was truncated ("Turret punching ing.");
            # paraphrased while preserving the standard punch sizes
            # (3.2 / 6.4 / 9.5 / 12.7 mm) verbatim.
            'Standard punch sizes: 3.2mm (1/8"), 6.4mm (1/4"), 9.5mm (3/8"), '
            '12.7mm (1/2"). Turret punching using these standards is fast '
            'and inexpensive. Non-standard holes require drilling (slower, '
            'more expensive). Use standard sizes for maximum cost savings.'
        ),
    })

    suggestions.append({
        'opportunity': 'Minimize number of bends',
        'savings': '10-15% per bend eliminated',
        'difficulty': 'Medium',
        'rationale': (
            # TODO(CR-27652557): recover original threshold
            # Original rationale was truncated; paraphrased.
            'Each bend requires a separate setup and adds 2-5 minutes of '
            'cycle time. Minimizing bends shortens cycle time and reduces '
            'tooling cost.'
        ),
    })

    # ----- Score and summary --------------------------------------------
    total_checks = len(issues) + len(warnings) + len(passed)
    if total_checks > 0:
        score = (len(passed) * 100 + len(warnings) * 50) / total_checks
    else:
        score = 85.0
    score_explanation = (
        f"Score from {len(passed)} passed checks, {len(warnings)} warnings, "
        f"{len(issues)} critical issues"
    )

    # Assessment ladder cutoffs default to 90/75/60 to match
    # die_casting_enhanced_v2.py and cnc_machining_enhanced.py.
    if score >= 90:
        assessment = "EXCELLENT - Well-suited for sheet metal fabrication"
    elif score >= 75:
        assessment = "GOOD - Minor optimization recommended"
    elif score >= 60:
        assessment = "ACCEPTABLE - Review warnings carefully"
    else:
        assessment = "NEEDS REVISION - Address critical issues before production"

    summary = (
        f"**Overall Assessment:** {assessment}\n"
        f"**Manufacturability Score:** {score:.1f}/100\n\n"
        f"**Analysis Results:** {len(passed)} checks passed, "
        f"{len(warnings)} warnings, {len(issues)} critical issues\n\n"
        f"**Key Findings:**\n"
        f"• Material thickness: {min_thickness:.2f}mm - "
        f"{'Optimal' if 0.9 <= min_thickness <= 6.0 else 'Review required'}\n"
        f"• Bend radius must be ≥1× material thickness\n"
        f"• Holes must be ≥2.5× thickness from bends\n"
        f"• Flange length must be ≥4× thickness or 12.7mm minimum\n\n"
        f"**Recommendation:** "
        f"{'Design is manufacturable. Address warnings to optimize cost and quality.' if len(issues) == 0 else 'Address critical issues before production - holes near bends and edge distances require revision.'}"
    )

    return {
        'success': True,
        'process': 'Sheet Metal',
        'material': material,
        'score': round(score, 1),
        'score_explanation': score_explanation,
        'issues': len(issues),
        'warnings': len(warnings),
        'suggestions': len(suggestions),
        'passed': len(passed),
        'all_rules': all_rules,  # Complete rule breakdown
        'geometry_info': {
            'dimensions': (
                f"{dims.get('x', 0):.1f} x {dims.get('y', 0):.1f} x "
                f"{dims.get('z', 0):.1f} mm"
            ),
            'volume': f"{volume:.2f} mm³",
            'min_thickness': (
                f"{min_thickness:.2f} mm" if min_thickness > 0 else 'N/A'
            ),
        },
        'rationale': rationale,
        'summary': summary,
        'details': {
            'critical_issues': issues[:5],
            'warnings': warnings[:5],
            'cost_savings': suggestions[:4],
        },
    }


# ---------------------------------------------------------------------------
# Injection molding
# ---------------------------------------------------------------------------
def analyze_injection_molding(parser, material, geometry) -> Dict:
    """Analyze for injection molding with comprehensive DFM rules."""
    issues = []
    warnings = []
    suggestions = []
    passed = []
    rationale = []

    dims = geometry.get('dimensions', {}) or {}
    volume = geometry.get('volume', 0)
    min_thickness = geometry.get('estimated_min_thickness', 0)

    # ----- RULE 1: Wall thickness (SPI standards) -----------------------
    if min_thickness > 0:
        if min_thickness < 0.5:
            issues.append({
                'category': 'Wall Thickness',
                'message': f'Critical: Wall thickness {min_thickness:.2f}mm too thin',
                'recommendation': 'Increase to 0.75-3.0mm range for injection molding',
                'rationale': (
                    'Walls thinner than 0.5mm cause short shots (incomplete '
                    'filling). Plastic flow resistance increases exponentially '
                    'below 0.5mm. Minimum: 0.5mm small parts, 0.75mm larger '
                    'parts.'
                ),
            })
            rationale.append(
                f"❌ Wall thickness {min_thickness:.2f}mm below minimum "
                f"(0.5mm) - will cause short shots."
            )
        elif min_thickness > 6.0:
            warnings.append({
                'category': 'Wall Thickness',
                'message': f'Thick walls {min_thickness:.2f}mm will cause sink marks',
                'recommendation': 'Reduce to 3-4mm or core out with ribs',
                'rationale': (
                    'Thick walls cool unevenly, causing sink marks, voids, '
                    'and warpage. Cycle time ∝ thickness². Core out thick '
                    'sections, add ribs for support. Max recommended: 4mm.'
                ),
            })
            rationale.append(
                f"⚠️ Wall {min_thickness:.2f}mm causes sink marks. Core out "
                f"thick sections."
            )
        else:
            passed.append({
                'check': 'Wall Thickness',
                'status': f'{min_thickness:.2f}mm - Optimal',
            })
            rationale.append(
                f"✓ Wall thickness {min_thickness:.2f}mm optimal (0.75-4mm "
                f"range)."
            )

    # ----- RULE 2: Draft angles -----------------------------------------
    warnings.append({
        'category': 'Draft Angles',
        'message': 'Add 1-3° draft to vertical walls',
        'recommendation': '1° minimum, 2-3° for textured surfaces',
        'rationale': (
            'Draft allows easy ejection. Without draft, parts stick in mold. '
            'Each 1° reduces ejection force 5-10%. Textured surfaces need '
            '1° per 0.025mm texture depth.'
        ),
    })
    rationale.append("⚠️ Add 1-3° draft angles to all walls parallel to mold opening.")

    # ----- RULE 3: Rib design (60% of wall thickness) -------------------
    if min_thickness > 0:
        rib_thickness = min_thickness * 0.6
        max_rib_height = min_thickness * 3
        suggestions.append({
            'opportunity': f'Design ribs at {rib_thickness:.2f}mm (60% of wall)',
            'savings': 'Prevents sink marks while maintaining strength',
            'difficulty': 'Easy',
            'rationale': (
                f'Ribs = 50-60% of wall to avoid sink marks. For '
                f'{min_thickness:.2f}mm walls: rib = {rib_thickness:.2f}mm, '
                f'max height = {max_rib_height:.1f}mm (3× wall). Add 0.5-1° '
                f'draft.'
            ),
        })

    # ----- RULE 4: Corner radii (0.5× wall thickness minimum) -----------
    if min_thickness > 0:
        min_radius = min_thickness * 0.5
        warnings.append({
            'category': 'Corner Radii',
            'message': f'Add {min_radius:.2f}mm minimum inside radius',
            'recommendation': f'Inside radius ≥{min_radius:.2f}mm (0.5× wall)',
            'rationale': (
                f'Sharp corners create stress concentrations and mold wear. '
                f'Min inside radius = 0.5× wall ({min_radius:.2f}mm). '
                f'Outside = inside + wall thickness.'
            ),
        })
        rationale.append(
            f"⚠️ Add {min_radius:.2f}mm minimum radius to all corners."
        )

    # ----- RULE 5: Undercuts --------------------------------------------
    suggestions.append({
        'opportunity': 'Eliminate undercuts to avoid side actions',
        'savings': '$5,000-$15,000 per side action eliminated',
        'difficulty': 'Medium',
        'rationale': (
            'Undercuts require slides/lifters ($5K-15K each, +2-5s cycle '
            'time). Alternatives: split part, redesign for straight pull, '
            'use bumpoffs (<0.5mm), hand-load inserts.'
        ),
    })

    # ----- RULE 6: Material-specific ------------------------------------
    if 'abs' in material.lower():
        passed.append({'check': 'Material', 'status': 'ABS - Excellent'})
        rationale.append(
            "✓ ABS: excellent flow, impact strength, surface finish. "
            "Shrinkage 0.5-0.7%."
        )
    elif 'polycarbonate' in material.lower() or 'pc' in material.lower():
        warnings.append({
            'category': 'Material',
            'message': 'PC requires high mold temps and drying',
            'recommendation': 'Mold temp 80-100°C, dry 4hrs at 120°C',
            'rationale': (
                'PC needs high mold temps (vs 50-80°C for ABS), +20-30% '
                'cycle time. Must dry or will have bubbles. Melt: 280-320°C.'
            ),
        })
        rationale.append(
            "⚠️ PC requires high mold temps (80-100°C) and pre-drying - "
            "longer cycles."
        )
    elif 'polypropylene' in material.lower() or 'pp' in material.lower():
        passed.append({'check': 'Material', 'status': 'PP - Excellent flow'})
        warnings.append({
            'category': 'Shrinkage',
            'message': 'PP has high shrinkage (1.5-2.5%)',
            'recommendation': 'Use glass-filled PP for tight tolerances',
            'rationale': (
                'PP shrinks 1.5-2.5% (vs 0.5-0.7% ABS). Glass-filled '
                '(20-30%) reduces to 0.5-1.0%.'
            ),
        })
        rationale.append(
            "✓ PP: excellent flow, low cost. ⚠️ High shrinkage 1.5-2.5%."
        )

    # ----- RULE 7: Tolerances -------------------------------------------
    suggestions.append({
        'opportunity': 'Use standard injection molding tolerances (±0.1mm)',
        'savings': '20-30% vs tight machined tolerances',
        'difficulty': 'Easy',
        'rationale': (
            'Standard injection molding tolerance: ±0.1mm for dimensions '
            '<100mm, ±0.2% for larger. Tight tolerances require slower '
            'cycles, conditioned tooling, or secondary machining.'
        ),
    })

    # ----- Score and summary --------------------------------------------
    total_checks = len(issues) + len(warnings) + len(passed)
    if total_checks > 0:
        score = (len(passed) * 100 + len(warnings) * 50) / total_checks
    else:
        score = 85.0

    summary = (
        "**Overall Assessment:** "
        f"{'GOOD - Suitable for injection molding' if score >= 75 else 'NEEDS REVIEW'}\n"
        f"**Score:** {score:.1f}/100\n"
        f"**Key Findings:** Wall {min_thickness:.2f}mm "
        f"{'optimal' if 0.75 <= min_thickness <= 4.0 else 'review'}, "
        "add 1-3° draft, ribs at 60% wall, eliminate undercuts\n"
        "**Recommendation:** "
        f"{'Manufacturable. Address warnings for optimization.' if len(issues) == 0 else 'Fix wall thickness issues before tooling.'}"
    )

    return {
        'success': True,
        'process': 'Injection Molding',
        'material': material,
        'score': round(score, 1),
        'score_explanation': (
            f"Based on {len(passed)} passed, {len(warnings)} warnings, "
            f"{len(issues)} issues"
        ),
        'issues': len(issues),
        'warnings': len(warnings),
        'suggestions': len(suggestions),
        'passed': len(passed),
        'geometry_info': {
            'dimensions': (
                f"{dims.get('x', 0):.1f} x {dims.get('y', 0):.1f} x "
                f"{dims.get('z', 0):.1f} mm"
            ),
            'volume': f"{volume:.2f} mm³",
            'min_thickness': (
                f"{min_thickness:.2f} mm" if min_thickness > 0 else 'N/A'
            ),
        },
        'rationale': rationale,
        'summary': summary,
        'details': {
            'critical_issues': issues[:5],
            'warnings': warnings[:5],
            'cost_savings': suggestions[:3],
        },
    }


# ---------------------------------------------------------------------------
# Die casting
# ---------------------------------------------------------------------------
def analyze_die_casting(parser, material, geometry) -> Dict:
    """Analyze for die casting with comprehensive DFM rules."""
    issues = []
    warnings = []
    suggestions = []
    passed = []
    rationale = []

    dims = geometry.get('dimensions', {}) or {}
    volume = geometry.get('volume', 0)
    min_thickness = geometry.get('estimated_min_thickness', 0)

    # ----- RULE 1: Wall thickness (0.75-6mm range) ----------------------
    if min_thickness > 0:
        if min_thickness < 0.75:
            issues.append({
                'category': 'Wall Thickness',
                'message': f'Wall {min_thickness:.2f}mm too thin for die casting',
                'recommendation': 'Increase to 1.0-3.0mm range',
                'rationale': (
                    "Thin walls (<0.75mm) don't fill completely in die "
                    "casting due to rapid solidification. Minimum: 0.75mm "
                    "aluminum, 1.0mm zinc. Molten metal freezes before "
                    "filling thin sections."
                ),
            })
            rationale.append(
                f"❌ Wall {min_thickness:.2f}mm below minimum (0.75mm) - "
                f"incomplete filling."
            )
        elif min_thickness > 6.0:
            warnings.append({
                'category': 'Wall Thickness',
                'message': f'Thick walls {min_thickness:.2f}mm cause porosity',
                'recommendation': 'Reduce to 4-5mm maximum or add cooling channels',
                'rationale': (
                    'Thick sections (>6mm) trap gas porosity and shrinkage '
                    'voids. Die casting works best with thin, uniform walls. '
                    'Maximum: 6mm for most alloys.'
                ),
            })
            rationale.append(
                f"⚠️ Wall {min_thickness:.2f}mm causes porosity. Reduce to "
                f"<6mm."
            )
        else:
            passed.append({
                'check': 'Wall Thickness',
                'status': f'{min_thickness:.2f}mm - Optimal',
            })
            rationale.append(
                f"✓ Wall thickness {min_thickness:.2f}mm is within optimal "
                f"die-casting range (0.75-6mm)."
            )

    # ----- RULE 2: Draft angles -----------------------------------------
    warnings.append({
        'category': 'Draft Angles',
        'message': 'Add 1-3° draft to all walls parallel to die-pull direction',
        'recommendation': '1° minimum on cores, 2-3° on cavity walls',
        'rationale': (
            'Draft is required to release the part from the die without '
            'galling or seizing. Without draft, parts stick and ejection '
            'damages the die.'
        ),
    })
    rationale.append(
        "⚠️ Add 1-3° draft to all walls parallel to die-pull direction."
    )

    # ----- RULE 3: Corner radii -----------------------------------------
    if min_thickness > 0:
        min_radius = max(min_thickness * 0.5, 0.5)
        warnings.append({
            'category': 'Corner Radii',
            'message': f'Add {min_radius:.2f}mm minimum inside radius to corners',
            'recommendation': f'Inside radius ≥{min_radius:.2f}mm',
            'rationale': (
                'Sharp corners cause stress risers in the casting and '
                'accelerate die wear. Minimum inside radius ≈ 0.5× wall '
                'thickness, with 0.5mm absolute floor.'
            ),
        })
        rationale.append(
            f"⚠️ Add {min_radius:.2f}mm minimum radius to all corners."
        )

    # ----- RULE 4: Undercuts --------------------------------------------
    suggestions.append({
        'opportunity': 'Eliminate undercuts to avoid slides',
        'savings': '$10,000-$25,000 per slide eliminated',
        'difficulty': 'Medium',
        'rationale': (
            'Undercuts require slides in die ($10K-25K each). Slides add '
            'complexity, maintenance, and cycle time. Alternatives: '
            'redesign for straight pull, split into assembly, or accept '
            'loose cores (hand-loaded).'
        ),
    })

    # ----- RULE 5: Material-specific (Aluminum vs Zinc) -----------------
    if 'aluminum' in material.lower():
        passed.append({'check': 'Material', 'status': 'Aluminum - Good for die casting'})
        rationale.append(
            "✓ Aluminum: good strength-to-weight, corrosion resistance. "
            "A380 most common. Min wall: 1.0mm."
        )
        suggestions.append({
            'opportunity': 'Use A380 aluminum alloy',
            'savings': 'Best balance of castability and cost',
            'difficulty': 'Easy',
            'rationale': (
                'A380 is standard die cast aluminum: excellent fluidity, '
                'good strength, low cost. A383 for better pressure '
                'tightness. A360 for corrosion resistance. Avoid 6061/7075 '
                '(not die-castable).'
            ),
        })
    elif 'zinc' in material.lower():
        passed.append({'check': 'Material', 'status': 'Zinc - Excellent castability'})
        rationale.append(
            "✓ Zinc: excellent castability, thinnest walls possible "
            "(0.75mm). Zamak 3 most common. Lower strength than aluminum."
        )
        suggestions.append({
            'opportunity': 'Zinc enables thinner walls (0.75mm) and tighter tolerances',
            'savings': '30-40% better dimensional accuracy than aluminum',
            'difficulty': 'Easy',
            'rationale': (
                'Zinc alloys (Zamak 3, 5) offer: thinnest walls (0.75mm vs '
                '1.0mm aluminum), tightest tolerances (±0.05mm vs ±0.1mm), '
                'best surface finish. Lower strength and higher density '
                'than aluminum. Best for small, complex parts.'
            ),
        })

    # ----- RULE 6: Tolerances -------------------------------------------
    suggestions.append({
        'opportunity': 'Use standard die casting tolerances (±0.1mm)',
        'savings': '20-30% vs machined tolerances',
        'difficulty': 'Easy',
        'rationale': (
            'Standard die casting: ±0.1mm for aluminum, ±0.05mm for zinc '
            '(dimensions <50mm). Tighter tolerances require secondary '
            'machining. As-cast finish: Ra 1.6-3.2μm. Only machine '
            'critical features.'
        ),
    })

    # ----- Score and summary --------------------------------------------
    total_checks = len(issues) + len(warnings) + len(passed)
    if total_checks > 0:
        score = (len(passed) * 100 + len(warnings) * 50) / total_checks
    else:
        score = 85.0

    summary = (
        "**Overall Assessment:** "
        f"{'GOOD - Suitable for die casting' if score >= 75 else 'NEEDS REVIEW'}\n"
        f"**Score:** {score:.1f}/100\n"
        f"**Key Findings:** Wall {min_thickness:.2f}mm "
        f"{'optimal' if 1.0 <= min_thickness <= 6.0 else 'review'}, "
        "add 1-3° draft, 0.5mm radii, eliminate undercuts\n"
        "**Recommendation:** "
        f"{'Manufacturable with die casting.' if len(issues) == 0 else 'Fix wall thickness before tooling.'}"
    )

    return {
        'success': True,
        'process': 'Die Casting',
        'material': material,
        'score': round(score, 1),
        'score_explanation': (
            f"Based on {len(passed)} passed, {len(warnings)} warnings, "
            f"{len(issues)} issues"
        ),
        'issues': len(issues),
        'warnings': len(warnings),
        'suggestions': len(suggestions),
        'passed': len(passed),
        'geometry_info': {
            'dimensions': (
                f"{dims.get('x', 0):.1f} x {dims.get('y', 0):.1f} x "
                f"{dims.get('z', 0):.1f} mm"
            ),
            'volume': f"{volume:.2f} mm³",
            'min_thickness': (
                f"{min_thickness:.2f} mm" if min_thickness > 0 else 'N/A'
            ),
        },
        'rationale': rationale,
        'summary': summary,
        'details': {
            'critical_issues': issues[:5],
            'warnings': warnings[:5],
            'cost_savings': suggestions[:3],
        },
    }


# ---------------------------------------------------------------------------
# Wire forming
# ---------------------------------------------------------------------------
def analyze_wire_forming(parser, material, geometry) -> Dict:
    """Analyze for wire forming with comprehensive DFM rules."""
    issues = []
    warnings = []
    suggestions = []
    passed = []
    rationale = []

    dims = geometry.get('dimensions', {}) or {}
    min_dim = min(dims.values()) if dims else 0
    volume = geometry.get('volume', 0)

    # ----- RULE 1: Wire diameter (0.5-12mm typical range) ---------------
    if min_dim > 0:
        if min_dim < 0.5:
            issues.append({
                'category': 'Wire Diameter',
                'message': f'Wire diameter {min_dim:.2f}mm too thin',
                'recommendation': 'Increase to minimum 0.5mm for reliable forming',
                'rationale': (
                    'Wire below 0.5mm is fragile and breaks during bending. '
                    'Difficult to handle and feed. Minimum practical: 0.5mm '
                    'for simple bends, 1.0mm for complex forms.'
                ),
            })
            rationale.append(
                f"❌ Wire diameter {min_dim:.2f}mm too thin - will break "
                f"during forming."
            )
        elif min_dim < 1.0:
            warnings.append({
                'category': 'Wire Diameter',
                'message': f'Thin wire {min_dim:.2f}mm requires careful handling',
                'recommendation': 'Consider 1.0mm+ for better formability',
                'rationale': (
                    'Thin wire (0.5-1.0mm) is delicate and prone to '
                    'kinking. Requires precise tooling and slower feed '
                    'rates. Standard range: 1.0-6.0mm for most '
                    'applications.'
                ),
            })
            rationale.append(
                f"⚠️ Wire {min_dim:.2f}mm is thin - requires careful forming."
            )
        elif min_dim > 12.0:
            warnings.append({
                'category': 'Wire Diameter',
                'message': f'Thick wire {min_dim:.2f}mm requires high forming force',
                'recommendation': 'Consider bar stock or machining for diameters >12mm',
                'rationale': (
                    'Wire over 12mm requires heavy-duty forming equipment '
                    'and high forces. May be more economical to machine '
                    'from bar stock. Maximum practical wire diameter: 12mm '
                    'for most CNC wire benders.'
                ),
            })
            rationale.append(
                f"⚠️ Wire {min_dim:.2f}mm requires heavy-duty equipment."
            )
        else:
            passed.append({
                'check': 'Wire Diameter',
                'status': f'{min_dim:.2f}mm - Good range',
            })
            rationale.append(
                f"✓ Wire diameter {min_dim:.2f}mm is within standard "
                f"forming range (1-12mm)."
            )

    # ----- RULE 2: Bend radius (minimum 3× wire diameter) ---------------
    if min_dim > 0:
        min_bend_radius = min_dim * 3
        recommended_radius = min_dim * 4
        warnings.append({
            'category': 'Bend Radius',
            'message': (
                f'Minimum bend radius: {min_bend_radius:.2f}mm (3× diameter)'
            ),
            'recommendation': (
                f'Use {recommended_radius:.2f}mm radius (4× diameter) for '
                f'best results'
            ),
            'rationale': (
                f'Bend radius must be ≥3× wire diameter to avoid cracking '
                f'and work-hardening. For {min_dim:.2f}mm wire: minimum = '
                f'{min_bend_radius:.2f}mm, recommended = '
                f'{recommended_radius:.2f}mm. Tighter bends cause material '
                f'failure. Spring steels need 5-6× diameter.'
            ),
        })
        rationale.append(
            f"⚠️ Minimum bend radius: {min_bend_radius:.2f}mm (3× wire "
            f"diameter rule)."
        )

    # ----- RULE 3: Minimum leg length (3× wire diameter) ----------------
    if min_dim > 0:
        min_leg_length = min_dim * 3
        warnings.append({
            'category': 'Leg Length',
            'message': f'Minimum straight leg length: {min_leg_length:.2f}mm',
            'recommendation': (
                f'Maintain ≥{min_leg_length:.2f}mm (3× diameter) between '
                f'bends'
            ),
            'rationale': (
                f'Short legs between bends are difficult to grip and form '
                f'accurately. Minimum leg length = 3× wire diameter. For '
                f'{min_dim:.2f}mm wire: {min_leg_length:.2f}mm minimum. '
                f'Shorter legs require special tooling.'
            ),
        })
        rationale.append(
            f"⚠️ Maintain ≥{min_leg_length:.2f}mm leg length between bends."
        )

    # ----- RULE 4: Springback compensation ------------------------------
    suggestions.append({
        'opportunity': 'Account for springback in bend angles',
        'savings': 'Prevents rework and ensures dimensional accuracy',
        'difficulty': 'Medium',
        'rationale': (
            'Wire springs back 2-10° after bending depending on material '
            'and diameter. Steel: 4-8° springback. Stainless: 6-10°. '
            'Aluminum: 2-4°. CNC wire benders compensate automatically, '
            'but manual forming requires overbending. Thicker wire = more '
            'springback.'
        ),
    })
    rationale.append(
        "Account for 2-10° springback depending on material (steel 4-8°, "
        "stainless 6-10°)."
    )

    # ----- RULE 5: Bend-to-bend distance (4× diameter) ------------------
    if min_dim > 0:
        min_bend_spacing = min_dim * 4
        warnings.append({
            'category': 'Bend Spacing',
            'message': (
                f'Minimum distance between bends: {min_bend_spacing:.2f}mm'
            ),
            'recommendation': (
                f'Space bends ≥{min_bend_spacing:.2f}mm apart (4× diameter)'
            ),
            'rationale': (
                f'Closely spaced bends interfere with tooling and cause '
                f'forming errors. Minimum spacing = 4× wire diameter for '
                f'reliable forming. For {min_dim:.2f}mm wire: '
                f'{min_bend_spacing:.2f}mm minimum between bend tangent '
                f'points.'
            ),
        })
        rationale.append(
            f"⚠️ Space bends ≥{min_bend_spacing:.2f}mm apart (4× diameter)."
        )

    # ----- RULE 6: Material-specific formability ------------------------
    if 'steel' in material.lower():
        if 'stainless' in material.lower():
            warnings.append({
                'category': 'Material Formability',
                'message': 'Stainless steel has poor formability',
                'recommendation': (
                    'Use 304 stainless (better than 316), increase bend '
                    'radii to 4-5× diameter'
                ),
                'rationale': (
                    'Stainless work-hardens during bending, requiring '
                    'larger radii (4-5× diameter vs 3× for mild steel). '
                    '304 is more formable than 316. High springback '
                    '(6-10°). Consider annealing for complex forms.'
                ),
            })
            rationale.append(
                "⚠️ Stainless steel: poor formability, use 4-5× diameter "
                "bend radius."
            )
        else:
            passed.append({'check': 'Material', 'status': 'Steel - Good formability'})
            rationale.append(
                "✓ Mild steel: good formability, 3× diameter bend radius, "
                "moderate springback (4-8°)."
            )
    elif 'aluminum' in material.lower():
        passed.append({'check': 'Material', 'status': 'Aluminum - Excellent formability'})
        rationale.append(
            "✓ Aluminum: excellent formability, 3× diameter bend radius, "
            "low springback (2-4°). Avoid 7075 (brittle)."
        )
    elif 'copper' in material.lower() or 'brass' in material.lower():
        passed.append({'check': 'Material', 'status': 'Copper/Brass - Excellent formability'})
        rationale.append(
            "✓ Copper/brass: excellent formability, 2-3× diameter bend "
            "radius, minimal springback."
        )

    # ----- RULE 7: Tolerance and repeatability --------------------------
    suggestions.append({
        'opportunity': 'Use CNC wire bending for tight tolerances',
        'savings': 'CNC: ±0.5mm vs ±2mm manual bending',
        'difficulty': 'Easy',
        'rationale': (
            'CNC wire benders achieve ±0.5mm positional accuracy and ±1° '
            'angular accuracy. Manual bending: ±2mm position, ±3° angle. '
            'CNC also provides automatic springback compensation and high '
            'repeatability for production runs.'
        ),
    })

    # ----- RULE 8: Complex geometries -----------------------------------
    suggestions.append({
        'opportunity': 'Simplify 3D bends to 2D where possible',
        'savings': '30-50% cost reduction vs 3D forming',
        'difficulty': 'Medium',
        'rationale': (
            '2D bends (all in one plane) are faster and cheaper than 3D '
            'bends. 3D forming requires rotation between bends, adding '
            'cycle time. If 3D bends required, minimize number of plane '
            'changes. Consider welding multiple 2D forms into 3D '
            'assembly.'
        ),
    })

    # ----- Score and summary --------------------------------------------
    total_checks = len(issues) + len(warnings) + len(passed)
    if total_checks > 0:
        score = (len(passed) * 100 + len(warnings) * 50) / total_checks
    else:
        score = 85.0

    summary = (
        "**Overall Assessment:** "
        f"{'GOOD - Suitable for wire forming' if score >= 75 else 'NEEDS REVIEW'}\n"
        f"**Score:** {score:.1f}/100\n"
        f"**Key Findings:** Wire diameter {min_dim:.2f}mm "
        f"{'optimal' if 1.0 <= min_dim <= 12.0 else 'review'}, bend radius "
        "≥3× diameter, leg length ≥3× diameter, account for springback\n"
        "**Recommendation:** "
        f"{'Manufacturable with wire forming.' if len(issues) == 0 else 'Adjust wire diameter before production.'}"
    )

    return {
        'success': True,
        'process': 'Wire Forming',
        'material': material,
        'score': round(score, 1),
        'score_explanation': (
            f"Based on {len(passed)} passed, {len(warnings)} warnings, "
            f"{len(issues)} issues"
        ),
        'issues': len(issues),
        'warnings': len(warnings),
        'suggestions': len(suggestions),
        'passed': len(passed),
        'geometry_info': {
            'dimensions': (
                f"{dims.get('x', 0):.1f} x {dims.get('y', 0):.1f} x "
                f"{dims.get('z', 0):.1f} mm"
            ),
            'volume': f"{volume:.2f} mm³",
            'wire_diameter': (
                f"{min_dim:.2f} mm" if min_dim > 0 else 'N/A'
            ),
        },
        'rationale': rationale,
        'summary': summary,
        'details': {
            'critical_issues': issues[:5],
            'warnings': warnings[:5],
            'cost_savings': suggestions[:3],
        },
    }


# ---------------------------------------------------------------------------
# Out-of-scope analyzer stubs (CR-27652557)
# ---------------------------------------------------------------------------
# These four processes are referenced by app.py's lazy imports inside route
# handlers but are not in scope for the rebuild (per
# .kiro/specs/dfm-analyzer-cr-analyzer-fixes/design.md § 10, step 6). The
# stubs return a graceful "process not yet implemented" payload so the
# request-time imports succeed and the endpoints respond with an explicit
# success=False dict instead of a 500 ImportError.

_NOT_IMPLEMENTED_RATIONALE = (
    "process not yet implemented"
)


def _not_implemented_result(process_label: str, material) -> Dict:
    """Build the standard analyzer dict for a not-yet-implemented process."""
    return {
        'success': False,
        'process': process_label,
        'material': material,
        'score': 0,
        'score_explanation': _NOT_IMPLEMENTED_RATIONALE,
        'issues': 0,
        'warnings': 0,
        'suggestions': 0,
        'passed': 0,
        'geometry_info': {},
        'rationale': [_NOT_IMPLEMENTED_RATIONALE],
        'summary': _NOT_IMPLEMENTED_RATIONALE,
        'details': {},
    }


def analyze_investment_casting(parser, material, geometry) -> Dict:
    """Stub: investment casting analyzer is not yet implemented."""
    return _not_implemented_result('Investment Casting', material)


def analyze_mim(parser, material, geometry) -> Dict:
    """Stub: metal injection molding analyzer is not yet implemented."""
    return _not_implemented_result('Metal Injection Molding (MIM)', material)


def analyze_rotational_molding(parser, material, geometry) -> Dict:
    """Stub: rotational molding analyzer is not yet implemented."""
    return _not_implemented_result('Rotational Molding', material)


def analyze_vacuum_forming(parser, material, geometry) -> Dict:
    """Stub: vacuum forming analyzer is not yet implemented."""
    return _not_implemented_result('Vacuum Forming', material)
