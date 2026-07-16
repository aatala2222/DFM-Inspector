# DFM Inspector - Rules Reference

Complete catalog of Design for Manufacturability (DFM) rules checked by the DFM Inspector tool.

**Reference Standards:**
- 930-00172_R01 - AR Sheet Metal Design Best Practices
- 930-00166_R01 - Design Guideline, High Pressure Die Cast and Gravity Cast Permanent Mold
- NADCA Product Specification Standards for Die Castings - 11th Edition
- Standards for Aluminum Sand and Permanent Mold Castings - 16th Edition 2021
- Injection Molding DFM AME Presentation (Bruce Johnson, Shinkansan Aug 2023)
- Casting DFM AME Presentation (Milan Lucic, Aug 2023)
- ISO 2768, ASME Y14.5, ISO 1302, ISO 965, ISO 286

---

## Table of Contents

1. [Sheet Metal](#sheet-metal)
2. [CNC Machining](#cnc-machining)
3. [Die Casting (HPDC)](#die-casting-hpdc)
4. [Low Pressure Die Casting (LPDC)](#low-pressure-die-casting-lpdc)
5. [Permanent Mold / Gravity Cast](#permanent-mold--gravity-cast)
6. [Injection Molding](#injection-molding)
7. [Welding](#welding)

---

## Sheet Metal

**Reference:** 930-00172_R01

### Process Capabilities Summary

| Process | Tolerance Feature-to-Feature | Min Hole/Slot | Max Thickness |
|---------|------------------------------|---------------|---------------|
| Turret Press | ±0.10 mm | 1.33T | 3.0 mm |
| Laser Cutting | ±0.10 mm | 0.25T (25% of T) | 3.0 mm |
| Hand Brake Press | Bend ±1.5° | 1.33T | 3.0 mm |
| Progressive Tool | ±0.05 mm (same station) | 1.33T | 3.0 mm |
| Multi Slide | ±0.05 mm | 1.33T | 3.0 mm |
| Fine Blanking | ±0.02 mm | 0.8T (steel), 1.0T (stainless) | 17 mm |

### Rule 1: Material Thickness
- **Standard:** 0.5-6.0mm range, in 0.5mm increments only
- **Acceptable values:** 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0 mm
- **FAIL if:** thickness <0.4mm OR not a 0.5mm increment
- **WARNING if:** thickness >6.0mm

### Rule 2: Minimum Hole Diameter
- **Standard:** 1.33 × T (material thickness)
- **For 2.0mm material:** minimum hole = 2.66mm
- **For 3.0mm material:** minimum hole = 3.99mm
- **FAIL if:** any hole < 1.33T

### Rule 3: Hole to Edge Distance
- **Standard:** 2 × T minimum from hole edge to part edge
- **For 2.0mm material:** minimum 4.0mm
- **FAIL if:** any hole closer than 2T to edge

### Rule 4: Hole Spacing
- **Standard:** 1.2 × T minimum between hole edges
- **For 2.0mm material:** minimum 2.4mm
- **FAIL if:** any hole pair closer than 1.2T edge-to-edge

### Rule 5: Bend Radius
- **Standard:** 1.0T minimum (or 0.6mm, whichever is greater)
- **Low carbon steel exception:** 0.5T minimum
- **For 2.0mm material:** minimum bend radius = 2.0mm
- **FAIL if:** any bend radius < 1.0T

### Rule 6: Flange Length
- **Standard:** 1.33T minimum (absolute), 4T preferred
- **For 2.0mm material:** absolute min = 2.66mm, preferred = 8.0mm
- **FAIL if:** flange < 1.33T
- **WARNING if:** flange between 1.33T and 4T

### Rule 7: Bend Relief
- **Depth:** > bend radius
- **Width:** ≥ material thickness (T)
- **When required:** bending close to an edge

### Rule 8: Extrusions
- **Spacing between extrusions:** ≥ 6T
- **Distance to edge:** ≥ 3T + 2R
- **Distance to bend:** ≥ 3T + R
- **Height for M3 thread engagement:** 2.0T - 2.5T
- **Height for M4 thread engagement:** 2.5T - 3.0T
- **Goal:** 4 thread engagement (~80% strength)

### Rule 9: Dimples
- **Maximum diameter:** 6T
- **Maximum height:** 4T
- **Minimum height:** 0.3 × D (diameter)
- **Min distance to hole:** 3T
- **Min distance between dimples:** 4T + D
- **Min distance to bend:** 2T
- **Min distance to part edge:** 3T + D/2
- **Angle Z:** ≥ 30°

### Rule 10: Hems
- **Min return flange height:** 4T
- **Min distance from hole:** 2T
- **Min distance from internal bend:** 5T
- **Min distance from external bend:** 8T
- **Avoid:** flat hems (fluid entrapment)

### Rule 11: Embossments / Stiffening Ribs
- **Round embossment max height:** 3T
- **V embossment max height:** 3T
- **Min spacing between parallel embossments:** 10T
- **Min distance to edge:** 4T
- **Min distance to hole:** 3T
- **Min distance to fold:** 4T

### Rule 12: Louvers
- **Material thickness range:** 0.8mm - 6mm
- **Min spacing (short edge) P1:** 5mm
- **Min spacing (long edge) P2:** 8mm
- **Max height H:** 0.6 × A
- **Min height H:** 3T
- **Radius R:** > H

### Rule 13: Lance and Form
- **Min height:** 2T
- **Min distance to fold:** 3T + R
- **Min distance to hole:** 3T
- **Min web between lances:** 6T
- **Bend relief:** not required

### Rule 14: Half Shear
- **Max height per operation:** 0.5T
- **Min feature width/diameter:** 2T
- **Multiple shears:** can be stacked for greater height

### Hole Distance from Bend
- **A min (perpendicular):** 2.0T + R
- **B min (parallel):** 3T + R
- **R min:** 1.0T or 0.6mm minimum

### Slot Distance from Bend
- **L < 50mm:** A = 3T + R
- **L > 50mm:** A = 4T + R
- **R min:** 1.0T or 0.6mm

### Z Bends
- **Maximum height:** 5T
- **Bend radius:** 1.5T (90° offset), 0.2mm (45° offset)

---

## CNC Machining

**Reference:** ISO 2768, ASME Y14.5, ISO 1302, ISO 965, ISO 286

### Rule 1: Wall Thickness (material-specific)

| Material | Minimum | Recommended | Cost Multiplier |
|----------|---------|-------------|-----------------|
| Aluminum 6061/7075 | 0.8 mm | 1.0 mm | 1.0× |
| Mild Steel | 1.0 mm | 1.5 mm | 1.3× |
| Stainless Steel | 1.2 mm | 1.5 mm | 2.0× |
| Brass / Copper | 0.8 mm | 1.0 mm | 1.5× |
| Titanium | 1.5 mm | 2.0 mm | 4.0× |

### Rule 2: Internal Corner Radii
- **Standard:** Minimum radius ≥ tool radius
- **Recommended:** radius = 1/3 × pocket depth
- **Standard sizes:** 0.5mm, 1mm, 3mm, 5mm
- **Sharp corners:** require EDM (+200-400% cost)

### Rule 3: Hole Diameter and Depth
- **Standard sizes:** 3, 4, 5, 6, 8, 10, 12mm (use these to avoid custom tooling)
- **Maximum depth:** 4× diameter (standard drill)
- **Optimal depth:** 2-3× diameter

### Rule 4: Tolerance Specifications
- **Standard:** ±0.1mm for non-critical features
- **Precision:** ±0.01-0.02mm for critical only
- **Target:** <20% tight tolerances
- **Cost impact:** Tight tolerances 1.8-2.5× standard cost

### Rule 5: Setup Minimization
- **Target:** ≤2 setups on 3-axis CNC
- **Each additional setup:** +30-40% cost
- **Tip:** Orient critical features to 1-2 sides

### Rule 6: Material Machinability

| Material | Rating | Cost Multiplier |
|----------|--------|-----------------|
| Aluminum 6061 | ★★★★★ | 1.0× |
| Brass | ★★★★☆ | 1.5× |
| Mild Steel | ★★★☆☆ | 1.3× |
| Stainless 304 | ★★☆☆☆ | 2.0× |
| Titanium | ★☆☆☆☆ | 4.0× |

---

## Die Casting (HPDC)

**Reference:** 930-00166_R01, NADCA 11th Edition

### Process Capabilities
- **Profile tolerance:** ±0.5mm typical (across parting line: +0.25mm)
- **Cycle time:** 60-100 seconds
- **Tool cost:** $15K-$300K+
- **Tool life:** 100K shots
- **Maximum projected area:** 5500 cm² (4400-ton press)

### Rule 1: Wall Thickness
- **Minimum feature:** 2.5 mm
- **Nominal:** 3.0 mm
- **Preferred:** 4.0 mm
- **Maximum (HPDC):** 10mm — thicker = porosity risk
- **FAIL if:** thickness < 2.5mm

### Rule 2: Corner Radii & Fillets
- **Internal:** ≥ 0.5mm minimum
- **External:** = internal + wall thickness
- **Exception:** Parting line edges should NOT have radii

### Rule 3: Draft Angles
- **HPDC:** 1.5° minimum
- **Critical:** addresses part shrinkage and ejection forces
- **Without draft:** part sticks/breaks on ejection

### Rule 4: Cast Hole Diameter
- **Minimum as-cast:** 5mm
- **Smaller holes:** must be post-cast CNC machined
- **Reason:** mold pins <5mm are fragile and break

### Rule 5: Feature-to-Feature Gap
- **Minimum:** 3mm (mold steel between features)
- **Smaller gaps:** mold overheats, cracks, fails

### Rule 6: Machining Stock
- **HPDC:** 1mm over-cast material
- **Don't exceed** — deeper cuts expose porosity

### Rule 7: Slides and Undercuts
- **Each slide:** +10% tool cost (~$2K-$10K)
- **Avoid if possible** — alternative is post-CNC

### Rule 8: Parting Line
- **Keep simple:** planar parting lines preferred
- **Complex parting:** +$5K-$30K tool cost

### Rule 9: Materials
- **A380 Aluminum:** ~85% Al, 8% Si, 4% Cu (general purpose)
- **AlSi12(Fe):** ~30% better thermal conductivity than A380

---

## Low Pressure Die Casting (LPDC)

**Reference:** 930-00166_R01

### Process Capabilities
- **Profile tolerance:** ±1.0mm typical
- **Cycle time:** 240-280 seconds
- **Tool cost:** $10K-$60K+
- **Best for:** round/symmetric parts (filling physics)

### Rule 1: Wall Thickness
- **Minimum:** 3.0 mm
- **Nominal:** 4.0 mm
- **Preferred:** 5.0 mm

### Rule 2: Draft Angles
- **Minimum:** 3.0°
- **Up to 7°** depending on draw depth

### Rule 3: Feature-to-Feature Gap
- **Minimum:** 6mm (larger than HPDC due to lower pressure)

### Rule 4: Machining Stock
- **LPDC:** 1.5-2mm over-cast material

---

## Permanent Mold / Gravity Cast

**Reference:** 930-00166_R01

### Process Capabilities
- **Profile tolerance:** ±2.6mm typical
- **Cycle time:** 240-280 seconds
- **Tool cost:** $10K-$60K+
- **Tool life:** 60K shots
- **Best for:** large structural parts with thick cross-sections

### Rule 1: Wall Thickness
- **Minimum:** 3.5 mm
- **Nominal:** 5.0 mm
- **Preferred:** 6.0 mm
- **Can handle thicker sections than HPDC**

### Rule 2: Draft Angles
- **Minimum:** 3.0°
- **Higher draft prevents sticking** (no high-pressure injection)

### Rule 3: Feature-to-Feature Gap
- **Minimum:** 6mm

### Rule 4: Machining Stock
- **Perm Mold:** 3mm over-cast material
- **Excess less risky** due to reduced porosity vs HPDC

### Rule 5: Materials
- **319.0 Aluminum:** primary alloy for permanent mold

---

## Injection Molding

**Reference:** Shinkansan Aug 2023 (Bruce Johnson, AME)

### Material Wall Thickness Ranges

| Material | Min | Max | Type | Shrinkage |
|----------|-----|-----|------|-----------|
| POM (Acetal) | 0.75 | 3.00 | Crystalline | 2.0% |
| Nylon (PA) | 0.25 | 3.00 | Crystalline | 1.5% |
| PP (Polypropylene) | 0.60 | 3.80 | Crystalline | 1.8% |
| PBT | 0.60 | 3.20 | Crystalline | 1.6% |
| PET | 0.60 | 3.20 | Crystalline | 1.6% |
| ABS | 1.00 | 3.50 | Amorphous | 0.6% |
| HIPS (Styrene) | 0.60 | 3.80 | Amorphous | 0.6% |
| PPO/PPE (Noryl) | 1.00 | 3.50 | Amorphous | 0.7% |
| PC (Polycarbonate) | 1.00 | 3.80 | Amorphous | 0.6% |
| PMMA (Acrylic) | 1.00 | 3.80 | Amorphous | 0.4% |
| SAN | 0.80 | 3.80 | Amorphous | 0.4% |

### Rule 1: Uniform Wall Thickness
- **Standard:** Maintain wall thickness within ±10% across part
- **Avoid:** abrupt thickness changes (causes sink, warpage, weld lines)

### Rule 2: Draft Angles
- **Vertical walls:** 3° minimum
- **Shutoff surfaces:** 5° minimum
- **Rib sides:** 0.5° minimum

### Rule 3: Rib Design
- **Rib base:** 50-60% of wall thickness
- **Maximum height:** 3T
- **Spacing between ribs:** ≥ 3T
- **Rib draft:** 0.5° minimum
- **Base fillet:** 0.4mm minimum

### Rule 4: Fillets and Radii
- **Internal fillets:** 25-60% of wall (minimum 0.4mm)
- **External radius:** = internal + wall thickness

### Rule 5: Tolerance Specification

#### Toolbound Commercial Tolerances (mm)
| Feature Size | 0-10mm | 10-25mm | 25-50mm | 50-75mm | 75-100mm | 100-150mm |
|--------------|--------|---------|---------|---------|----------|-----------|
| Tolerance | ±0.100 | ±0.125 | ±0.150 | ±0.200 | ±0.225 | ±0.250 |

#### Non-Toolbound Commercial Tolerances (mm)
| Feature Size | 0-10mm | 10-25mm | 25-50mm | 50-75mm | 75-100mm | 100-150mm |
|--------------|--------|---------|---------|---------|----------|-----------|
| Tolerance | ±0.200 | ±0.225 | ±0.250 | ±0.300 | ±0.350 | ±0.400 |

**Toolbound** = within single non-moving tool piece (tighter tolerances)
**Non-toolbound** = across parting line, lifters, slides, cavity-to-core

### Rule 6: Snap Fit Design
- **Avoid:** steady-state load on snapped position (creep)
- **Use pass cores** for hooks when possible
- **Taper snap beam** for even stress distribution

### Rule 7: Undercuts
- **External undercuts:** require slides (+10% tool cost each)
- **Internal undercuts:** require lifters
- **Pass cores:** simpler alternative when accessible

---

## Welding

**Reference:** AWS D1.1, D1.2, D1.3, D1.6

### Rule 1: Groove Angles
- **Standard:** 50-65° depending on material
- **Purpose:** ensure proper fusion

### Rule 2: Skewed Joints
- **Beveling required** based on joint angle

### Rule 3: Weld Access
- **Adequate space required** for welding gun and arc visibility

### Rule 4: Material Thickness
- **Per AWS D1.x standards** (varies by material/process)

### Rule 5: Root Opening
- **Proper gap required** for penetration

### Rule 6: Joint Design
- **CJP** (Complete Joint Penetration) vs **PJP** (Partial Joint Penetration)
- **Fillet weld sizing** per AWS

### AWS Standards
- **D1.1:** Structural Welding Code - Steel
- **D1.2:** Structural Welding Code - Aluminum
- **D1.3:** Structural Welding Code - Sheet Steel
- **D1.6:** Structural Welding Code - Stainless Steel
- **A2.4:** Standard Symbols for Welding

---

## Cost Optimization Quick Reference

### Sheet Metal
- Use standard 0.5mm thickness increments
- Minimum hole 1.33T to enable punching (vs drilling +$0.50-$1.00/hole)
- Use Taptite extrusions instead of tapped holes
- Group features in single station for tighter tolerances

### CNC Machining
- Use standard hole sizes (3, 4, 5, 6, 8, 10, 12mm)
- Apply ±0.1mm standard tolerance, tight only where critical
- Design for ≤2 setups
- Add corner radii ≥1mm (avoids EDM)

### Die Casting
- Cast hole minimum 5mm (smaller → CNC)
- Avoid slides if possible (each adds 10% tool cost)
- Simple parting line saves $5K-$30K
- Use A380 for general parts, AlSi12(Fe) for thermal applications

### Injection Molding
- Choose material based on application + cost ratio
- Toolbound tolerances are 50% tighter than non-toolbound
- Uniform wall thickness prevents sink and warpage
- Minimize slides/lifters
