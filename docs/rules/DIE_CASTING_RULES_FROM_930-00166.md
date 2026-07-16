# Die Casting Design Rules - Extracted from 930-00166_R01

## Key Design Guidelines from Amazon Robotics Document (20 pages)

### Document Overview
**Title:** Design Guideline - High Pressure Die Cast and Gravity Cast Permanent Mold
**Processes Covered:** 
- High Pressure Die Casting (HPDC)
- Gravity Cast Permanent Mold (Perm Mold)
**Materials:** Aluminum (A380, AlSi12(Fe), 319.0), Magnesium, Zinc

---

## Critical Design Rules

### 1. Wall Thickness

#### High Pressure Die Casting (HPDC)
- **Nominal**: 3mm (thicker preferred)
- **Minimum**: 2.0mm
- **Rationale**: Thin walls risk incomplete fill, porosity. Thick walls risk shrink porosity.

#### Permanent Mold
- **Nominal**: 4mm (thicker preferred)
- **Minimum**: 3-4mm (supplier feedback required)
- **Rationale**: Gravity feed requires thicker walls for reliable fill.

**Key Principle:** Maintain uniform wall thickness throughout part. Avoid abrupt transitions.

---

### 2. Draft Angles

#### High Pressure Die Casting
- **Minimum**: 1.5 degrees
- **Rationale**: Enables part ejection without sticking or warpage

#### Permanent Mold
- **Minimum**: 3.0 degrees
- **Rationale**: Higher draft needed due to surface roughness and gravity casting process

**Note:** Vertical walls (0° draft) require post-CNC machining or side action/slides

---

### 3. Corner Radii and Fillets

- **Minimum Internal Radius**: 0.5mm (HPDC best practice)
- **External Radius**: Internal R + wall thickness (maintains uniform wall)
- **Rationale**: 
  - Sharp corners in mold impossible to maintain over tool life
  - Sharp corners are stress concentrators (part and mold)
  - Improves material flow and part strength

**Exception:** Edges at parting line should not have radii unless functionally required

---

### 4. Minimum Mold Steel Thickness (Feature-to-Feature Gap)

#### High Pressure Die Casting
- **Minimum**: 3mm (thicker preferred)
- **Rationale**: Thin mold steel breaks or wears quickly

#### Permanent Mold
- **Minimum**: 6mm for 20mm height features
- **Rule**: Maintain ~1:3 tool steel width:height ratio
- **Rationale**: Prevents mold deflection and breakage

---

### 5. Minimum As-Cast Hole Diameter

#### High Pressure Die Casting
- **Cast holes**: ≥5mm diameter
- **Drill holes**: <5mm diameter (post-CNC)
- **Rationale**: Small holes difficult to cast, risk of core pin breakage

#### Permanent Mold
- **Variable**: Depends on hole depth and draft angle
- **Consult supplier** for proper blind hole diameter:depth ratio
- **Rationale**: Gravity feed and draft requirements limit small holes

---

### 6. Machining Stock (Over-Cast Material)

#### High Pressure Die Casting
- **Add**: 1mm over-cast material for machined surfaces
- **Warning**: Do not add excess - risk of hitting porosity deeper in part

#### Permanent Mold
- **Add**: 1.5-2mm over-cast material
- **Note**: Excess material less risky but impacts CNC time

**Purpose:** Ensures sufficient material for precision machining while avoiding porosity

---

### 7. Parting Line Design

**Best Practice:** Keep parting lines as simple as possible

**Benefits:**
- Simplified tooling (lower cost, shorter leadtime)
- Easier trim die design and fabrication
- Better tool life and fit/finish
- Easier maintenance of planar parting line

**Note:** Gates and vents are located at parting line

---

### 8. Undercuts and Side Action

**Undercut:** Feature that cannot be manufactured with simple two-part mold

**Management Options:**
1. **Side Action/Slides**: Additional tool steel pieces (adds ~10% to tool cost)
2. **Post-CNC Machining**: Machine features after casting
3. **Ejection Lifter or Pass Core**: Less common, consult supplier

**Cost Consideration:** Analyze slide cost vs CNC cost to determine best approach

---

### 9. Tolerances

#### High Pressure Die Casting (NADCA Standards)
- **Linear (same side)**: ±0.25mm per 25mm + 0.025mm per additional 25mm
- **Across Parting Line**: Add 0.25mm
- **Surface Finish**: 60-120 RMS

#### Permanent Mold (Aluminum Association Standards)
- **Linear (same side)**: ±0.38mm per 25mm + 0.051mm per additional 25mm
- **Across Parting Line**: Add 0.76-1.0mm
- **Surface Finish**: 250-420 RMS

**Key Factors:**
- Tolerance increases with part size
- Across parting line always greater than same side
- Moving cores (slides) have additional tolerance

---

### 10. Datum Strategy

**Critical Rules:**
- Establish cast datums on **same side** of die (cavity OR core, not both)
- Choose side with most functional requirements
- Avoid datums near: ejector pins, parting lines, vents, gates
- Keep cast datums on part (not on tabs that will be machined off)
- Add flat pads on non-orthogonal surfaces when possible

**Rationale:** As mold wears, variability across parting line grows. Single-side datums prevent datum frame variation.

---

## Process Comparison: HPDC vs Permanent Mold

| Characteristic | HPDC | Perm Mold |
|---------------|------|-----------|
| **Wall Thickness** | 3mm nominal, 2mm min | 4mm nominal, 3-4mm min |
| **Draft** | 1.5° minimum | 3.0° minimum |
| **Surface Finish** | 60-120 RMS | 250-420 RMS |
| **Tolerance (linear)** | ±0.25mm/25mm | ±0.38mm/25mm |
| **Tolerance (parting)** | +0.25mm | +0.76-1.0mm |
| **Cycle Time** | 60-100 seconds | 240-280 seconds |
| **Part Strength** | 30-50% stronger (as-cast) | Lower strength, but can cast thicker sections |
| **Max Part Size** | ~5500 cm² (4400 ton press) | Larger parts possible |
| **Tooling Cost** | $15K-$300K+ | $10K-$60K+ |
| **Tool Life** | 100K shots | 60K shots |
| **Piece Part Cost** | Lower (faster cycle) | Higher (slower cycle) |

---

## Design Optimization Guidelines

### Promote Good Part Fill
1. **Uniform wall thickness** - Avoid abrupt transitions
2. **Bridge hanging features** - Connect isolated features to adjacent features
3. **Consider gate location** - Optimize for flow direction
4. **Add feeder ribs** - Mitigate orthogonal ribbing flow disruption
5. **Material bridges** - Add bridges over holes, machine out later

### Minimize Porosity Risk
1. **Avoid thick sections** - Risk of shrink porosity in HPDC
2. **Gradual thickness transitions** - Prevent turbulence and pressure changes
3. **Proper venting** - Ensure air evacuation
4. **Machining depth** - Stay within 1mm of surface in HPDC to avoid porosity

### Reduce Tooling Cost
1. **Simple parting lines** - Easier tooling, better maintenance
2. **Minimize side action** - Each slide adds ~10% to tool cost
3. **Standard draft angles** - 1.5° HPDC, 3° Perm Mold
4. **Avoid undercuts** - Use CNC instead of slides when cost-effective

### Improve Part Quality
1. **Add corner radii** - Minimum 0.5mm internal
2. **Proper draft** - Prevents sticking and warpage
3. **Cast datums on one side** - Maintains datum stability over tool life
4. **Adequate machining stock** - 1mm HPDC, 1.5-2mm Perm Mold

---

## Materials

### High Pressure Die Casting
- **A380**: General purpose alloy (most common at AR)
- **AlSi12(Fe)**: Improved thermal conductivity (~30% better)

### Permanent Mold
- **319.0**: Primary alloy for permanent mold parts

---

## Finishes

| Finish | Cost | Conductive? | Corrosion Protection? | Apply Pre-CNC? | Notes |
|--------|------|-------------|----------------------|----------------|-------|
| Raw Casting | $ | Yes | No | N/A | Risk of oxidation |
| Chromate Conversion | $ | Yes | Yes | Typically post-CNC | Clear finish, thin |
| E-coat | $ | No | Yes | Typically post-CNC | Black, thin, shows as-cast quality |
| Anodize | $$ | Not usually | Yes | Typically post-CNC | Multiple colors, thin |
| Powder Coat | $ | No | Yes | Can apply pre-CNC | Very good cosmetics, robust |

---

## Implementation Priority

### Critical (FAIL if violated):
1. Wall thickness < minimum (2mm HPDC, 3mm Perm Mold)
2. Draft angle < minimum (1.5° HPDC, 3° Perm Mold)
3. Sharp internal corners (no radius)
4. Holes <5mm diameter cast in HPDC

### Important (WARNING if violated):
1. Non-uniform wall thickness
2. Abrupt thickness transitions
3. Complex parting lines
4. Insufficient machining stock
5. Mold steel thickness <3mm HPDC, <6mm Perm Mold

### Optimization (SUGGESTIONS):
1. Simplify parting lines
2. Eliminate side action/slides where possible
3. Use CNC instead of slides for undercuts
4. Add corner radii ≥0.5mm
5. Bridge hanging features
6. Establish datums on one die side
7. Use thread-forming fasteners instead of tapped holes

---

## Cost Drivers

### Tooling Cost Factors:
- Process type (HPDC > Perm Mold)
- Mold complexity (parting line, slides)
- Side action/slides (+10% per slide)
- Trim die complexity

### Piece Part Cost Factors:
- Material alloy (usually negligible difference)
- Cycle time (HPDC faster than Perm Mold)
- Automation level (HPDC more automated)
- Part size (material + cycle time)
- Machining operations
- Finishing process and masking

---

## Key Formulas

1. **Minimum Wall Thickness**: 3mm HPDC, 4mm Perm Mold
2. **Draft Angle**: 1.5° HPDC, 3° Perm Mold
3. **Internal Corner Radius**: ≥0.5mm
4. **External Corner Radius**: Internal R + wall thickness
5. **Mold Steel Gap**: 3mm HPDC, 6mm Perm Mold
6. **Machining Stock**: 1mm HPDC, 1.5-2mm Perm Mold
7. **Minimum Cast Hole**: 5mm HPDC, variable Perm Mold
8. **Linear Tolerance**: ±0.25mm/25mm HPDC, ±0.38mm/25mm Perm Mold
