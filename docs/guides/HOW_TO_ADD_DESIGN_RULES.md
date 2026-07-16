# How to Add New Design Rules to DFM Inspector

## Overview
Design rules are implemented in Python code, not in .md files. The .md files are just documentation for users.

## File Locations

### Current Implementation:
- **Sheet Metal**: `src/process_analyzers.py` → `analyze_sheet_metal()` function
- **CNC Machining**: `app.py` → `_analyze_cnc_machining()` function  
- **Welding**: `src/welding_inspector.py` → `inspect()` method
- **Other Processes**: `src/process_analyzers.py` → various functions

## Step-by-Step: Adding a New Rule

### Example: Adding "Bend Radius" Rule to Sheet Metal

#### Step 1: Define the Rule
```python
# Add this in src/process_analyzers.py, inside analyze_sheet_metal() function

# RULE 5: Bend Radius (add after existing rules)
rule_name = "Bend Radius"
rule_standard = "Minimum bend radius = 1× thickness (steel), 1.5× thickness (aluminum)"

if min_thickness > 0:
    min_bend_radius = min_thickness * 1.5  # Standard for most materials
    
    # Check if design has appropriate bend radius
    # (In real implementation, you'd detect actual bends from geometry)
    
    warnings.append({
        'category': 'Bend Radius',
        'message': f'Verify bend radius is at least {min_bend_radius:.2f}mm',
        'recommendation': f'Use {min_bend_radius:.2f}mm minimum radius for all bends',
        'rationale': 'Bend radius below 1× thickness causes cracking. Standard: 1.5-2× thickness.'
    })
    
    rationale.append(f"⚠️ Verify bend radii meet minimum {min_bend_radius:.2f}mm (1.5× thickness).")
    
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'WARNING',
        'measured_value': f'Material thickness: {min_thickness:.2f}mm',
        'evaluation': f'For {min_thickness:.2f}mm material, minimum bend radius is {min_bend_radius:.2f}mm',
        'recommendation': f'Ensure all bends have minimum {min_bend_radius:.2f}mm radius',
        'rationale': f'Bend radius below 1× thickness causes material cracking. Standard practice: 1.5-2× thickness provides reliable forming. For {min_thickness:.2f}mm material: {min_bend_radius:.2f}mm minimum.',
        'cost_impact': f'Using {min_bend_radius:.2f}mm radius: standard cost. Tighter radii: +40-60% cost due to specialized tooling'
    })
```

#### Step 2: Update the Score Calculation
The score is automatically calculated from the number of passed/warning/failed checks, so no changes needed.

#### Step 3: Test Your Rule
1. Restart the server: `python app.py`
2. Upload a STEP file
3. Run Sheet Metal analysis
4. Verify the new rule appears in the results

## Rule Structure

Every rule should have these components:

### 1. Issues Array (Critical Failures)
```python
issues.append({
    'category': 'Rule Category',
    'message': 'What is wrong',
    'recommendation': 'How to fix it',
    'rationale': 'Why it matters (technical explanation)'
})
```

### 2. Warnings Array (Non-Critical)
```python
warnings.append({
    'category': 'Rule Category',
    'message': 'What needs attention',
    'recommendation': 'How to optimize',
    'rationale': 'Why it matters'
})
```

### 3. Passed Array (Compliant)
```python
passed.append({
    'check': 'Rule Name',
    'status': 'Description of passing condition'
})
```

### 4. Rationale Array (Summary)
```python
rationale.append("✓ Brief summary of check result")  # Pass
rationale.append("⚠️ Brief summary of warning")      # Warning
rationale.append("❌ Brief summary of failure")      # Fail
```

### 5. All Rules Array (Detailed Breakdown)
```python
all_rules.append({
    'name': 'Rule Name',
    'standard': 'Industry standard or specification',
    'status': 'PASS' | 'FAIL' | 'WARNING' | 'INFO',
    'measured_value': 'Actual measured or estimated value',
    'evaluation': 'Detailed assessment of the measurement',
    'recommendation': 'Specific action to take',
    'rationale': 'Why this rule matters (detailed technical explanation)',
    'cost_impact': 'Financial impact of compliance or non-compliance'
})
```

## Common Rule Types

### 1. Dimension-Based Rules
Check if dimensions meet minimum/maximum requirements:
```python
if min_thickness < 0.5:
    issues.append({...})  # Too thin
elif min_thickness > 6.0:
    warnings.append({...})  # Too thick
else:
    passed.append({...})  # Good
```

### 2. Ratio-Based Rules
Check relationships between dimensions:
```python
depth_ratio = depth / diameter
if depth_ratio > 10:
    issues.append({...})  # Too deep
elif depth_ratio > 4:
    warnings.append({...})  # Challenging
else:
    passed.append({...})  # Good
```

### 3. Material-Based Rules
Check material properties:
```python
if 'aluminum' in material.lower() and '6061' in material:
    warnings.append({...})  # Poor formability
elif 'aluminum' in material.lower() and '5052' in material:
    passed.append({...})  # Excellent formability
```

### 4. Geometry-Based Rules
Check geometric features:
```python
holes = geometry.get('holes', [])
for hole in holes:
    if hole['min_edge_distance'] < min_required:
        issues.append({...})  # Too close to edge
```

## Example: Complete New Rule Implementation

Here's a complete example for "Hole Spacing" in Sheet Metal:

```python
# RULE 6: Hole Spacing
rule_name = "Hole Spacing"
rule_standard = "Minimum spacing = 2× hole diameter, or 3× material thickness, whichever is greater"

holes = geometry.get('holes', [])
if len(holes) >= 2 and min_thickness > 0:
    min_spacing = max(2 * max([h['diameter'] for h in holes]), 3 * min_thickness)
    
    # Check spacing between holes (simplified - would need actual distance calculation)
    spacing_issues = []
    
    # For demonstration, assume we can calculate spacing
    # In real implementation, calculate distance between each pair of holes
    
    if spacing_issues:
        issues.append({
            'category': 'Hole Spacing',
            'message': f'{len(spacing_issues)} hole pairs too close together',
            'recommendation': f'Maintain {min_spacing:.1f}mm minimum spacing between holes',
            'rationale': f'Holes closer than {min_spacing:.1f}mm cause material distortion during punching.'
        })
        
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'FAIL',
            'measured_value': f'{len(spacing_issues)} violations detected',
            'evaluation': f'Some holes are spaced closer than {min_spacing:.1f}mm minimum',
            'recommendation': f'Increase spacing to {min_spacing:.1f}mm minimum',
            'rationale': f'Holes too close together cause material distortion during punching. The web between holes must be strong enough to withstand forming forces. Formula: 2× diameter or 3× thickness. For {min_thickness:.2f}mm material: {min_spacing:.1f}mm minimum.',
            'cost_impact': 'Close hole spacing: 20-30% scrap rate. May require drilling instead of punching (+40% cost per hole)'
        })
    else:
        passed.append({'check': 'Hole Spacing', 'status': 'Adequate spacing'})
        
        all_rules.append({
            'name': rule_name,
            'standard': rule_standard,
            'status': 'PASS',
            'measured_value': f'{len(holes)} holes with adequate spacing',
            'evaluation': 'All holes maintain adequate spacing',
            'recommendation': 'No changes needed',
            'rationale': f'Holes are spaced adequately (minimum {min_spacing:.1f}mm). Can be punched without distortion.',
            'cost_impact': 'Standard punching cost'
        })
else:
    all_rules.append({
        'name': rule_name,
        'standard': rule_standard,
        'status': 'INFO',
        'measured_value': 'Not applicable',
        'evaluation': 'Insufficient holes to check spacing',
        'recommendation': 'N/A',
        'rationale': 'Hole spacing check requires at least 2 holes',
        'cost_impact': 'N/A'
    })
```

## Quick Reference: Rule Status Types

- **PASS** ✓ - Design meets the requirement
- **FAIL** ❌ - Critical issue that will cause manufacturing problems
- **WARNING** ⚠️ - Non-critical issue that increases cost or risk
- **INFO** ℹ️ - Rule cannot be evaluated or is not applicable

## Testing Your New Rules

1. **Add the rule code** to the appropriate analyzer function
2. **Restart the server**: Stop and start `python app.py`
3. **Upload a test file** that should trigger your rule
4. **Verify the output**:
   - Check console logs for any errors
   - Verify rule appears in the web interface
   - Confirm status (PASS/FAIL/WARNING) is correct
   - Check that all fields display properly

## Tips for Writing Good Rules

1. **Be Specific**: Use actual measurements and formulas
2. **Explain Why**: Always include rationale with technical reasoning
3. **Quantify Cost**: Provide specific cost impacts when possible
4. **Use Standards**: Reference industry standards (ISO, ASME, etc.)
5. **Test Thoroughly**: Test with files that pass, fail, and trigger warnings
6. **Handle Edge Cases**: What if geometry data is missing?

## Common Pitfalls to Avoid

1. ❌ **Don't forget to add to all_rules array** - This is what displays in the UI
2. ❌ **Don't use vague messages** - "Hole too close" → "Hole 3.2mm from edge, requires 12.5mm"
3. ❌ **Don't skip rationale** - Users need to understand WHY the rule matters
4. ❌ **Don't forget cost impact** - This helps users prioritize fixes
5. ❌ **Don't assume geometry exists** - Always check if data is available

## Need Help?

If you want to add a specific rule and need help with the implementation, just describe:
1. What you want to check (e.g., "minimum distance between holes")
2. What the requirement is (e.g., "2× hole diameter")
3. What manufacturing process it applies to (e.g., "Sheet Metal")

I can provide the exact code to add!
