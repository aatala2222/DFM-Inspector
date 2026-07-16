# Die Casting Enhancement Complete

## Summary
Successfully integrated comprehensive die casting design guidelines from **930-00166_R01** (High Pressure Die Cast and Gravity Cast Permanent Mold - 20 pages) into the DFM Inspector.

## Implementation Details

### New Files Created
- **`src/die_casting_enhanced.py`** - Enhanced die casting analyzer with rule-by-rule breakdown
- **`DIE_CASTING_RULES_FROM_930-00166.md`** - Complete rule extraction and documentation
- **`die_casting_extracted.txt`** - Raw extracted text from PDF
- **`extract_die_casting.py`** - PDF extraction script

### Files Modified
- **`app.py`** - Updated to use `analyze_die_casting_enhanced()` instead of basic analyzer

## Design Rules Implemented

### 1. Wall Thickness
- **HPDC Standard**: Nominal 3mm, Minimum 2mm
- **Perm Mold Standard**: Nominal 4mm, Minimum 3-4mm
- **Status**: PASS/FAIL/WARNING based on thickness
- **Checks**: 
  - FAIL if <2mm HPDC or <3mm Perm Mold (incomplete fill, porosity)
  - WARNING if >10mm (shrink porosity risk)
  - WARNING if below nominal (reduced flow quality)
  - PASS if ≥nominal thickness
- **Cost Impact**: Walls below minimum: 40-60% scrap rate

### 2. Draft Angles
- **HPDC Standard**: 1.5° minimum per side
- **Perm Mold Standard**: 3.0° minimum per side
- **Status**: WARNING (cannot auto-detect from geometry)
- **Checks**: Manual verification required
- **Rationale**: Enables part ejection without sticking or warpage
- **Cost Impact**: No draft: +20-30% cycle time, 15-25% scrap rate

### 3. Corner Radii and Fillets
- **Standard**: Minimum internal radius 0.5mm. External radius = internal R + wall thickness
- **Status**: WARNING (design consideration)
- **Checks**: Manual verification required
- **Rationale**: Sharp corners are stress concentrators, mold corners wear quickly
- **Cost Impact**: Sharp corners: 40-60% reduction in part strength, 20-30% shorter tool life

### 4. Minimum As-Cast Hole Diameter
- **HPDC Standard**: Cast holes ≥5mm, drill holes <5mm post-CNC
- **Perm Mold Standard**: Variable based on depth and draft (consult supplier)
- **Status**: INFO (design guideline)
- **Rationale**: Small holes risk core pin breakage, poor hole quality
- **Cost Impact**: Casting holes ≥5mm saves $0.30-$0.80 per hole vs drilling

### 5. Machining Stock (Over-Cast Material)
- **HPDC Standard**: Add 1mm over-cast material
- **Perm Mold Standard**: Add 1.5-2mm over-cast material
- **Status**: INFO (design guideline)
- **Rationale**: Ensures sufficient material for precision machining without hitting porosity
- **Cost Impact**: Insufficient stock: 20-30% scrap. Excess stock: +10-20% CNC time

### 6. Uniform Wall Thickness
- **Standard**: Maintain consistent thickness, avoid abrupt transitions
- **Status**: WARNING (design consideration)
- **Checks**: Design guideline
- **Rationale**: Non-uniform walls cause differential cooling, warpage, porosity
- **Cost Impact**: Non-uniform walls: 25-35% higher scrap rate

## Process Comparison: HPDC vs Permanent Mold

| Characteristic | HPDC | Permanent Mold |
|---------------|------|----------------|
| **Wall Thickness** | 3mm nominal, 2mm min | 4mm nominal, 3-4mm min |
| **Draft Angle** | 1.5° minimum | 3.0° minimum |
| **Surface Finish** | 60-120 RMS | 250-420 RMS |
| **Linear Tolerance** | ±0.25mm/25mm | ±0.38mm/25mm |
| **Parting Line Tolerance** | +0.25mm | +0.76-1.0mm |
| **Mold Steel Gap** | 3mm minimum | 6mm minimum |
| **Machining Stock** | 1mm | 1.5-2mm |
| **Min Cast Hole** | 5mm diameter | Variable (consult supplier) |
| **Cycle Time** | 60-100 seconds | 240-280 seconds |
| **Part Strength** | 30-50% stronger (as-cast) | Lower, but can cast thicker |
| **Tooling Cost** | $15K-$300K+ | $10K-$60K+ |
| **Tool Life** | 100K shots | 60K shots |

## Output Format

Each rule includes:
- **name**: Rule name (e.g., "Wall Thickness")
- **standard**: Industry standard specification from 930-00166
- **status**: PASS/FAIL/WARNING/INFO
- **measured_value**: Actual measurement from geometry
- **evaluation**: Detailed assessment
- **recommendation**: Specific action to take
- **rationale**: Technical explanation of WHY it matters
- **cost_impact**: Financial impact of non-compliance

## Key Design Principles from 930-00166

### Promote Good Part Fill
1. Maintain uniform wall thickness
2. Avoid abrupt thickness transitions
3. Bridge hanging/isolated features
4. Consider gate location and flow direction
5. Add feeder ribs for orthogonal ribbing

### Minimize Porosity Risk
1. Avoid thick sections (>10mm) - shrink porosity risk
2. Use gradual thickness transitions (3:1 taper)
3. Proper venting for air evacuation
4. Stay within 1mm of surface when machining HPDC (avoid deep porosity)

### Reduce Tooling Cost
1. Simple parting lines (easier tooling, better maintenance)
2. Minimize side action/slides (each adds ~10% to tool cost)
3. Standard draft angles (1.5° HPDC, 3° Perm Mold)
4. Avoid undercuts - use CNC instead when cost-effective

### Improve Part Quality
1. Add corner radii (minimum 0.5mm internal)
2. Proper draft angles (prevents sticking, warpage)
3. Cast datums on one die side (maintains stability over tool life)
4. Adequate machining stock (1mm HPDC, 1.5-2mm Perm Mold)

## Cost Optimization Suggestions

1. **Cast holes ≥5mm, drill smaller holes**
   - Savings: $0.30-$0.80 per hole
   - Difficulty: Easy

2. **Add proper machining stock**
   - Savings: Prevents scrap from insufficient material
   - Difficulty: Easy

3. **Simplify parting lines**
   - Savings: 10-20% tooling cost reduction
   - Difficulty: Medium

4. **Eliminate side action/slides**
   - Savings: ~10% per slide eliminated
   - Difficulty: Medium (may require post-CNC)

5. **Use thread-forming fasteners**
   - Savings: Eliminates tapping operations
   - Difficulty: Easy

## Materials Covered

### High Pressure Die Casting
- **A380**: General purpose aluminum alloy (most common)
- **AlSi12(Fe)**: Improved thermal conductivity (~30% better)

### Permanent Mold
- **319.0**: Primary aluminum alloy for permanent mold

### Other Materials
- Magnesium, Zinc (consult supplier for specific guidelines)
- NOT suitable for: Iron, Steel, Stainless Steel

## Finishes Available

| Finish | Cost | Conductive? | Corrosion Protection? | Apply Pre-CNC? |
|--------|------|-------------|----------------------|----------------|
| Raw Casting | $ | Yes | No | N/A |
| Chromate Conversion | $ | Yes | Yes | Typically post-CNC |
| E-coat | $ | No | Yes | Typically post-CNC |
| Anodize | $$ | Not usually | Yes | Typically post-CNC |
| Powder Coat | $ | No | Yes | Can apply pre-CNC |

## Testing

To test the enhanced die casting analyzer:

1. Start the server (already running):
   ```bash
   python app.py
   ```

2. Upload a die casting STEP file

3. Select "Die Casting" process

4. Review the detailed rule-by-rule analysis

## Expected Results

For a typical die cast part:
- Wall thickness check (PASS if ≥3mm nominal, FAIL if <2mm)
- Draft angle reminder (WARNING - verify 1.5° minimum)
- Corner radii reminder (WARNING - verify 0.5mm minimum internal)
- Hole diameter guideline (INFO - cast ≥5mm, drill <5mm)
- Machining stock guideline (INFO - add 1mm)
- Uniform thickness reminder (WARNING - avoid abrupt transitions)

## Source Document

All rules extracted from:
**930-00166_R01 - Design Guideline: High Pressure Die Cast and Gravity Cast Permanent Mold**
- 20 pages of comprehensive design guidelines
- Process comparison: HPDC vs Permanent Mold
- Materials: Aluminum (A380, AlSi12(Fe), 319.0), Magnesium, Zinc
- Tolerances: NADCA standards (HPDC), Aluminum Association standards (Perm Mold)
- Cost drivers and optimization strategies

## Process Type Selection

The analyzer defaults to HPDC (High Pressure Die Casting) but can be configured for Permanent Mold:
- **HPDC**: Faster cycle time, tighter tolerances, better surface finish, higher tooling cost
- **Permanent Mold**: Slower cycle time, looser tolerances, lower tooling cost, can cast larger/thicker parts

## Status

✅ Enhanced die casting analyzer implemented
✅ All 6 critical rules from 930-00166 integrated
✅ HPDC and Permanent Mold parameters included
✅ Cost impact analysis included
✅ app.py updated to use enhanced analyzer
✅ Server restarted and running
🔄 Ready for testing with user's files

## Summary of All Enhanced Processes

The DFM Inspector now has enhanced analyzers for:

1. **CNC Machining** - Comprehensive rules with tolerances, hole specs, thread standards
2. **Welding** - AWS standards integration (D1.1, D1.2, D1.3, D1.6)
3. **Sheet Metal** - 930-00172 (6 rules: thickness, hole diameter, edge distance, spacing, bend radius, flange length)
4. **Injection Molding** - 930-00164 (5 rules: wall thickness, draft, uniformity, ribs, radii)
5. **Die Casting** - 930-00166 (6 rules: wall thickness, draft, radii, holes, machining stock, uniformity)

All processes provide rule-by-rule breakdown with:
- Industry standard specifications
- Pass/Fail/Warning/Info status
- Measured values from geometry
- Detailed recommendations
- Technical rationale
- Cost impact analysis
