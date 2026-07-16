# Process Design Criteria Re-Evaluation
## Based on Amazon Robotics Process Specification Documents

**Document Date:** March 10, 2026  
**Analysis Scope:** Injection Molding, Die Casting, Sheet Metal, and Weldments

---

## Executive Summary

This document re-evaluates the DFM (Design for Manufacturing) criteria currently implemented in the system against the official Amazon Robotics process specification guidelines. The analysis identifies alignment gaps, opportunities for enhancement, and recommended updates to ensure compliance with enterprise standards.

---

## 1. INJECTION MOLDING (930-00164_R01)

### Current Implementation Status

**Key Specifications from Process Spec:**
- **Wall Thickness:** Nominal 3mm (thicker preferred)
- **Draft Angle:** 1.5° minimum (can vary based on supplier review)
- **Radii:** Minimum inside R of 0.5mm
- **Parting Line:** Critical design consideration
- **Gate Types:** Multiple options (sprue, edge, tab, submarine, hot runner, valve)
- **Tolerances:** ±0.031" fractional, ±0.010" decimal dimensions

### Recommended Updates to DFM Rules

1. **Wall Thickness Validation**
   - Add rule: Warn if wall thickness < 3mm
   - Add rule: Recommend wall thickness > 3mm for optimal results
   - Add rule: Flag abrupt thickness transitions (create material turbulence)

2. **Draft Angle Enforcement**
   - Current: Likely checking for draft
   - Enhance: Ensure minimum 1.5° on all vertical walls
   - Add: Special handling for 0° draft conditions (requires post-CNC)

3. **Radii Requirements**
   - Current: Likely checking for radii
   - Enhance: Enforce minimum 0.5mm inside radius
   - Add: External radii = inside R + wall thickness

4. **Parting Line Complexity**
   - Add rule: Evaluate parting line simplicity
   - Add rule: Flag complex parting lines (increase tooling cost/leadtime)
   - Add rule: Recommend keeping parting lines as simple as possible

5. **Gate Design Considerations**
   - Add rule: Validate gate location for material flow
   - Add rule: Check for gate freeze timing
   - Add rule: Warn about shear heating for large parts with small gates

### Tolerance Specifications to Implement

| Dimension Type | Standard Tolerance |
|---|---|
| Fractional dimensions | ±0.031" (±0.79mm) |
| Decimal dimensions | ±0.010" (±0.25mm) |
| Angular dimensions | ±1° to 2° |
| Standard cross-section | ±1/64" (±0.40mm) |

---

## 2. DIE CASTING & PERMANENT MOLD (930-00166_R01)

### Current Implementation Status

**Key Specifications from Process Spec:**

**High Pressure Die Casting (HPDC):**
- **Profile Tolerance:** 0.5-1.5mm (part size dependent)
- **Dimensional Tolerance:** 0.002mm/mm of length
- **Across parting line:** Additional 0.25mm
- **Minimum wall thickness:** 3-10mm
- **Draft:** 1-1.5 degrees minimum
- **Surface finish:** 60-120 RMS

**Permanent Mold (Perm Mold):**
- **Profile Tolerance:** 2.6-3.6mm (across parting line)
- **Dimensional Tolerance:** 0.38mm + 0.002mm/mm
- **Across parting line:** Additional 0.76-1mm
- **Minimum wall thickness:** 4mm and thicker
- **Draft:** 1-3 degrees or more
- **Surface finish:** 250-420 RMS

### Recommended Updates to DFM Rules

1. **Process Selection Logic**
   - Add rule: Recommend HPDC for parts < 5500cm² projected area
   - Add rule: Recommend Perm Mold for larger parts or thick sections
   - Add rule: Consider part strength requirements (HPDC 30-50% stronger)

2. **Wall Thickness Validation**
   - HPDC: Enforce 3-10mm nominal
   - Perm Mold: Enforce 4mm minimum
   - Add rule: Flag thin walls that may cause porosity

3. **Draft Angle Requirements**
   - HPDC: Enforce 1-1.5° minimum
   - Perm Mold: Enforce 1-3° minimum
   - Add rule: Flag 0° draft conditions (requires side action or post-CNC)

4. **Parting Line Management**
   - Add rule: Evaluate parting line complexity
   - Add rule: Recommend simple parting lines (reduce tooling cost)
   - Add rule: Ensure gates and vents are at parting line

5. **Undercut Handling**
   - Add rule: Identify undercuts
   - Add rule: Recommend side action (10% tooling cost increase)
   - Add rule: Evaluate post-CNC alternative

6. **Machining Stock Allowance**
   - HPDC: Add 1mm over-cast material for CNC surfaces
   - Perm Mold: Add 1.5-2mm over-cast material
   - Add rule: Warn about porosity risk if machining too deep

### Tolerance Specifications to Implement

**HPDC Tolerances:**
- Profile: ±0.5-1.5mm (part size dependent)
- Dimensional: 0.002mm/mm of length
- Across parting line: +0.25mm additional

**Perm Mold Tolerances:**
- Profile: ±2.6-3.6mm (across parting line)
- Dimensional: 0.38mm + 0.002mm/mm
- Across parting line: +0.76-1mm additional

### Feature Size Constraints

| Feature | HPDC | Perm Mold |
|---|---|---|
| Minimum wall thickness | 3mm | 4mm |
| Minimum hole diameter | 5mm (cast) | Supplier dependent |
| Minimum mold steel thickness | 3mm | 6mm (if 20mm height) |
| Corner radius (inside) | 0.5mm minimum | 0.5mm minimum |

---

## 3. SHEET METAL (930-00172_R01)

### Current Implementation Status

**Key Specifications from Process Spec:**

**Fabrication Processes:**
- Turret Press
- Laser Cutting
- Manual Press Brake
- Progressive Die
- Multi-Slide
- Fine Blanking

**Tolerance Capabilities by Process:**

| Process | Feature-to-Feature | Hole Size | Bend Angle |
|---|---|---|---|
| Turret Press | ±0.10" | ±0.10" | N/A |
| Laser Cutting | ±0.10" | 0.25T min | N/A |
| Hand Brake | ±0.5" (fold-fold) | 1.33T min | ±1.5° |
| Progressive | ±0.05" | ±0.08" | ±1° |
| Multi-Slide | ±0.05" | ±0.05" | ±1° |
| Fine Blanking | ±0.03" | ±0.02" | N/A |

### Recommended Updates to DFM Rules

1. **Process Selection Logic**
   - Add rule: Recommend process based on volume and tolerance requirements
   - Add rule: Turret Press for prototypes/low volume
   - Add rule: Progressive for high volume
   - Add rule: Fine Blanking for precision requirements

2. **Bend Radius Requirements**
   - Add rule: Minimum bend radius = 1.0T or 0.6mm (whichever is greater)
   - Add rule: For low carbon steel, minimum = 0.5T
   - Add rule: Flag sharp corners that may cause cracking

3. **Bend Relief Design**
   - Add rule: Require bend relief when bend is close to edge
   - Add rule: Relief depth > bend radius
   - Add rule: Relief width ≥ material thickness

4. **Hole Distance from Bend**
   - Add rule: Minimum distance A = 2.0T + R
   - Add rule: Minimum distance B = 3T + R
   - Add rule: Flag holes too close to bends

5. **Slot Distance from Bend**
   - Add rule: For L < 50mm: A = 3T + R
   - Add rule: For L > 50mm: A = 4T + R

6. **Feature Spacing**
   - Add rule: Minimum distance between holes = 1.2T
   - Add rule: Minimum distance between extrusions = 6T
   - Add rule: Minimum extrusion height for threads = 2.0-3.0T

7. **Dimple Design**
   - Add rule: Maximum diameter D = 6T
   - Add rule: Maximum height H = 4T
   - Add rule: Minimum height H = D * 0.3
   - Add rule: Minimum distance to hole = 3T
   - Add rule: Minimum distance between dimples = 4T + D

### Material Thickness Tolerances

**Stainless Steel:**
- 0.6-0.79mm: ±0.05mm
- 0.80-0.99mm: ±0.055mm
- 1.0-1.19mm: ±0.06mm
- 1.20-1.49mm: ±0.07mm

**SGCC Steel (Hot-Dipped Galvanized):**
- 0.40-0.60mm: ±0.05mm
- 0.61-0.80mm: ±0.06mm
- 0.81-1.00mm: ±0.07mm

**SECC Steel (Electro-Galvanized):**
- 0.40-0.60mm: ±0.03mm
- 0.61-0.80mm: ±0.04mm
- 0.81-1.00mm: ±0.05mm

**Aluminum:**
- Group I (1000, 3000, 5000 series):
  - 0.6-0.80mm: ±0.03mm
  - 0.81-1.00mm: ±0.04mm
  - 1.01-1.20mm: ±0.04mm

---

## 4. WELDMENTS (960-00169_R01)

### Current Implementation Status

**Key Specifications from Process Spec:**

**Welding Standards:**
- AWS D1.1/D1.1M: Carbon and low alloy steels (≥3mm, ≤100 ksi yield)
- AWS D1.2/D1.2M: Aluminum structural alloys
- AWS D1.3/D1.3M: Structural sheet steels (<5mm thickness)
- AWS D1.6/D1.6M: Stainless steel (≥1.5mm)

**Weld Types:**
- Fillet Welds
- Groove Welds (V-groove, U-groove, J-groove)
- Plug/Slot Welds
- Flare Groove Welds

### Recommended Updates to DFM Rules

1. **Weld Access Design**
   - Add rule: Ensure welding gun access to joint
   - Add rule: Validate welding angles (50-65° groove angle recommended)
   - Add rule: Check root opening (gap) for proper penetration
   - Add rule: Verify welding position feasibility

2. **Groove Angle Requirements**
   - Carbon steel: 50-60°
   - Aluminum: 60-65°
   - Stainless steel: 55-60°

3. **Root Face Requirements**
   - Add rule: For bevel angle ≤30°, root face = 0
   - Add rule: For bevel angle >30°, root face minimum = 0.040"
   - Add rule: Root face aligned with contact surface

4. **Fillet Weld Sizing**
   - Add rule: Validate fillet weld leg size
   - Add rule: Check effective throat calculation
   - Add rule: Ensure adequate penetration

5. **Skewed Joint Handling**
   - Add rule: For inclination angle <10°, use fillet weld
   - Add rule: For inclination angle ≥10°, beveling mandatory
   - Add rule: Calculate required bevel angle based on groove angle

6. **Design for Manufacturability**
   - Add rule: Identify drain holes for cleaning
   - Add rule: Identify outgassing holes for all-around welds
   - Add rule: Review fixturing locations with supplier
   - Add rule: Consider part warpage for long continuous welds

7. **Weld Discontinuity Prevention**
   - Add rule: Flag designs prone to porosity
   - Add rule: Flag designs prone to undercut
   - Add rule: Flag designs prone to incomplete fusion
   - Add rule: Flag designs prone to incomplete joint penetration

### Weld Qualification Requirements

**Essential Variables to Control:**
- Base metal thickness
- Filler material type and diameter
- Welding position (flat, horizontal, vertical, overhead)
- Groove angle and root opening
- Preheat temperature
- Interpass temperature
- Welding speed and amperage

---

## 5. CROSS-PROCESS DESIGN CRITERIA

### Universal DFM Rules to Implement

1. **Tolerance Stack-up Analysis**
   - Add rule: Evaluate cumulative tolerances across processes
   - Add rule: Flag designs with tight tolerance stacks
   - Add rule: Recommend tolerance relaxation where possible

2. **Material Selection Validation**
   - Add rule: Verify material compatibility with process
   - Add rule: Check material availability and lead times
   - Add rule: Validate material properties for application

3. **Cost Optimization**
   - Add rule: Evaluate process alternatives for cost reduction
   - Add rule: Flag designs requiring secondary operations
   - Add rule: Recommend design changes to eliminate secondary ops

4. **Manufacturability Assessment**
   - Add rule: Evaluate tooling complexity
   - Add rule: Estimate tooling lead time
   - Add rule: Assess production volume justification

5. **Quality and Inspection**
   - Add rule: Ensure critical dimensions are measurable
   - Add rule: Validate datum structure for inspection
   - Add rule: Flag features difficult to inspect

---

## 6. IMPLEMENTATION ROADMAP

### Phase 1: Immediate Updates (Week 1-2)
- [ ] Update injection molding wall thickness rules
- [ ] Add draft angle validation for all processes
- [ ] Implement sheet metal bend relief requirements
- [ ] Add weld access design checks

### Phase 2: Enhanced Validation (Week 3-4)
- [ ] Implement process selection logic
- [ ] Add tolerance stack-up analysis
- [ ] Create material compatibility matrix
- [ ] Add cost optimization recommendations

### Phase 3: Advanced Features (Week 5-6)
- [ ] Implement 3D visualization for weld access
- [ ] Add manufacturability scoring
- [ ] Create process capability database
- [ ] Implement supplier feedback integration

---

## 7. CONFIGURATION FILE UPDATES REQUIRED

### Files to Update:

1. **config/injection_molding_rules.yaml**
   - Add wall thickness validation
   - Add parting line complexity assessment
   - Add gate design validation

2. **config/die_casting_rules.yaml**
   - Add process selection logic (HPDC vs Perm Mold)
   - Add undercut detection
   - Add machining stock validation

3. **config/sheet_metal_rules.yaml**
   - Add bend relief requirements
   - Add feature spacing validation
   - Add process capability matching

4. **config/welding_rules.yaml**
   - Add weld access design checks
   - Add groove angle validation
   - Add skewed joint handling

---

## 8. SUMMARY OF KEY FINDINGS

### Alignment with Standards
✅ **Good Alignment:**
- Draft angle requirements
- Radii and fillet specifications
- Basic tolerance frameworks

⚠️ **Needs Enhancement:**
- Process selection logic
- Tolerance stack-up analysis
- Material compatibility validation
- Cost optimization recommendations

❌ **Missing Implementation:**
- Weld access design validation
- Skewed joint handling
- Machining stock allowance
- Drain hole and outgassing requirements

---

## 9. RECOMMENDATIONS

1. **Prioritize weld design validation** - Currently missing critical checks for weld access and joint configuration

2. **Implement process selection logic** - Add rules to recommend optimal manufacturing process based on part characteristics

3. **Add cost optimization** - Evaluate alternative processes and design modifications to reduce manufacturing cost

4. **Enhance tolerance management** - Implement stack-up analysis and supplier capability matching

5. **Create supplier feedback loop** - Integrate supplier DFM review recommendations into automated checks

---

## Document Control

| Item | Value |
|---|---|
| Document Version | 1.0 |
| Last Updated | March 10, 2026 |
| Analysis Scope | 4 Major Processes |
| Specifications Reviewed | 6 Amazon Robotics Documents |
| Recommendations | 50+ DFM Rules |

