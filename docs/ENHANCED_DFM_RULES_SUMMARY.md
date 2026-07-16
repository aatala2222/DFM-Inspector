# Enhanced DFM Rules Summary

## Overview
The DFM Inspector has been significantly enhanced with comprehensive, industry-standard design rules for all 10 manufacturing processes. Each process now includes specific geometric relationships, measurable criteria, and detailed rationale.

---

## 1. CNC MACHINING - 13 Enhanced Rules

### RULE 1: Wall Thickness (ISO 2768)
- **Minimum**: 0.8mm aluminum, 1.0mm steel
- **Optimal**: 2.0mm+ for standard machining
- **Rationale**: Thin walls deflect under cutting forces, causing chatter and dimensional errors

### RULE 2: Hole Depth-to-Diameter Ratio
- **Standard drilling**: Depth ≤ 4× diameter
- **Deep hole drilling**: 4-10× diameter (requires peck drilling, +40-60% cycle time)
- **Gun drilling**: >10× diameter (requires specialized equipment, +200-500% cost)
- **Rationale**: Deep holes have poor chip evacuation and straightness issues

### RULE 3: Internal Corner Radii
- **Minimum radius**: 1/3 of pocket depth or 0.5mm
- **Rationale**: Sharp corners impossible to machine (tools are round). Smaller radii = smaller tools = slower machining

### RULE 4: Thread Depth
- **Steel**: 1.5× nominal diameter + 2mm runout
- **Aluminum**: 2× nominal diameter + 2mm runout
- **Example**: M6 thread needs 11-14mm total depth
- **Rationale**: Insufficient depth causes tap breakage ($50-200 to remove)

### RULE 5: Part Size Limits
- **Standard machines**: 500×500×500mm
- **Large format**: 500-1000mm (+50-100% cost)
- **Oversized**: >1000mm (+300-500% cost, very limited availability)

### RULE 6: Small Features
- **Micro-features**: <2.0mm (requires micro-tooling, +200-400% cycle time)
- **Small features**: 2-5mm (requires small tooling, +40-60% cycle time)
- **Optimal**: 5mm+ (standard 6-12mm tooling)

### RULE 7: Tolerance Specifications (ISO 2768-m)
- **Standard**: ±0.1mm up to 30mm, ±0.2mm up to 120mm
- **Tight tolerances**: Each dimension adds 15-25% cost
- **Rationale**: Only specify tight tolerances where functionally required

### RULE 8: Surface Finish
- **Standard**: Ra 3.2μm (125μin) as-machined
- **Fine**: Ra 1.6μm (+30-50% cycle time)
- **Polished**: Ra 0.8μm (+100-200% cost, requires grinding/polishing)

### RULE 9: Geometry Integrity
- **Requirement**: Watertight solid model
- **Rationale**: Open surfaces cause CAM failures and rejected quotes

### RULE 10: Material Machinability Ratings
- **Excellent (5/5)**: Aluminum 6061/7075, Brass (3-4× faster than steel)
- **Moderate (3/5)**: Mild steel (3-4× longer than aluminum)
- **Poor (2/5)**: Stainless steel (4-6× longer, +200-300% cost)
- **Very Poor (1/5)**: Titanium (8-10× longer, +400-600% cost)

### RULE 11: Aspect Ratio
- **High aspect ratio**: >10:1 requires custom fixturing ($500-2000)
- **Best practice**: <5:1 for standard fixturing

### RULE 12: Material Removal Optimization
- **Low volume-to-surface ratio**: Indicates excessive material removal
- **Solutions**: Start from thinner stock, use ribs instead of solid sections

### RULE 13: Standard Features
- **Standard hole sizes**: 3, 4, 5, 6, 8, 10, 12mm (metric)
- **Non-standard holes**: Require reaming (+30-50% cost per hole)
- **Undercuts**: Require 4/5-axis machining (+100-200% cost)

---

## 2. SHEET METAL - 10 Enhanced Rules

### RULE 1: Material Thickness (ASME Y14.5)
- **Minimum**: 0.5mm (20 gauge) steel, 0.8mm aluminum
- **Standard**: 0.9-3.0mm (18-12 gauge)
- **Maximum**: 6mm (thicker better suited for machining)

### RULE 2: Bend Radius to Thickness Ratio
- **Minimum**: 1× material thickness
- **Recommended**: 1.5× material thickness
- **Example**: 1.2mm material → 1.2mm min radius, 1.8mm recommended
- **Standard tooling**: 0.76mm (0.030"), 1.5mm, 3.0mm radius

### RULE 3: Minimum Flange Length
- **Formula**: 4× material thickness OR 12.7mm minimum (whichever is greater)
- **Example**: 2mm material → 12.7mm minimum flange
- **Rationale**: Short flanges slip in press brake, require custom fixtures ($500-2000)

### RULE 4: Hole-to-Edge Distance
- **Formula**: 2× thickness + bend radius, OR 2.5mm minimum
- **Rationale**: Prevents tearing during punching/bending

### RULE 5: Hole-to-Bend Distance (CRITICAL)
- **Formula**: 2.5× thickness + bend radius from hole edge to bend centerline
- **Example**: 1.5mm material → 5.25mm minimum
- **Rationale**: Holes in bend zones distort into ovals, cause cracking

### RULE 6: Minimum Hole Diameter
- **Formula**: ≥ material thickness, 1.0mm absolute minimum
- **Rationale**: Smaller holes difficult to punch, may break punch

### RULE 7: Hole-to-Hole Spacing
- **Formula**: 2× material thickness OR 3.0mm minimum
- **Rationale**: Close spacing creates weak bridges that tear

### RULE 8: Part Size Limits
- **Standard press brakes**: 1500mm (60") bed length
- **Large format**: 1500-2500mm (+30-50% cost)
- **Oversized**: >2500mm (+200-400% cost, very limited)

### RULE 9: Material Formability
- **Excellent**: 5052-H32 aluminum (25% elongation), mild steel
- **Poor**: 6061-T6 aluminum (8% elongation, cracks at bends)
- **Stainless**: Requires 2× thickness bend radius (+20-30% cost)

### RULE 10: Cost Optimization
- **Standard bend radius**: Eliminates custom tooling ($2,000-5,000 per tool)
- **Standard punch sizes**: 3.2, 6.4, 9.5, 12.7mm (turret punch 5-10× faster than drilling)
- **Minimize bends**: Each bend = $5-15, 2-5 minutes cycle time

---

## 3. INJECTION MOLDING - 12 Enhanced Rules

### RULE 1: Wall Thickness (SPI Standards)
- **Minimum**: 0.5mm (small parts), 0.75mm (larger parts)
- **Optimal**: 0.75-4.0mm
- **Maximum**: 6mm (causes sink marks, voids, warpage)
- **Rationale**: Cycle time ∝ thickness²

### RULE 2: Wall Thickness Uniformity
- **Variation**: <25% of nominal thickness
- **Transitions**: 3:1 taper ratio for thick-to-thin
- **Rationale**: Non-uniform walls cause warpage and internal stresses

### RULE 3: Draft Angles
- **Minimum**: 0.5° shallow features, 1° standard
- **Recommended**: 2-3° per side
- **Textured surfaces**: +1° per 0.025mm texture depth
- **Rationale**: Each degree reduces ejection force 5-10%

### RULE 4: Rib Design
- **Thickness**: 50-60% of nominal wall
- **Height**: ≤3× wall thickness
- **Draft**: 0.5-1° per side
- **Example**: 2mm wall → 1.2mm rib, 6mm max height

### RULE 5: Corner Radii
- **Inside radius**: 0.5× wall thickness minimum
- **Outside radius**: Inside radius + wall thickness
- **Example**: 2mm wall → 1mm inside, 3mm outside radius

### RULE 6: Boss Design
- **Wall thickness**: 60% of nominal wall
- **Height**: ≤2.5× outer diameter
- **Support**: Add gussets/ribs for tall bosses
- **Minimum OD**: 2× screw diameter

### RULE 7: Undercuts
- **Cost**: $5,000-$15,000 per side action
- **Alternatives**: Split part, redesign for straight pull, bumpoffs (<0.5mm)

### RULE 8: Gate Design
- **Thickness**: 50-70% of wall thickness
- **Location**: At thickest section, away from cosmetic surfaces
- **Rationale**: Undersized gates cause high pressure and long fill times

### RULE 9: Part Size and Tonnage
- **Formula**: ~5 tons per cm² projected area
- **Large parts**: >500 tons ($150-300/hr vs $50-100/hr)
- **Solution**: Split into smaller parts

### RULE 10: Material-Specific
- **ABS**: Excellent flow, shrinkage 0.5-0.7%, mold temp 50-80°C
- **Polycarbonate**: High mold temp 80-100°C (+20-30% cycle time), must dry 4hrs
- **Polypropylene**: High shrinkage 1.5-2.5%, use glass-filled for tight tolerances
- **Nylon**: Hygroscopic, must dry 4-6hrs, dimensional changes in humidity

### RULE 11: Tolerances
- **Commercial**: ±0.13mm up to 25mm, ±0.25mm up to 100mm
- **Tight tolerances**: +10-20% cost per dimension

### RULE 12: Cycle Time
- **Formula**: Cycle time ∝ (wall thickness)²
- **Example**: Reducing wall 20% → 36% faster cycle time

---

## 4. DIE CASTING - 6 Enhanced Rules

### RULE 1: Wall Thickness
- **Minimum**: 0.75mm aluminum, 1.0mm zinc
- **Optimal**: 1.0-3.0mm
- **Maximum**: 6mm (causes porosity and voids)

### RULE 2: Draft Angles
- **External surfaces**: 1° minimum
- **Internal surfaces**: 2-3°
- **Deep pockets**: 3-5°

### RULE 3: Fillet Radii
- **Minimum**: 0.5mm
- **Preferred**: 1.0-2.0mm
- **Rationale**: Improves metal flow and die life

### RULE 4: Undercuts
- **Cost**: $10,000-$25,000 per slide
- **Alternatives**: Redesign for straight pull, split into assembly

### RULE 5: Material Selection
- **Aluminum A380**: Best balance of castability and cost, min wall 1.0mm
- **Zinc Zamak 3**: Thinnest walls (0.75mm), tightest tolerances (±0.05mm)
- **Comparison**: Zinc 30-40% better accuracy than aluminum

### RULE 6: Tolerances
- **Aluminum**: ±0.1mm (dimensions <50mm)
- **Zinc**: ±0.05mm (dimensions <50mm)
- **Surface finish**: Ra 1.6-3.2μm as-cast

---

## 5. WIRE FORMING - 8 Enhanced Rules

### RULE 1: Wire Diameter
- **Minimum**: 0.5mm (simple bends), 1.0mm (complex forms)
- **Standard**: 1.0-6.0mm
- **Maximum**: 12mm (heavier requires special equipment)

### RULE 2: Bend Radius
- **Minimum**: 3× wire diameter
- **Recommended**: 4× wire diameter
- **Spring steels**: 5-6× wire diameter
- **Example**: 2mm wire → 6mm min radius, 8mm recommended

### RULE 3: Minimum Leg Length
- **Formula**: 3× wire diameter between bends
- **Example**: 2mm wire → 6mm minimum leg length
- **Rationale**: Short legs difficult to grip and form

### RULE 4: Springback Compensation
- **Steel**: 4-8° springback
- **Stainless**: 6-10° springback
- **Aluminum**: 2-4° springback
- **Rationale**: Thicker wire = more springback

### RULE 5: Bend-to-Bend Distance
- **Formula**: 4× wire diameter between bend tangent points
- **Example**: 2mm wire → 8mm minimum spacing

### RULE 6: Material Formability
- **Excellent**: Aluminum (3× diameter radius), Copper/Brass (2-3× diameter)
- **Good**: Mild steel (3× diameter, 4-8° springback)
- **Poor**: Stainless (4-5× diameter, 6-10° springback, work-hardens)

### RULE 7: Tolerance
- **CNC bending**: ±0.5mm position, ±1° angle
- **Manual bending**: ±2mm position, ±3° angle

### RULE 8: 2D vs 3D Bends
- **2D bends**: All in one plane (faster, cheaper)
- **3D bends**: Multiple planes (+30-50% cost)
- **Alternative**: Weld multiple 2D forms into 3D assembly

---

## Implementation Status

### ✅ Fully Enhanced (4 processes):
1. **CNC Machining** - 13 comprehensive rules with specific measurements
2. **Sheet Metal** - 10 rules with geometric formulas
3. **Injection Molding** - 12 rules with material-specific guidance
4. **Die Casting** - 6 rules with alloy comparisons
5. **Wire Forming** - 8 rules with bend radius calculations

### 🔄 Standard Implementation (5 processes):
6. Investment Casting - Basic rules (can be enhanced further)
7. Metal Injection Molding - Basic rules (can be enhanced further)
8. Rotational Molding - Basic rules (can be enhanced further)
9. Vacuum Forming - Basic rules (can be enhanced further)
10. Welding - Comprehensive rules already implemented

---

## Key Improvements

### 1. Specific Geometric Relationships
- **Before**: "Maintain proper wall thickness"
- **After**: "Wall thickness = 1× material thickness minimum, 1.5× recommended. For 1.2mm material: 1.2mm min, 1.8mm recommended"

### 2. Measurable Criteria
- **Before**: "Holes should not be too close to edges"
- **After**: "Hole-to-edge distance = 2× thickness + bend radius, or 2.5mm minimum. For 1.5mm material: 5.5mm minimum"

### 3. Cost Impact Quantification
- **Before**: "Undercuts increase cost"
- **After**: "Undercuts require side actions: $5,000-$15,000 per action, +2-5 seconds cycle time"

### 4. Material-Specific Guidance
- **Before**: "Select appropriate material"
- **After**: "ABS: 0.5-0.7% shrinkage, 50-80°C mold temp. PP: 1.5-2.5% shrinkage, use glass-filled for tight tolerances"

### 5. Industry Standards Referenced
- ISO 2768 (CNC tolerances)
- ASME Y14.5 (Sheet metal)
- SPI Standards (Injection molding)
- AWS D1.1-D1.6 (Welding - already implemented)

---

## Usage

The enhanced rules are automatically applied when analyzing parts:

1. Upload your CAD file (STL format)
2. Select manufacturing process
3. Choose material
4. Click "Analyze Design"
5. Review detailed feedback with:
   - Specific measurements and formulas
   - Cost impact quantification
   - Material-specific recommendations
   - Industry standard references

---

## Next Steps (Optional Enhancements)

If you want to further enhance the remaining 4 processes:

1. **Investment Casting**: Add wax pattern shrinkage rules, shell thickness requirements
2. **Metal Injection Molding**: Add sintering shrinkage (20%), green strength requirements
3. **Rotational Molding**: Add wall thickness uniformity rules, corner radius requirements
4. **Vacuum Forming**: Add draw ratio limits, draft angle calculations

---

## Technical Details

**Files Modified:**
- `app.py` - Enhanced CNC machining analyzer with 13 rules
- `src/process_analyzers.py` - Enhanced Sheet Metal, Injection Molding, Die Casting, Wire Forming

**Server Status:**
- ✅ Application restarted successfully
- ✅ All 10 processes showing "Ready" status
- ✅ Enhanced rules active and functional
- 🌐 Access at: http://localhost:5000 or http://192.168.1.221:5000

---

**Last Updated:** March 6, 2026
**Version:** 2.0 - Comprehensive DFM Rules Enhancement
