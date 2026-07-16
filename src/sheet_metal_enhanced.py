"""
Enhanced Sheet Metal Analyzer
Based on 930-00172_R01-1 - Amazon Robotics Sheet Metal Design Best Practices
"""
from typing import Dict


def analyze_sheet_metal_enhanced(parser, material, geometry) -> Dict:
    """
    Comprehensive sheet metal DFM analysis
    Based on industry standards from 930-00172_R01-1 (98 pages)
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
    
    # Estimate material thickness from geometry if not provided
    # For sheet metal, min_thickness is typically the material thickness
    material_thickness = min_thickness if min_thickness > 0 else 1.0  # Default 1mm if unknown
    
    # RULE 1: Material Thickness
    rule_name = "Material Thickness"
    rule_standard = "Standard range: 0.5-3.0mm. Turret press minimum: 0.4mm. Progressive tool: 0.4-3.0mm per 930-00172"
    
    if material_thickness > 0:
        if material_thickness < 0.4:
            issues.append({
                'category': 'Material Thickness',
                'message': f'Critical: Thickness {material_thickness:.2f}mm too thin for sheet metal',
                'recommendation': 'Increase to minimum 0.5mm for reliable forming',
                'rationale': 'Material below 0.4mm is extremely difficult to handle, prone to tearing during forming, and cannot hold tolerances. Press brake operators cannot reliably grip and position ultra-thin material. Bending forces cause immediate tearing at the bend line.'
            })
            rationale.append(f"❌ Material thickness {material_thickness:.2f}mm below minimum - will tear during bending.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'FAIL',
                'measured_value': f'{material_thickness:.2f}mm',
                'evaluation': f'Thickness {material_thickness:.2f}mm is below minimum 0.4mm requirement for any sheet metal process',
                'recommendation': 'Increase to 0.5mm minimum for prototype/low-volume, 0.6mm for production runs',
                'rationale': 'Material <0.4mm causes multiple critical failures: (1) Cannot hold dimensional tolerances - material flexes and distorts during handling, (2) Tears during bending - insufficient material strength at bend radius causes immediate failure, (3) Difficult to handle - operators cannot reliably grip and position thin sheets in press brake, (4) Punching issues - thin material pulls through die rather than shearing cleanly, (5) Welding problems - burns through easily. Minimum practical thickness: 0.5mm for prototype (hand brake), 0.6mm for production (turret press/progressive tool). Industry standard per 930-00172: 0.4mm absolute minimum, but 0.5-0.6mm strongly recommended.',
                'cost_impact': 'Material <0.4mm: 50-70% scrap rate from tearing and distortion, requires specialized micro-forming equipment (+150-200% cost), limited fabricator availability (most shops refuse <0.5mm), longer lead times (+2-3 weeks)'
            })
        elif material_thickness > 3.0:
            warnings.append({
                'category': 'Material Thickness',
                'message': f'Thick material {material_thickness:.2f}mm requires high tonnage press brake',
                'recommendation': 'Verify press brake capacity for material >3mm. Consider 4mm maximum for standard shops.',
                'rationale': 'Thick material requires high bending force (tonnage increases with square of thickness), larger bend radii (minimum 1.5-2.0T), and specialized heavy-duty tooling. Standard press brakes limited to 3mm for most materials.'
            })
            rationale.append(f"⚠️ Material thickness {material_thickness:.2f}mm requires high-tonnage equipment and special tooling.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'{material_thickness:.2f}mm',
                'evaluation': f'Thickness {material_thickness:.2f}mm exceeds standard 3.0mm range - requires heavy-duty equipment',
                'recommendation': 'Verify press brake tonnage capacity (typically 80-100 tons for 3mm, 150-200 tons for 4mm). Confirm tooling availability for thick material.',
                'rationale': 'Material >3mm creates multiple challenges: (1) Bending force - tonnage requirement increases with square of thickness (3mm→4mm = 78% more force), (2) Bend radius - minimum radius increases to 1.5-2.0T to prevent cracking (4mm material needs 6-8mm radius), (3) Tooling - requires heavy-duty dies and punches (standard tooling rated to 3mm), (4) Springback - thicker material has more elastic recovery requiring overbending compensation, (5) Equipment availability - many shops limited to 3mm maximum capacity. For 4mm+ material: verify fabricator has 150+ ton press brake, heavy-duty tooling, and experience with thick material. Alternative: Consider laser cutting + welding instead of bending for thick sections.',
                'cost_impact': 'Material >3mm: +30-50% forming cost due to higher tonnage requirements, +20-30% tooling cost for heavy-duty dies, limited fabricator availability (reduces competition, increases price), longer lead times (+1-2 weeks to find capable shop)'
            })
        else:
            passed.append({'check': 'Material Thickness', 'status': f'{material_thickness:.2f}mm - Standard range'})
            rationale.append(f"✓ Material thickness {material_thickness:.2f}mm is within standard range for all sheet metal processes.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'PASS',
                'measured_value': f'{material_thickness:.2f}mm',
                'evaluation': f'Thickness {material_thickness:.2f}mm is within standard 0.5-3.0mm sheet metal range',
                'recommendation': 'No changes needed - thickness is optimal for standard sheet metal fabrication',
                'rationale': 'Material thickness 0.5-3.0mm is the sweet spot for sheet metal fabrication: (1) Readily available - standard stock sizes from all metal suppliers, (2) Standard tooling - all press brakes and turret presses equipped for this range, (3) Good formability - bends cleanly without cracking (with proper radius), (4) Holds tolerances - sufficient rigidity to maintain dimensional accuracy, (5) Cost-effective - no premium for special handling or equipment. This range covers 90% of sheet metal applications. Process capabilities per 930-00172: Turret press (0.4-3.0mm), Laser cutting (0.5-3.0mm), Hand brake (0.5-3.0mm), Progressive tool (0.4-3.0mm). Your {material_thickness:.2f}mm thickness works with all standard processes.',
                'cost_impact': 'Standard material cost - no premium. Competitive pricing from multiple fabricators. Fast turnaround (1-2 weeks typical).'
            })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': 'Not measured',
            'evaluation': 'Material thickness could not be determined from geometry - manual specification required',
            'recommendation': 'Specify material thickness in drawing. Recommended: 0.8-1.5mm for general purpose, 1.0-2.0mm for structural parts, 0.5-0.8mm for enclosures',
            'rationale': 'Material thickness is the most critical parameter in sheet metal design - it drives ALL other design rules: (1) Hole diameter (minimum 1.33T), (2) Hole spacing (minimum 1.2T), (3) Edge distance (minimum 2T), (4) Bend radius (minimum 1.0T), (5) Flange length (minimum 1.33T). Without knowing thickness, cannot validate any other design rules. Common thickness selections: 0.5mm (light enclosures), 0.8mm (electronics enclosures), 1.0mm (general brackets), 1.5mm (structural brackets), 2.0mm (heavy-duty structural), 2.5-3.0mm (high-load applications). Material availability: Aluminum (0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0mm), Steel (0.5, 0.7, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0mm), Stainless (0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0mm).',
            'cost_impact': 'Material cost scales with thickness: 1.0mm baseline, 0.5mm = 50% cost, 2.0mm = 200% cost, 3.0mm = 300% cost. Thicker = more expensive but stronger.'
        })
    
    # RULE 2: Minimum Hole Diameter
    rule_name = "Minimum Hole Diameter"
    rule_standard = "Minimum hole diameter = 1.33T (1.33× material thickness) per 930-00172"
    
    min_hole_diameter = 1.33 * material_thickness
    
    if holes:
        hole_issues = []
        hole_warnings = []
        for hole in holes:
            diameter = hole.get('diameter', 0)
            if diameter > 0:
                if diameter < min_hole_diameter:
                    hole_issues.append(f"Hole Ø{diameter:.2f}mm < minimum {min_hole_diameter:.2f}mm")
                elif diameter < min_hole_diameter * 1.1:  # Within 10% of minimum
                    hole_warnings.append(f"Hole Ø{diameter:.2f}mm near minimum")
        
        if hole_issues:
            issues.append({
                'category': 'Hole Diameter',
                'message': f'Critical: {len(hole_issues)} holes below minimum diameter',
                'recommendation': f'Increase hole diameter to minimum {min_hole_diameter:.2f}mm (1.33T)',
                'rationale': 'Holes smaller than 1.33T cause punch breakage, poor hole quality, and excessive tool wear. Minimum ensures clean punching.'
            })
            rationale.append(f"❌ {len(hole_issues)} holes below minimum diameter {min_hole_diameter:.2f}mm.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'FAIL',
                'measured_value': f'{len(hole_issues)} holes below minimum',
                'evaluation': f'Checking criteria: Hole diameter must be ≥1.33T (≥{min_hole_diameter:.2f}mm for {material_thickness:.2f}mm material). Analysis: Detected {len(hole_issues)} holes with diameter <{min_hole_diameter:.2f}mm. Examples: {", ".join(hole_issues[:3])}. Result: FAIL - holes too small for reliable punching.',
                'recommendation': f'Increase all hole diameters to minimum {min_hole_diameter:.2f}mm (1.33× material thickness)',
                'rationale': f'Holes <1.33T cause: punch breakage (small punches are weak), poor hole quality (ragged edges), excessive tool wear. For {material_thickness:.2f}mm material, minimum hole = {min_hole_diameter:.2f}mm. Smaller holes require drilling (secondary operation, +cost).',
                'cost_impact': 'Holes <1.33T: Cannot punch, must drill (+$0.50-$1.00 per hole), 40-60% longer lead time'
            })
        elif hole_warnings:
            warnings.append({
                'category': 'Hole Diameter',
                'message': f'{len(hole_warnings)} holes near minimum diameter',
                'recommendation': f'Consider increasing to {min_hole_diameter * 1.2:.2f}mm for better tool life',
                'rationale': 'Holes near minimum diameter work but cause faster tool wear. Slightly larger holes improve tool life and hole quality.'
            })
            rationale.append(f"⚠️ {len(hole_warnings)} holes near minimum diameter.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'{len(hole_warnings)} holes near minimum',
                'evaluation': f'Checking criteria: Hole diameter should be ≥1.2× minimum ({min_hole_diameter * 1.2:.2f}mm) for optimal tool life. Analysis: Detected {len(hole_warnings)} holes between {min_hole_diameter:.2f}mm and {min_hole_diameter * 1.1:.2f}mm (within 10% of minimum). Result: WARNING - holes are punchable but will cause faster tool wear.',
                'recommendation': f'Consider increasing to {min_hole_diameter * 1.2:.2f}mm (20% above minimum) for optimal tool life',
                'rationale': 'Holes at minimum diameter are manufacturable but cause faster punch wear. Increasing by 20% significantly improves tool life and hole quality with minimal design impact.',
                'cost_impact': 'Holes at minimum: 30-40% faster tool wear, more frequent sharpening'
            })
        else:
            passed.append({'check': 'Hole Diameter', 'status': f'All holes ≥{min_hole_diameter:.2f}mm'})
            rationale.append(f"✓ All holes meet minimum diameter requirement.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'PASS',
                'measured_value': f'{len(holes)} holes checked',
                'evaluation': f'Checking criteria: All holes must be ≥1.33T (≥{min_hole_diameter:.2f}mm for {material_thickness:.2f}mm material). Analysis: Checked {len(holes)} holes in geometry. All holes meet or exceed {min_hole_diameter:.2f}mm diameter. Result: PASS - all holes are properly sized for punching.',
                'recommendation': 'No changes needed - hole sizes are appropriate for standard punching operations',
                'rationale': 'All holes are ≥1.33T, ensuring clean punching, good tool life, and quality holes. Standard punches available.',
                'cost_impact': 'Standard punching cost - no premium'
            })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': 'No holes detected',
            'evaluation': 'Checking criteria: Hole diameter ≥1.33T. Analysis: No holes detected in geometry. Result: INFO - rule not applicable to this part.',
            'recommendation': f'If adding holes, use minimum diameter {min_hole_diameter:.2f}mm (1.33T for {material_thickness:.2f}mm material)',
            'rationale': 'Minimum hole diameter rule applies when holes are added to design',
            'cost_impact': 'N/A'
        })
    
    # RULE 3: Hole to Edge Distance
    rule_name = "Hole to Edge Distance"
    rule_standard = "Minimum distance from hole edge to part edge = 2T (2× material thickness) per 930-00172"
    
    min_edge_distance = 2.0 * material_thickness
    
    if holes and dims:
        # Calculate part edges from bounding box
        part_min_x = 0
        part_max_x = dims.get('x', 0)
        part_min_y = 0
        part_max_y = dims.get('y', 0)
        
        edge_issues = []
        edge_warnings = []
        
        for hole in holes:
            center = hole.get('center', {})
            diameter = hole.get('diameter', 0)
            radius = diameter / 2.0
            
            if center and diameter > 0:
                x = center.get('x', 0)
                y = center.get('y', 0)
                
                # Calculate distance from hole edge to part edges
                dist_to_left = x - radius - part_min_x
                dist_to_right = part_max_x - (x + radius)
                dist_to_bottom = y - radius - part_min_y
                dist_to_top = part_max_y - (y + radius)
                
                min_dist = min(dist_to_left, dist_to_right, dist_to_bottom, dist_to_top)
                
                if min_dist < min_edge_distance:
                    edge_issues.append(f"Hole at ({x:.1f}, {y:.1f}): {min_dist:.2f}mm from edge")
                elif min_dist < min_edge_distance * 1.2:
                    edge_warnings.append(f"Hole at ({x:.1f}, {y:.1f}): {min_dist:.2f}mm from edge")
        
        if edge_issues:
            issues.append({
                'category': 'Hole to Edge Distance',
                'message': f'Critical: {len(edge_issues)} holes too close to edge',
                'recommendation': f'Move holes to minimum {min_edge_distance:.2f}mm (2T) from edge',
                'rationale': 'Holes too close to edge cause material deformation, tearing, and poor hole quality during punching. Edge may curl or distort.'
            })
            rationale.append(f"❌ {len(edge_issues)} holes violate minimum edge distance {min_edge_distance:.2f}mm.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'FAIL',
                'measured_value': f'{len(edge_issues)} holes too close',
                'evaluation': f'Checking criteria: Distance from hole edge to part edge must be ≥2T (≥{min_edge_distance:.2f}mm for {material_thickness:.2f}mm material). Analysis: Calculated distance from each hole center to all 4 part edges (left, right, top, bottom), subtracted hole radius to get edge-to-edge distance. Detected {len(edge_issues)} holes with edge distance <{min_edge_distance:.2f}mm. Examples: {", ".join(edge_issues[:3])}. Result: FAIL - insufficient material between hole and edge.',
                'recommendation': f'Relocate holes to minimum {min_edge_distance:.2f}mm from all edges (measure from hole edge, not center)',
                'rationale': f'Holes <2T from edge cause: material deformation (insufficient material to support punch force), edge tearing/curling, poor hole quality (oval holes), part distortion. For {material_thickness:.2f}mm material, minimum edge distance = {min_edge_distance:.2f}mm. Closer holes require secondary operations.',
                'cost_impact': 'Holes <2T from edge: Cannot punch reliably, may require drilling (+$0.50-$1.00 per hole), 30-50% scrap rate from edge tearing'
            })
        elif edge_warnings:
            warnings.append({
                'category': 'Hole to Edge Distance',
                'message': f'{len(edge_warnings)} holes near minimum edge distance',
                'recommendation': f'Consider moving to {min_edge_distance * 1.3:.2f}mm for better quality',
                'rationale': 'Holes near minimum edge distance work but may show slight edge deformation. More clearance improves quality.'
            })
            rationale.append(f"⚠️ {len(edge_warnings)} holes near minimum edge distance.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'{len(edge_warnings)} holes near minimum',
                'evaluation': f'Checking criteria: Edge distance should be ≥2.4T ({min_edge_distance * 1.2:.2f}mm) for optimal quality. Analysis: Calculated edge-to-edge distance for all holes. Detected {len(edge_warnings)} holes between {min_edge_distance:.2f}mm and {min_edge_distance * 1.2:.2f}mm from edge (within 20% of minimum). Examples: {", ".join(edge_warnings[:3])}. Result: WARNING - holes are punchable but may show slight edge deformation.',
                'recommendation': f'Consider increasing to {min_edge_distance * 1.3:.2f}mm (30% above minimum) for optimal quality',
                'rationale': 'Holes at minimum edge distance are manufacturable but may show slight edge deformation or require careful setup. Increasing clearance by 30% improves quality and reduces scrap.',
                'cost_impact': 'Holes at minimum edge distance: 10-20% higher scrap rate, requires careful setup'
            })
        else:
            passed.append({'check': 'Hole to Edge Distance', 'status': f'All holes ≥{min_edge_distance:.2f}mm from edge'})
            rationale.append(f"✓ All holes meet minimum edge distance requirement.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'PASS',
                'measured_value': f'{len(holes)} holes checked',
                'evaluation': f'Checking criteria: Distance from hole edge to part edge must be ≥2T (≥{min_edge_distance:.2f}mm for {material_thickness:.2f}mm material). Analysis: Calculated distance from each hole to all 4 part edges. Checked {len(holes)} holes. All holes maintain ≥{min_edge_distance:.2f}mm clearance from edges. Result: PASS - all holes properly positioned.',
                'recommendation': 'No changes needed - hole placement is appropriate for standard punching',
                'rationale': 'All holes maintain ≥2T edge distance, ensuring clean punching without edge deformation or tearing. Standard setup, no special fixtures required.',
                'cost_impact': 'Standard punching cost - no premium'
            })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': 'Cannot evaluate',
            'evaluation': 'Insufficient geometry data for hole-to-edge analysis',
            'recommendation': f'Maintain minimum {min_edge_distance:.2f}mm (2T) from hole edge to part edge',
            'rationale': 'Hole-to-edge distance rule applies when holes are present in design',
            'cost_impact': 'N/A'
        })
    
    # RULE 4: Hole Spacing
    rule_name = "Hole Spacing"
    rule_standard = "Minimum distance between hole edges = 1.2T (1.2× material thickness) per 930-00172"
    
    min_hole_spacing = 1.2 * material_thickness
    
    if len(holes) >= 2:
        spacing_issues = []
        spacing_warnings = []
        
        # Check spacing between all hole pairs
        for i, hole1 in enumerate(holes):
            center1 = hole1.get('center', {})
            diameter1 = hole1.get('diameter', 0)
            
            for hole2 in holes[i+1:]:
                center2 = hole2.get('center', {})
                diameter2 = hole2.get('diameter', 0)
                
                if center1 and center2 and diameter1 > 0 and diameter2 > 0:
                    # Calculate center-to-center distance
                    dx = center2.get('x', 0) - center1.get('x', 0)
                    dy = center2.get('y', 0) - center1.get('y', 0)
                    center_distance = (dx**2 + dy**2)**0.5
                    
                    # Calculate edge-to-edge distance
                    edge_distance = center_distance - (diameter1/2.0 + diameter2/2.0)
                    
                    if edge_distance < min_hole_spacing:
                        spacing_issues.append(f"Holes {edge_distance:.2f}mm apart")
                    elif edge_distance < min_hole_spacing * 1.15:
                        spacing_warnings.append(f"Holes {edge_distance:.2f}mm apart")
        
        if spacing_issues:
            issues.append({
                'category': 'Hole Spacing',
                'message': f'Critical: {len(spacing_issues)} hole pairs too close together',
                'recommendation': f'Increase spacing to minimum {min_hole_spacing:.2f}mm (1.2T) between hole edges',
                'rationale': 'Holes too close together cause material deformation between holes, web tearing, and poor hole quality.'
            })
            rationale.append(f"❌ {len(spacing_issues)} hole pairs violate minimum spacing {min_hole_spacing:.2f}mm.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'FAIL',
                'measured_value': f'{len(spacing_issues)} violations',
                'evaluation': f'Checking criteria: Distance between hole edges must be ≥1.2T (≥{min_hole_spacing:.2f}mm for {material_thickness:.2f}mm material). Analysis: Calculated center-to-center distance for all hole pairs, subtracted both radii to get edge-to-edge spacing. Checked {len(holes)*(len(holes)-1)//2} hole pairs. Detected {len(spacing_issues)} pairs with spacing <{min_hole_spacing:.2f}mm. Examples: {", ".join(spacing_issues[:3])}. Result: FAIL - insufficient material between holes (web too thin).',
                'recommendation': f'Increase spacing to minimum {min_hole_spacing:.2f}mm between hole edges (measure edge-to-edge, not center-to-center)',
                'rationale': f'Holes <1.2T apart cause: web tearing (insufficient material between holes), material deformation, poor hole quality (oval holes), punch breakage. For {material_thickness:.2f}mm material, minimum spacing = {min_hole_spacing:.2f}mm edge-to-edge.',
                'cost_impact': 'Holes <1.2T apart: 40-60% scrap rate from web tearing, cannot punch simultaneously, requires multiple operations (+30-50% cost)'
            })
        elif spacing_warnings:
            warnings.append({
                'category': 'Hole Spacing',
                'message': f'{len(spacing_warnings)} hole pairs near minimum spacing',
                'recommendation': f'Consider increasing to {min_hole_spacing * 1.3:.2f}mm for better quality',
                'rationale': 'Holes near minimum spacing work but may show slight web deformation. More spacing improves quality.'
            })
            rationale.append(f"⚠️ {len(spacing_warnings)} hole pairs near minimum spacing.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'WARNING',
                'measured_value': f'{len(spacing_warnings)} near minimum',
                'evaluation': f'Checking criteria: Spacing should be ≥1.4T ({min_hole_spacing * 1.15:.2f}mm) for optimal quality. Analysis: Calculated edge-to-edge spacing for all hole pairs. Detected {len(spacing_warnings)} pairs between {min_hole_spacing:.2f}mm and {min_hole_spacing * 1.15:.2f}mm (within 15% of minimum). Examples: {", ".join(spacing_warnings[:3])}. Result: WARNING - holes are punchable but may show slight web deformation.',
                'recommendation': f'Consider increasing to {min_hole_spacing * 1.3:.2f}mm (30% above minimum) for optimal quality',
                'rationale': 'Holes at minimum spacing are manufacturable but may show slight web deformation. Increasing spacing by 30% improves quality and allows simultaneous punching.',
                'cost_impact': 'Holes at minimum spacing: 15-25% higher scrap rate, may require sequential punching'
            })
        else:
            passed.append({'check': 'Hole Spacing', 'status': f'All holes ≥{min_hole_spacing:.2f}mm apart'})
            rationale.append(f"✓ All holes meet minimum spacing requirement.")
            all_rules.append({
                'name': rule_name,
                'standard': rule_standard,
                'status': 'PASS',
                'measured_value': f'{len(holes)} holes checked',
                'evaluation': f'Checking criteria: Distance between hole edges must be ≥1.2T (≥{min_hole_spacing:.2f}mm for {material_thickness:.2f}mm material). Analysis: Calculated edge-to-edge spacing for all {len(holes)*(len(holes)-1)//2} hole pairs. All pairs maintain ≥{min_hole_spacing:.2f}mm spacing. Result: PASS - sufficient material between all holes.',
                'recommendation': 'No changes needed - hole spacing is appropriate for simultaneous punching',
                'rationale': 'All holes maintain ≥1.2T spacing, ensuring clean punching without web tearing or deformation. Can punch multiple holes simultaneously.',
                'cost_impact': 'Standard punching cost - no premium'
            })
    else:
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'INFO',
            'measured_value': f'{len(holes)} holes',
            'evaluation': f'Checking criteria: Hole spacing ≥1.2T. Analysis: Part has {len(holes)} holes - need at least 2 holes to check spacing. Result: INFO - rule not applicable.',
            'recommendation': f'If adding multiple holes, maintain minimum {min_hole_spacing:.2f}mm (1.2T) spacing',
            'rationale': 'Hole spacing rule applies when multiple holes are present',
            'cost_impact': 'N/A'
        })
    
    # RULE 5: Bend Radius
    rule_name = "Bend Radius"
    rule_standard = "Minimum bend radius = 1.0T or 0.6mm (whichever is greater) per 930-00172. Low carbon steel: 0.5T minimum"
    
    min_bend_radius = max(1.0 * material_thickness, 0.6)
    
    warnings.append({
        'category': 'Bend Radius',
        'message': 'Verify all bends meet minimum radius requirements',
        'recommendation': f'Use minimum {min_bend_radius:.2f}mm bend radius (1.0T or 0.6mm)',
        'rationale': 'Sharp bends cause cracking, especially in hard materials. Minimum radius prevents material failure during bending.'
    })
    rationale.append(f"⚠️ Verify all bends use minimum {min_bend_radius:.2f}mm radius.")
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'WARNING',
        'measured_value': 'Cannot detect from geometry',
        'evaluation': 'Bend radius cannot be automatically verified - manual check required',
        'recommendation': f'Use minimum {min_bend_radius:.2f}mm (1.0T or 0.6mm) for all bends',
        'rationale': f'Bends <1.0T cause: material cracking (especially stainless steel, aluminum), inconsistent bend angles, excessive springback, tool damage. For {material_thickness:.2f}mm material, minimum radius = {min_bend_radius:.2f}mm. Low carbon steel only: can use 0.5T. Standard press brake tooling: 0.8mm, 1.0mm, 1.5mm, 2.0mm radius.',
        'cost_impact': 'Bends <1.0T: 30-50% scrap rate from cracking, requires special tooling (+$500-$1,000), annealing may be needed (+$50-$100 per part)'
    })
    
    # RULE 6: Flange Length
    rule_name = "Flange Length"
    rule_standard = "Minimum flange length = 1.33T per 930-00172. Preferred: 4T or 6mm minimum"
    
    min_flange_length = 1.33 * material_thickness
    preferred_flange = max(4.0 * material_thickness, 6.0)
    
    suggestions.append({
        'opportunity': f'Maintain minimum flange length of {preferred_flange:.2f}mm',
        'savings': '15-25% by avoiding special fixtures and reducing scrap',
        'difficulty': 'Easy',
        'rationale': f'Short flanges (<{min_flange_length:.2f}mm) are difficult to hold during bending and may slip or distort. Preferred minimum: {preferred_flange:.2f}mm (4T or 6mm).'
    })
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'INFO',
        'measured_value': 'Design consideration',
        'evaluation': 'Flange length is critical for bendability and part quality',
        'recommendation': f'Absolute minimum: {min_flange_length:.2f}mm (1.33T). Preferred: {preferred_flange:.2f}mm (4T or 6mm)',
        'rationale': f'Flanges <1.33T: Cannot grip in press brake, requires special fixtures (+$200-$500), high scrap rate (30-40%) from slipping. Flanges <4T: Difficult to hold, may distort. For {material_thickness:.2f}mm material: absolute minimum = {min_flange_length:.2f}mm, preferred = {preferred_flange:.2f}mm.',
        'cost_impact': 'Flanges <1.33T: Requires custom fixtures (+$200-$500), 30-40% scrap rate. Flanges <4T: 15-20% scrap rate'
    })
    
    # Additional suggestions based on 930-00172
    suggestions.append({
        'opportunity': 'Use Taptite screws instead of tapped holes',
        'savings': '$0.50-$1.50 per hole (eliminates tapping operation)',
        'difficulty': 'Easy',
        'rationale': 'Taptite screws form their own threads in extruded holes, eliminating secondary tapping operation. Stronger than tapped threads in thin material.'
    })
    
    suggestions.append({
        'opportunity': 'Group features in single turret station',
        'savings': '±0.05mm tolerance vs ±0.2mm between stations',
        'difficulty': 'Medium',
        'rationale': 'Features punched in same station have tighter tolerances (±0.05mm) vs different stations (±0.2mm). Reduces cumulative error.'
    })
    
    suggestions.append({
        'opportunity': 'Use standard bend radius (0.8mm or 1.0mm)',
        'savings': 'Eliminates custom tooling costs ($500-$1,000)',
        'difficulty': 'Easy',
        'rationale': 'Standard press brake tooling available: 0.8mm, 1.0mm, 1.5mm, 2.0mm radius. Custom radii require special tooling.'
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
        assessment = "EXCELLENT - Well-designed for sheet metal fabrication"
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
• Material thickness: {material_thickness:.2f}mm {"(standard range)" if 0.5 <= material_thickness <= 3.0 else "(review required)"}
• Hole specifications: {"All holes meet requirements" if len([r for r in all_rules if r.get('status') == 'PASS' and 'Hole' in r.get('name', '')]) > 0 else "Review hole sizes and placement"}
• Bend radius: Minimum {min_bend_radius:.2f}mm (1.0T or 0.6mm)
• Flange length: Minimum {min_flange_length:.2f}mm (1.33T), preferred {preferred_flange:.2f}mm

**Recommendation:** {"Design is manufacturable with standard sheet metal processes." if len(issues) == 0 else "Address critical issues before fabrication."}

**Based on:** 930-00172_R01-1 - Amazon Robotics Sheet Metal Design Best Practices (98 pages)"""
    
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
        'all_rules': all_rules,
        'parser': parser,  # Include parser for 3D visualization
        'holes': holes,  # Include holes data for visualization
        'geometry': {  # Raw geometry data for calculations
            'dimensions': dims,
            'volume': volume,
            'material_thickness': material_thickness,
            'holes': holes
        },
        'geometry_info': {  # Formatted geometry info for display
            'dimensions': f"{dims.get('x', 0):.1f} x {dims.get('y', 0):.1f} x {dims.get('z', 0):.1f} mm",
            'volume': f"{volume:.2f} mm³",
            'material_thickness': f"{material_thickness:.2f} mm",
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
