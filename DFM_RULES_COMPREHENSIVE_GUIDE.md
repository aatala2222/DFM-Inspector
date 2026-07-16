# DFM Rules Comprehensive Guide
## All Manufacturing Processes — Design for Manufacturability Reference

**Document:** DFM_RULES_COMPREHENSIVE_GUIDE  
**Source Specifications:** Process Specs folder (930-00163, 930-00164, 930-00166, 930-00172, 960-00169, CNC_Machining_DFM_Guidelines)  
**Processes Covered:** CNC Machining, Thermoplastic Injection Molding, Die Casting & Permanent Mold, Sheet Metal Fabrication, Weldments, Integral Skin PU Foam Molding

---

## Table of Contents

1. [CNC Machining](#1-cnc-machining)
2. [Thermoplastic Injection Molding](#2-thermoplastic-injection-molding)
3. [High Pressure Die Casting & Permanent Mold](#3-high-pressure-die-casting--permanent-mold)
4. [Sheet Metal Fabrication](#4-sheet-metal-fabrication)
5. [Weldments](#5-weldments)
6. [Integral Skin PU Foam Molding](#6-integral-skin-pu-foam-molding)

---

# 1. CNC Machining

**Source:** CNC_Machining_DFM_Guidelines.docx  
**Standards:** ISO 2768-mK, ASME Y14.5, ISO 1302, ISO 965, ISO 286

## 1.1 Tolerances

| Feature Type | Standard Tolerance | Precision Tolerance |
|---|---|---|
| General | ±0.1 mm (±0.005") | ±0.01–0.02 mm |
| Non-critical surfaces | ±0.1 mm | — |
| Shaft/hole fits | — | ±0.02 mm |
| Alignment features | ±0.05 mm | — |

- Limit tight tolerances to 5–10% of features; each tight feature adds 40–80% cost.
- Flag designs where >20% of features have tight tolerances.

## 1.2 Internal Corners and Radii

| Tool Diameter | Min Radius | Recommended Radius |
|---|---|---|
| 3 mm | 1.5 mm | 2.0 mm |
| 6 mm | 3.0 mm | 4.0 mm |
| 10 mm | 5.0 mm | 6.0 mm |
| 12 mm | 6.0 mm | 8.0 mm |

- Absolute minimum internal radius: 0.5 mm.
- Recommended: radius = 1/3 × pocket depth.
- Standard sizes: 0.5, 1.0, 3.0, 5.0 mm.
- Sharp corners require EDM (200–400% cost increase).

## 1.3 Wall Thickness

| Material | Absolute Min | Recommended |
|---|---|---|
| Aluminum 6061/7075 | 0.8 mm | 1.0 mm |
| Mild Steel | 1.0 mm | 1.5 mm |
| Stainless Steel 304/316 | 1.2 mm | 1.5 mm |
| Brass/Copper | 0.8 mm | 1.0 mm |
| Titanium | 1.5 mm | 2.0 mm |
| Engineering Plastics | 1.5 mm | 2.0 mm |

- Max aspect ratio (height:thickness): 4:1.
- Add ribs above 3:1 aspect ratio.
- Max thickness variation within same part: 50%.

## 1.4 Pockets and Cavities

- Max depth: 4× tool diameter (optimal: 2–3×).
- Error threshold: 6× tool diameter (requires custom tooling).

| Tool | Max Depth | Optimal Range |
|---|---|---|
| 3 mm | 12 mm | 6–9 mm |
| 6 mm | 24 mm | 12–18 mm |
| 10 mm | 40 mm | 20–30 mm |
| 12 mm | 48 mm | 24–36 mm |

## 1.5 Holes

- Use standard metric sizes: 3, 4, 5, 6, 8, 10, 12, 16, 20 mm.
- Max depth: 4× diameter (optimal: 2–3×, error: 5×).
- Min edge distance: 1.5× diameter.
- Min hole spacing: 2× diameter.
- Through holes preferred over blind holes.
- Limit unique hole sizes to 5 per part.

### Counterbore Rules

| Check | Requirement |
|---|---|
| Depth | ≤ 1.5 × bolt head height |
| Diameter | ≥ bolt head diameter + 0.5 mm |
| Wall thickness | ≥ 1.5 mm |
| Perpendicularity | ≤ 0.05 mm |

- Detected by: two distinct diameters, flat bottom, 90° wall angle.
- Machining: 2 operations (pilot hole + counterbore). Cost: moderate.
- Best for soft materials (aluminum, brass).

### Countersink Rules

| Check | Requirement |
|---|---|
| Angle | 82° (metric) or 90° (imperial), ±2° |
| Diameter | ≥ screw head diameter + 0.2 mm |
| Depth | = screw head height |
| Material thickness | ≥ 1.5 mm |

- Detected by: conical surface, no flat bottom, 82°/90° cone angle.
- Machining: 1 operation. Cost: low.
- Best for hard materials (steel).

## 1.6 Threads

- Standard metric: M2, M2.5, M3, M4, M5, M6, M8, M10, M12, M16, M20.
- Depth: 1.5× nominal diameter (standard), 1.0× (low-strength), 2.5× (max).
- Min wall thickness around thread: 2× thread diameter.
- Default tolerance: 6H (internal), 6g (external).

## 1.7 Surface Finish

| Finish | Ra (µm) | Application | Cost Multiplier |
|---|---|---|---|
| As machined | 3.2–6.3 | Functional parts | 1.0× |
| Fine machined | 1.6–3.2 | Moving assemblies | 1.2× |
| Bead blasted | 1.6–2.4 | Aesthetic surfaces | 1.3× |
| Anodized Type II | 0.8–1.6 | Corrosion protection (Al only) | 1.5× |
| Anodized Type III | 0.4–0.8 | Aerospace, wear (Al only) | 2.0× |
| Polished | 0.4–0.8 | Medical, decorative | 2.5–3.0× |

## 1.8 Setup Minimization

- Each setup adds 15–60 min and 30–40% cost.
- Alignment error per setup: ±0.02–0.05 mm.
- 3-axis: typically 2 setups (max recommended).
- 4-axis: typically 1 setup (1.3× cost multiplier).
- 5-axis: typically 1 setup (1.8–2.5× cost multiplier).

## 1.9 Tool Access

- Min channel width: 3× tool diameter (absolute), 4× (recommended), 5× (optimal).
- Line-of-sight access required.
- Add chamfer for entry (0.5–1.0 mm).
- Undercuts require special tools or 5-axis.

## 1.10 GD&T Achievable (3-Axis)

| Characteristic | Typical | Tight |
|---|---|---|
| Flatness | 0.05 mm/100mm | 0.01 mm |
| Perpendicularity | 0.05 mm | 0.02 mm |
| Parallelism | 0.05 mm | 0.02 mm |
| Position | 0.1 mm | 0.02 mm |
| Concentricity | 0.05 mm | 0.01 mm |

## 1.11 Material Machinability

| Material | Rating (1–5) | Relative Cost | Tool Wear |
|---|---|---|---|
| Aluminum 6061 | 5 | 1.0× | Low |
| Aluminum 7075 | 4 | 1.2× | Low |
| Brass | 4 | 1.5× | Very low |
| Mild Steel 1018 | 3 | 1.3× | Moderate |
| Stainless 304 | 2 | 2.0× | High |
| Stainless 316 | 2 | 2.2× | High |
| Titanium Grade 5 | 1 | 4.0× | Very high |
| Tool Steel | 1 | 3.5× | Very high |

## 1.12 Cost Optimization Summary

| Opportunity | Time Savings | Cost Reduction |
|---|---|---|
| Relax tolerances | 30–50% | 40–80% |
| Reduce setups | 20–40% | 30–40% |
| Add corner radii | 15–25% | 20–30% |
| Standardize holes | 10–20% | 15–25% |
| Simplify geometry | 20–40% | 25–40% |


---

# 2. Thermoplastic Injection Molding

**Source:** 930-00164_R01 Design Guideline — Thermoplastic Injection Molding  
**Process Owner:** Advanced Manufacturing Engineering

## 2.1 Wall Thickness

- Recommended range: 0.5–4.0 mm (typical).
- Keep walls as thin and uniform as possible.
- Where varying thickness is unavoidable, use gradual transitions.

**Impact of wall thickness:**
- Mold filling: too thin = incomplete fill.
- Part weight: thicker = heavier.
- Cooling time: thicker = longer cycle.
- Part cost: thicker = higher cost.
- Dimensional accuracy: non-uniform = warpage.
- Aesthetics: thick sections = sink marks; non-uniform = voids.

## 2.2 Draft Angle

| Condition | Minimum Draft |
|---|---|
| Untextured surfaces | 0.5° |
| General recommendation | 1–3° |
| Textured surfaces | Add 0.4–0.5° per 0.1 mm texture depth |
| Shut-off surfaces (stepped parting) | 7° minimum (5° absolute minimum) |

- Without draft: friction causes scratches, gouges, and texture damage during ejection.
- Higher shrinkage materials need larger draft.
- Taller features need more draft.

## 2.3 Radii and Chamfers

- Inner corner radius: 25–60% of nominal wall thickness.
- Minimum inner radius: 0.5 mm.
- Outer radius = inner radius + wall thickness (for uniform wall).
- All sharp outer edges: break with at least 0.125 mm radius.
- Stress concentration factor: ~1.5 at 50% wall radius; ~3.0 at 10% wall radius.

## 2.4 Parting Line

Five types:
1. Vertical (most common, perpendicular to mold opening).
2. Stepped (requires pins to support unbalanced force).
3. Beveled (beveled shape transition).
4. Curved (curved shape transition).
5. Comprehensive (combination of all forms).

- Parting line is always visible; minimize by location, draft, and geometry.
- Keep as simple as possible to reduce tooling cost.

## 2.5 Undercuts

- Undercuts require slides and lifter mechanisms.
- Always add cost, complexity, and maintenance.
- Redesign to eliminate undercuts when possible.
- Straight-pull mold (no undercuts) is lowest cost.

## 2.6 Ribs

| Parameter | Rule |
|---|---|
| Thickness | 50–60% of wall thickness |
| Height | ≤ 3× wall thickness |
| Draft on sides | 1–1.5° |
| Base radius | 25–50% of wall thickness (min 0.4 mm) |
| Spacing | ≥ 2× wall thickness |

- Orient ribs parallel to melt flow.
- Orient along axis of bending for maximum stiffness.
- Exceeding thickness ratio causes sink marks on opposite surface.

## 2.7 Gussets

- Subset of ribs; same dimensioning and placement rules apply.
- Used to reinforce corners, side walls, and bosses.

## 2.8 Bosses

| Parameter | Rule |
|---|---|
| Wall thickness | < 50% of general wall thickness |
| Base radius | 25% of wall thickness or 0.4 mm |
| Outer draft | ≥ 0.5° |
| Inner draft (tubular) | ≥ 0.25° |
| Distance from external wall | ≥ 3 mm |
| Spacing between bosses | ≥ 2× wall thickness |
| Max aspect ratio (height:width) | 3:1 |

- Extend core pin slightly through wall to reduce sink marks.
- Add gussets or connect to sidewall for strength.

## 2.9 Gate Types

**Manually trimmed:** Sprue, Edge/Side, Tab, Overlap, Film/Flash, Diaphragm, External Ring, Internal Ring.

**Automatically trimmed:** Pin (3-plate only), Submarine/Tunnel, Cashew, Hot Runner, Valve.

**Selection factors:**
- Part geometry and mold design.
- Material sensitivity to shear heating.
- Gate freeze timing.
- Production volume (auto-trim for high volume).
- Scrap cost (hot runner = zero scrap).

## 2.10 Mold Types

| Type | Use Case |
|---|---|
| Two-plate | Most common, single parting plane |
| Three-plate | Automatic degating, separate runner ejection |
| Hot runner | Zero scrap, high volume |
| Cold runner | Lower tooling cost, runner ejected each cycle |
| Single cavity | Low volume, lower tooling cost |
| Multiple cavity | High volume, lower unit cost |
| Family mold | Multiple different parts, same material |

## 2.11 Tolerances

| Feature Size | Toolbound Commercial | Toolbound Fine | Non-Toolbound Commercial | Non-Toolbound Fine |
|---|---|---|---|---|
| 0–10 mm | ±0.100 | ±0.050 | ±0.200 | ±0.100 |
| 10.1–25 mm | ±0.125 | ±0.075 | ±0.225 | ±0.125 |
| 25.1–50 mm | ±0.150 | ±0.100 | ±0.250 | ±0.150 |
| 50.1–75 mm | ±0.200 | ±0.125 | ±0.300 | ±0.175 |
| 75.1–100 mm | ±0.225 | ±0.150 | ±0.350 | ±0.200 |
| 100.1–150 mm | ±0.250 | ±0.175 | ±0.400 | ±0.225 |
| 150.1–200 mm | ±0.500 | ±0.275 | ±0.600 | ±0.325 |
| 200.1–250 mm | ±0.650 | ±0.375 | ±0.750 | ±0.425 |
| 250.1–300 mm | ±0.800 | ±0.475 | ±0.900 | ±0.525 |
| 300.1–350 mm | ±0.950 | ±0.575 | ±1.050 | ±0.625 |
| 350.1–400 mm | ±1.100 | ±0.675 | ±1.200 | ±0.725 |
| 400.1–450 mm | ±1.250 | ±0.775 | ±1.350 | ±0.825 |

*All values in mm. Toolbound = single side of tool. Non-Toolbound = across moving sections (parting line, lifter, slide, cavity to core).*

## 2.12 Surface Finishes (SPI Standards)

| Standard | Ra (µm) | Method | Look |
|---|---|---|---|
| A-1 | 0.012–0.025 | 6000 Grit Diamond | Super High Glossy |
| A-2 | 0.012–0.025 | 3000 Grit Diamond | High Glossy |
| A-3 | 0.05–0.10 | 1200 Grit Diamond | Normal Glossy |
| B-1 | 0.05–0.10 | 600 Grit Paper | Fine Semi-glossy |
| B-2 | 0.10–0.15 | 400 Grit Paper | Medium Semi-glossy |
| B-3 | 0.28–0.32 | 320 Grit Paper | Normal Semi-glossy |
| C-1 | 0.35–0.40 | 600 Grit Stone | Fine Matte |
| C-2 | 0.45–0.55 | 400 Grit Stone | Medium Matte |
| C-3 | 0.63–0.70 | 320 Grit Stone | Normal Matte |
| D-1 | 0.80–1.00 | Dry Blast Glass Bead | Satin Textured |
| D-2 | 1.00–2.80 | Dry Blast #240 Oxide | Dull Textured |
| D-3 | 3.20–18.0 | Dry Blast #24 Oxide | Rough Textured |

Other methods: EDM Spark Erosion, Media Blasting, Chemical Photoetching, Laser Etching.

## 2.13 Injection Molding Process Variants

- **Gas Assisted:** Nitrogen gas displaces 20–30% of plastic. Creates hollow, lightweight parts. Lower clamp tonnage.
- **Over Molding / Insert Molding:** Mold one material over another (e.g., TPE over plastic or metal insert).
- **Film Insert Molding (IMD/IML):** Mold plastic over decorated film.
- **Double Injection (2-shot):** Two different materials in one cycle using rotating mold.

## 2.14 Design Checklist

- Wall thickness 0.5–4 mm, as thin and uniform as possible.
- Draft 1–3° (0.5° min untextured, add for texture).
- Inner radius ≥ 0.5 mm (25–60% of wall).
- Outer radius = inner + wall thickness.
- Parting line as simple as possible.
- Avoid undercuts or use slides.
- Ribs: 50–60% wall thickness, ≤ 3× height.
- Bosses: < 50% wall thickness, ≥ 3 mm from walls.
- Gate type and location optimized.
- Mold flow analysis completed.
- Supplier DFM review completed.


---

# 3. High Pressure Die Casting & Permanent Mold

**Source:** 930-00166_R01 Design Guideline — High Pressure Die Cast and Gravity Cast Permanent Mold
**Process Owner:** Advanced Manufacturing Engineering
**Standards:** NADCA Product Specification Standards 11th Edition, Aluminum Association Standards 16th Edition

## 3.1 Process Selection: HPDC vs Permanent Mold

| Attribute | HPDC | Permanent Mold |
|---|---|---|
| Profile Tolerance | 0.5–1.5 mm (same side) | 2.6–3.6 mm (across parting line) |
| Dimensional Tolerance | 0.002 mm/mm of length | 0.38 mm + 0.002 mm/mm |
| Across Parting Line | +0.25 mm additional | +0.76–1.0 mm additional |
| Part Strength (as-cast) | 30–50% stronger than gravity | Lower; heat treatment closes gap to ~5–10% |
| Surface Finish | 60–120 RMS | 250–420 RMS |
| Draft Requirement | 1–1.5° | 1–3° or more |
| Min Wall Thickness | 3–10 mm | 4 mm and thicker |
| Max Part Size | ~5500 cm² projected area (4400-ton press) | No press-size limit |
| Cycle Time | 60–100 seconds | 240–280 seconds |
| Tooling Cost | $15K–$300K+ | $10K–$60K+ |
| Sample Leadtime | 12–26 weeks | 12–16 weeks |
| Production Leadtime | 3–6 weeks after approval | 3–6 weeks after approval |
| Tool Life | 100K shots (capped) | 60K shots |

**Selection guidance:**
- HPDC: Higher volumes (>10K/year), tighter tolerances, better surface finish, smaller parts.
- Permanent Mold: Large/thick parts, lower volumes (1K–10K/year), lower tooling investment.
- Permanent Mold cost-effective at as low as 1,000 pieces/year depending on complexity.

## 3.2 Wall Thickness

| Process | Nominal Min | Min Feature Thickness | Preferred |
|---|---|---|---|
| HPDC | 3 mm | 2.0 mm | 4 mm+ |
| Permanent Mold | 4 mm | 3–4 mm (supplier feedback) | 5 mm+ |

- Maintain uniform wall thickness for good material flow and part fill.
- Avoid abrupt thickness transitions — causes turbulence, pressure changes, and porosity.
- Thick sections susceptible to shrink porosity in HPDC (air bubbles form as material cools/contracts).
- Hanging/isolated features should be bridged with material to adjacent features to promote flow and eliminate thin mold steel areas.

## 3.3 Draft Angle

| Process | Minimum Draft | Notes |
|---|---|---|
| HPDC | 1.5° | More or less may be required per supplier DFM |
| Permanent Mold | 3.0° | Higher draft needed to reduce sticking risk |

- Without draft, friction causes part warpage or breakage during ejection.
- Draft is critical: affects wall thickness and mating interfaces.
- For truly vertical walls: post-CNC machining (interior) or slides/side action (exterior).

## 3.4 Corner Radii and Fillets

- Minimum inside radius: 0.5 mm (any radius is better than sharp).
- External radius = inside radius + wall thickness (maintains uniform wall).
- Sharp corners in mold are impossible to maintain over tool life.
- Sharp inside corners are stress concentrators in both part and mold.
- Exception: edges at parting line (or where mold halves meet) shall NOT have radii unless function requires it.

## 3.5 Parting Lines

- Parting line = separation perimeter of the two mold halves.
- Defines the draft plane — must be carefully considered during design.
- Keep as simple as possible:
  - Simplified tooling (lower cost and leadtime).
  - Easier trim die design (gates/vents are at parting line).
  - Better tool life, fit, and finish.

## 3.6 Undercuts and Zero-Draft Conditions

Undercuts are features that cannot be manufactured with a simple two-part mold.

**Handling options:**
1. Side action/slides: ~10% tooling cost increase. Tolerance uses "across parting line" values.
2. Post-casting CNC: Compare cost vs. slide option.
3. Ejection lifter or pass core: Not common; consult supplier.

**Side action considerations:**
- Impacts tooling cost and leadtime.
- Tolerance is looser (fixed steel to movable steel).
- Always compare slide cost vs. CNC cost.

## 3.7 Machining Stock Allowance

| Process | Machining Stock | Notes |
|---|---|---|
| HPDC | 1 mm over-cast | Do NOT add excess — deeper machining risks hitting porosity |
| Permanent Mold | 1.5–2 mm over-cast | Less porosity risk, but excess material increases CNC time |

- Air cuts can be specified at maximum material condition to mitigate profile tolerance issues from tool wear.

## 3.8 Minimum Feature Sizes

| Feature | HPDC | Permanent Mold |
|---|---|---|
| Min mold steel thickness | 3 mm | 6 mm (at 20 mm height); ~1:3 width:height ratio |
| Min as-cast hole diameter | 5 mm (smaller = post-CNC) | Supplier-dependent (depth/draw angle) |
| Heat sink fin pitch | 2.5 mm top + 3 mm gap + draft | 3 mm top + 4 mm gap + draft |

- Ejector pin pads may be needed on parts without large flat areas orthogonal to ejection direction.
- Unusual geometry (flat sections without ribbing, large asymmetry) should be flagged for early DFM — higher warp propensity.

## 3.9 Gates and Vents/Risers

**Die Casting:**
- Gate location sets material flow direction (least resistance to fill).
- Venting promotes fill and steers material flow.
- Impediments to flow: thickness changes, holes, features orthogonal to fill direction.
- Mitigation: feeder ribs in flow direction; material bridges across holes (machined out later).

**Permanent Mold:**
- Gravity-fed: larger gates and risers, fewer risers than HPDC.
- Part orientation and gate location optimized to eliminate trapped air.
- Risers allow air escape and overflow for complete fill.

## 3.10 Tolerances

**Linear tolerance on one side of mold:**

| Dimension | Perm Mold | HPDC Standard | HPDC Precision |
|---|---|---|---|
| Basic (up to 25 mm) | ±0.38 mm | ±0.25 mm | ±0.05 mm |
| Each additional 25 mm | ±0.051 mm | ±0.025 mm | ±0.025 mm |

**Tolerance categories (NADCA):** Linear, Parting Line, Moving Die Component, Angularity, Concentricity, Parting Line Shift, Draft, Flatness.

**Tolerance categories (Perm Mold):** Linear, Parting Line, Side Core, Flatness, Profile.

- Higher precision = higher cost (shorter production runs, more die maintenance).
- Design to industry-published tolerances for supplier flexibility.

## 3.11 Datum Strategy

- Cast datums on same side of die half (cavity or core).
- Choose die half with most functional requirements or mating features.
- Avoid datums on: ejector pins, areas near parting lines, vents, gates.
- Select datum features that will NOT be machined (maintains traceability).
- Add flat pads on non-orthogonal surfaces if possible.
- Keep cast datums on the part itself, not on tabs that will be machined off.

## 3.12 Materials

| Process | Primary Alloy | Notes |
|---|---|---|
| HPDC | A380 | General purpose, majority of castings |
| HPDC | AlSi12(Fe) | ~30% better thermal conductivity, minor property sacrifice |
| Permanent Mold | 319.0 | Primary alloy for perm mold parts |

- Not suitable for iron, steel, or stainless steel.
- Magnesium and zinc possible but require separate investigation.

## 3.13 Finishes

| Finish | Cosmetics | Cost | Electrically Conductive? | Corrosion Protection? | Apply Pre-CNC? |
|---|---|---|---|---|---|
| Raw Casting | As-cast, not great | None | Yes (oxidation risk) | No | N/A |
| Chromate Conversion | Not cosmetic | $ | Configurable | Yes | Yes (if CNC surfaces don't need finish) |
| E-coat | Semi-uniform | $ | No | Yes | Typically post-CNC |
| Anodize | Good (heavier coat) | $$ | No usually | Yes | Yes (if CNC surfaces don't need finish) |
| Powder Coat | Very good | $ | No | Yes | Yes (robust enough pre-CNC) |

## 3.14 Cost Drivers

**Tooling cost factors:**
- HPDC tooling > Permanent Mold tooling (cost and leadtime).
- Complex parting lines, side action/slides increase cost and maintenance.
- Each machining setup requires a unique fixture.

**Piece part cost factors:**
- Material alloy cost (A380 vs AlSi12Fe negligible delta).
- Cycle time (HPDC faster = lower piece part cost).
- Automation level (HPDC more automatable).
- Part size (larger = more material, slower cycles).
- Machining operations and total machining time.
- Finishing process and masking requirements.

## 3.15 Design Checklist

- Process selected (HPDC vs Permanent Mold).
- Part size within process capability.
- Wall thickness within process limits (uniform).
- Draft angle meets minimum (1.5° HPDC, 3° Perm Mold).
- Inside radius ≥ 0.5 mm; external = inside + wall.
- Parting line as simple as possible.
- Gates and vents at parting line.
- Undercuts minimized or eliminated.
- Machining stock allowance included (1 mm HPDC, 1.5–2 mm Perm Mold).
- Hole sizes achievable with process.
- Mold steel thickness adequate.
- Datum strategy on one side of die half.
- Surface finish and tolerances specified.
- Supplier DFM review completed.


---

# 4. Sheet Metal Fabrication

**Source:** 930-00172_R01 Design Guideline — Sheet Metal Best Practices
**Process Owner:** Hardware Engineering

## 4.1 Fabrication Processes

### Soft Tooling (Prototypes / Alpha Builds)

| Process | Strengths | Limitations |
|---|---|---|
| Turret Press | Flexible for holes and shallow forms; 80–300 hits/min; inexpensive custom tooling | Flat forms only; limited thickness; higher part cost vs progressive |
| Laser Cutting | No tooling; complex geometry; high accuracy; small kerf; engraving capable | 2D profiles only; operator-dependent; edge quality degrades with thickness |
| Hand Press Brake | Flexible; low cost tooling; low lead time; high material versatility | Highly manual; lower accuracy; operator-dependent; complex parts = multiple ops |

### Hard Tooling (Beta / Production)

| Process | Strengths | Limitations |
|---|---|---|
| Single Stage / Transfer Die | Cost-effective; easy setup; long lifespan; quick ROI | Slower production rate; one step at a time; die replacement per operation |
| Progressive Die | Automated; minimal scrap; tight tolerances; scales to long runs; reduced labor | Higher tooling cost; precision alignment needed; coil feeder required |
| Multi-Slide | Complex small parts; multiple bends; high repeatability; minimal scrap | Higher tooling cost; precision alignment; coil feeder needed |
| Fine Blanking | Extremely flat; smooth edges; ±0.03 mm accuracy; eliminates secondary ops; up to 17 mm thick | Slower; higher equipment investment |

## 4.2 Process Capabilities / Tolerances

### Turret Press

| Description | Tolerance |
|---|---|
| Feature to feature | ±0.10 mm (±0.004") |
| Punched feature size | ±0.10 mm (±0.004") |
| Feature with multiple hits | ±0.20 mm (±0.008") |
| Feature to edge | 1.33T |

### Laser Cutting

| Description | Tolerance |
|---|---|
| Feature to feature | ±0.10 mm (±0.004") |
| Feature to edge | ±0.10 mm (±0.004"), 1.33T |
| Minimum kerf | ±0.2 mm (±0.008") |
| Minimum feature size | 0.25T (25% material thickness) |

### Hand Brake Press

| Description | Tolerance |
|---|---|
| Fold to fold | ±0.5 mm (±0.020") |
| Fold to feature or edge | ±0.4 mm (±0.015") |
| Bend angle | ±1.5° |
| Minimum radius | 1.33T |

### Progressive Die

| Description | Tolerance | Fine Tolerance |
|---|---|---|
| Features same station | ±0.05 mm (±0.002") | — |
| Features different stations | ±0.2 mm (±0.008") | — |
| Folds same station | ±0.2 mm (±0.008") | — |
| Folds different stations | ±0.4 mm (±0.016") | ±0.3 mm (±0.012") |
| Fold to feature or edge | ±0.25 mm (±0.010") | ±0.1 mm (±0.004") |
| Bend angle | ±1° | — |
| Min hole diameter / slot width | 1.33T | — |
| Hole or feature size | ±0.08 mm (±0.003") | ±0.03 mm (±0.001") |
| Flatness | 0.15/100 mm (0.006"/4") | — |
| Straightness | 0.12/100 mm (0.005"/4") | — |

### Multi-Slide

| Description | Tolerance |
|---|---|
| Features distance | ±0.05 mm (±0.002") |
| Folds distance | ±0.15 mm (±0.006") |
| Fold to feature or edge | ±0.15 mm (±0.006") |
| Bend angle | ±1° |
| Min hole diameter / slot width | 1.33T |
| Hole or feature size | ±0.05 mm (±0.002") |
| Flatness | 0.15/100 mm |
| Straightness | 0.12/100 mm |

### Fine Blanking

| Description | Tolerance |
|---|---|
| Features distance | ±0.03 mm (±0.001") |
| Hole or feature size | ±0.02 mm (±0.001") |
| Min hole diameter / slot width (steel) | 0.8T |
| Min hole diameter / slot width (stainless) | 1.0T |
| Flatness | 1.0T |

## 4.3 Shear Mechanics

**Bending methods:**
- Bottoming: Sheet compressed to die bottom; no spring-back; material thinned at bend base.
- Coining: High precision; no spring-back; dent created like a coin.
- Air Bending: Sheet does not contact die bottom; prone to spring-back; less accurate.
- Roll Bending: Three rollers create curves/tubes/cones.
- Wipe Bending: Fastest method; risk of surface scratches.
- Rotary Bending: No surface scratching; can bend sharp corners >90°.

## 4.4 Materials

### Steel Specifications

| Code | Description |
|---|---|
| SPCC | Commercial grade basic CRS, general use, dead mild steel |
| SPCD | Drawing quality CRS, general use |
| SPCE | Deep drawing quality CRS |
| SECC | Commercial stamping grade CRS, electro-galvanized zinc |
| SECD | Drawing grade CRS, electro-galvanized zinc |
| SECE | Drawing grade CRS, electro-galvanized zinc, improved thermal conduction |
| SGCC | Commercial grade CRS, hot-dipped galvanized |
| SGCD | Drawing grade CRS, hot-dipped galvanized |
| SPTE | Thin low-carbon, tin plated (canning industry) |

### Material Thickness Tolerances — Stainless Steel

| Thickness (mm) | Tolerance |
|---|---|
| 0.6–0.79 | ±0.05 mm |
| 0.80–0.99 | ±0.055 mm |
| 1.0–1.19 | ±0.06 mm |
| 1.20–1.49 | ±0.07 mm |
| 1.50–1.99 | ±0.08 mm |
| 2.0–2.49 | ±0.09 mm |
| 2.5–2.99 | ±0.11 mm |
| 3.0 | ±0.13 mm |

### Material Thickness Tolerances — SGCC Steel (Hot-Dipped Galvanized)

| Thickness (mm) | Tolerance |
|---|---|
| 0.40–0.60 | ±0.05 mm |
| 0.61–0.80 | ±0.06 mm |
| 0.81–1.00 | ±0.07 mm |
| 1.01–1.20 | ±0.08 mm |
| 1.21–1.60 | ±0.11 mm |
| 1.61–2.00 | ±0.14 mm |
| 2.01–2.50 | ±0.16 mm |
| 2.51–3.00 | ±0.19 mm |

### Material Thickness Tolerances — SECC Steel (Electro-Galvanized)

| Thickness (mm) | Tolerance |
|---|---|
| 0.40–0.60 | ±0.03 mm |
| 0.61–0.80 | ±0.04 mm |
| 0.81–1.00 | ±0.05 mm |
| 1.01–1.20 | ±0.06 mm |
| 1.21–1.60 | ±0.08 mm |
| 1.61–2.00 | ±0.10 mm |

### Material Thickness Tolerances — Aluminum

| Thickness (mm) | Group I | Group II |
|---|---|---|
| 0.6–0.80 | ±0.03 mm | ±0.04 mm |
| 0.81–1.00 | ±0.04 mm | ±0.05 mm |
| 1.01–1.20 | ±0.04 mm | ±0.05 mm |
| 1.21–1.50 | ±0.05 mm | ±0.07 mm |
| 1.51–1.80 | ±0.06 mm | ±0.08 mm |
| 2.01–2.50 | ±0.07 mm | ±0.10 mm |
| 2.51–3.00 | ±0.08 mm | ±0.11 mm |
| 3.01–3.50 | ±0.10 mm | ±0.12 mm |

*Group I: 1000, 3000, 4006, 4007, 5005, 5050, 8011A series. Group II: 2000, 6000, 7000, 3004, 5040, 5049, 5251, 5052, 5154A, 5454, 5754, 5182, 5083, 5086 series.*

### US Gage to Metric Conversion

| Gage | mm | inches |
|---|---|---|
| 26 | 0.455 | 0.0179 |
| 24 | 0.607 | 0.0239 |
| 22 | 0.759 | 0.0299 |
| 20 | 0.912 | 0.0359 |
| 18 | 1.214 | 0.0478 |
| 16 | 1.519 | 0.0598 |
| 14 | 1.897 | 0.0747 |

### Normalized Material Cost

| Material | Normalized Cost |
|---|---|
| Cold Rolled Steel | 1.0× |
| Steel EG | 1.2× |
| Aluminum | 3.0× |
| Stainless Steel | 6.0× |
| Copper/Brass | 10.0× |

## 4.5 DFX Design Guidelines

### General Feature Rules (T = material thickness, R = bend radius)

| Parameter | Rule |
|---|---|
| Max hole size (A) | 2B or 6T |
| Min hole diameter (B) | 1.33T |
| Min hole spacing (C) | 2T |
| Min hole to edge (D) | = C |
| Min inside radius (R1) | 0.5T or 0.4 mm |
| Min outside radius (R2) | 0.5T or 0.4 mm |

### Feature-to-Bend Rules

| Parameter | Rule |
|---|---|
| Min flange height (A) | 2.0T |
| Min feature to bend (B) | 2.0T |
| Max flange when A = min (C) | 50 mm |
| Min flange (C) | 2R + T |
| Min feature spacing (D) | 2T |
| Min hole to edge (E) | 1.2T |
| Min feature to bend (F) | 3T (if C ≤ 10T), 4T (if C > 10T) |

### Hole Distance from Bend

| Parameter | Rule |
|---|---|
| Minimum (A) | 2.0T + R |
| Recommended (B) | 3T + R |
| Min bend radius (R) | 1.0T or 0.6 mm minimum |

### Slot Distance from Bend

| Slot Length | Minimum Distance |
|---|---|
| L < 50 mm | 3T + R |
| L > 50 mm | 4T + R |

### Bend Radius

- Minimum: 1.0T or 0.6 mm (whichever is greater).
- Low carbon steel only: R min = 0.5T.

### Bend Relief

- Required when bend is close to an edge — prevents tearing.
- Relief depth > bend radius.
- Relief width ≥ material thickness.
- Punched slot in bend allows holes closer to fold without deformation.

### Z Bends

- H ≤ 5T for 90° offset.
- R = 1.5T for 90° offset.
- R = 0.2 mm for 45° offset.

### Hems

- Used to hide burrs (not improve flatness).
- Requires multiple steps (acute angle bend + flattening).
- Tear drop is most common type.
- Min return flange height: 4T.
- Min distance from hole: 2T.
- Min distance from internal bend: 5T.
- Min distance from external bend: 8T.
- Flat hems tend to fracture and cause fluid entrapment.

### Extrusions

| Parameter | Rule |
|---|---|
| Min distance between extrusions | 6T |
| Min distance to edge | 3T + 2R |
| Min distance to bend | 3T + R |
| Min height for M3 screw | 2.0T–2.5T |
| Min height for M4 screw | 2.5T–3.0T |

*Minimum 4 threads of engagement (~80% strength).*

### Half Shear

- Max height of single shear: 0.5T.
- Min width/diameter of feature: 2T.
- Multiple shears can exceed 0.5T total height.

### Dimples

| Parameter | Rule |
|---|---|
| Max diameter (D) | 6T |
| Max height (H) | 4T |
| Min height (H) | D × 0.3 |
| Min distance to hole | 3T |
| Min distance between dimples | 4T + D |
| Min distance to bend | 2T |
| Min distance to edge (P) | 3T + D/2 |
| Min angle (Z) | ≥ 30° |

### Embossments / Stiffening Ribs

**Round:** Max height H = 3T, Min width W = 3T.
**V embossment:** Max height H = 3T, Min width W = 3H.
**Flat:** Max depth = internal radius + external radius.

| Parameter | Rule |
|---|---|
| Min distance between parallel embossments | 10T |
| Min distance to edge | 4T |
| Min distance to hole | 3T |
| Min distance to fold (D) | 4T |

### Louvers

- Min radius R > H (louver height).

### Lance and Form

| Parameter | Rule |
|---|---|
| Min height (H) | 2T |
| Min distance to fold | 3T + R |
| Min distance to hole | 3T |
| Min web distance between lances | 6T |
| Bend relief | Not required |

### Lance Bridges

| Parameter | Rule |
|---|---|
| Min height | 2T |
| Max height | 5T |
| Min distance to fold | 3T + R (recommended 8T) |
| Min distance to hole | 3T |
| Bend relief | Not required |

## 4.6 Joining Techniques

| Technique | Pros | Cons |
|---|---|---|
| Blind Rivets | One-side install; portable; fast; dissimilar materials | Inconsistent back-side cinch; low vibration resistance |
| Hollow Rivets | Low cost; low profile; dissimilar materials | Back-side access required; higher install cost |
| Solid Rivets | Highest strength; low cost; dissimilar materials | Back-side access; loud impact process |
| Orbital Riveting | Tight joints; highly controlled; vibration resistant | Both-side access; 2–15 sec cycle time |
| Spot Welding | Thin materials; dissimilar materials; no fillers; high control | Thermal HAZ; secondary corrosion process needed |
| Projection Spot Welding | Less current than spot; multiple welds per op; not thickness-sensitive | Requires formed projections; tighter process control |
| Laser Spot Welding | Small puddle; no filler; min HAZ; complex geometry | Fixtures required; small nugget; skilled labor |
| Tox / Tog-L-Loc | No heat; 30–60% savings vs spot weld; dissimilar materials; coating intact | High positional variation without tooling |
| Extrude and Flare | No added material; mechanical interlock; good alignment | Limited flare contact |
| Tab and Fold | No fasteners; low cost; dissimilar thickness | Requires tooling; limited joint strength |
| Tab and Screw | ~80% strength if L > D; temporary; blind joint; high reliability | Requires threaded hole or insert; additional parts |

## 4.7 Secondary Operations Minimization

| Secondary Operation | Alternative |
|---|---|
| Tapped hole | Extruded hole + Taptite |
| Threaded hardware | Extruded hole + Taptite |
| Spacers | Bridge feature or emboss |
| Standoffs | Bridge feature or emboss |
| Spot welds | Tox / Tog-L-Loc / Swaging |
| Rivets | Tox / Tog-L-Loc / Swaging |
| Screws | Tox / Tog-L-Loc / Swaging |

## 4.8 Design Checklist

- Specify punch direction and grain direction.
- Specify areas needing deburring or coining.
- Identify features grouped in single station for best tolerancing.
- Avoid secondary operations if possible.
- Keep embosses and draws shallow.
- Use standard, readily available, precoated materials.
- Review design for handling and shipping damage.
- Review strip layout before releasing hard tooling.
- Add tooling holes for consistent reference features.
- Specify acceptable carrier tab locations.
- Datum structure aligns with part use and function.
- GD&T clearly defines features.
- Process control dimensions measurable at press with simple tools.
- Use sheared edges for critical reference features.
- Define max and min bend radius.
- Design inspection fixtures in parallel with part design.
- Clearly specify critical and major dimensions.


---

# 5. Weldments

**Source:** 960-00169_R01 Design Guideline — Weldments (Welding Fundamentals & AWS Basics)
**Process Owner:** Advanced Manufacturing Engineering
**Standards:** AWS A3.0M/A3.0:2010, AWS A2.4:2012, AWS D1.1/D1.2/D1.3/D1.6

## 5.1 Welding Processes

| Process | Full Name | Typical Use |
|---|---|---|
| GMAW (MIG) | Gas Metal Arc Welding | General purpose, high volume, thick materials |
| GTAW (TIG) | Gas Tungsten Arc Welding | Precision, thin materials, aluminum |
| RSW | Resistance Spot Welding | Sheet metal assembly, fast cycle, minimal distortion |

## 5.2 Weld Joint Types

**By configuration:** Butt, T-joint, Lap, Corner, Edge.

**By penetration:**
- Complete Joint Penetration (CJP): Weld metal extends through full joint thickness.
- Partial Joint Penetration (PJP): Incomplete joint penetration exists.

**By accessibility:** Flat, Horizontal, Vertical, Overhead (affects difficulty and quality).

## 5.3 Parts of a Weld

| Term | Definition |
|---|---|
| Theoretical Throat | Distance from joint root perpendicular to hypotenuse of largest inscribed right triangle (assumes zero gap) |
| Actual Throat | Shortest distance between weld root and face of fillet weld |
| Effective Throat | Minimum distance from fillet weld face (minus convexity) to weld root |
| Leg / Size | Length of the sides of the fillet weld triangle |
| Weld Metal Zone | The deposited filler material |
| Heat-Affected Zone (HAZ) | Base metal altered by welding heat |
| Base Metal | Unaffected parent material |

- For 45° fillet: Effective throat ≈ 0.707 × leg size.

## 5.4 Welding Symbolization (AWS A2.4:2012)

**Standard elements:** Reference line, arrow, basic weld symbol, dimensions, supplementary symbols, tail (for specifications).

**Weld symbols:** Fillet, Groove (V, Bevel, U, J, Flare-V, Flare-Bevel), Plug, Slot.

**Key rules:**
- Symbols denote continuous welds unless otherwise indicated.
- Symbols apply only between changes in welding direction (except weld-all-around symbol).
- Weld-all-around symbol: continuous weld extending around a series of connected joints (may involve different directions and planes).
- Circumferential joints do NOT require weld-all-around symbol.

## 5.5 AWS Welding Standards

| Standard | Applicable To | Key Sections |
|---|---|---|
| AWS D1.1 | Carbon/low alloy steels, ≥3 mm thick, ≤100 ksi yield | Design (§2), Qualification (§4), Fabrication (§5), Inspection (§6) |
| AWS D1.2 | Aluminum structural alloys (excludes pressure vessels/piping) | Design (§2), Qualification (§3), Fabrication (§4), Inspection (§5) |
| AWS D1.3 | Sheet steels <5 mm, HSS <3 mm wall, ≤80 ksi yield | Design (§2), Qualification (§4), Fabrication (§5), Inspection (§6) |
| AWS D1.6 | Stainless steel (at least one material), ≥1.5 mm thick | Design (§4), Qualification (§6), Fabrication (§7), Inspection (§8) |

**Tip:** When only WPS/welder qualification is needed, drawings may note: "Welding procedure specifications and welding personal performance qualification per AWS D1.x as applicable."

## 5.6 Welding Qualification

| Document | Purpose |
|---|---|
| WPS (Welding Procedure Specification) | Written "recipe" specifying all essential variables for quality welds |
| PQR (Procedure Qualification Record) | Documents successful qualification testing with real test conditions |
| WPQR (Welder Performance Qualification Record) | Certifies individual welder's ability to produce conforming welds |

**Essential variables include:** Base metal thickness/type/grade, filler material type/diameter, welding position, groove angle, root opening, preheat/interpass temperature, welding speed/amperage, heat input, post-weld heat treatment.

## 5.7 Groove Angle Requirements

| Material | Groove Angle Range | Recommended |
|---|---|---|
| Carbon Steel | 50°–60° | 55° |
| Aluminum | 60°–65° | 62° |
| Stainless Steel | 55°–60° | 57° |

## 5.8 Root Opening and Root Face

- Root opening affects fusion, penetration, and weld pool control.
- Root face requirements:
  - Bevel angle ≤ 30°: Root face = 0 (not required).
  - Bevel angle > 30°: Root face minimum = 0.040" (1 mm).
  - Root face aligned with contact surface.

## 5.9 Skewed Joint Configuration

Skewed joints involve non-perpendicular part angles:
- ψ = angle between parts
- β = inclination angle
- α = bevel angle
- γ = groove angle
- Relations: β = 90° − ψ, γ = α − β

**Beveling rules:**
- Inclination angle < 10°: Beveling NOT mandatory; use fillet weld symbol.
- Inclination angle ≥ 10°: Beveling IS mandatory; bevel angle must ensure groove angle requirement.
- Beveling recommended only on the obtuse side.

**Obtuse side weld symbols:**
- Large α: Reinforcing fillet weld may be added.
- Weld face in plane of skewed part: Use bevel weld symbol.
- α ≈ 30°, γ ≈ 60°: Use fillet weld.

**Acute side weld symbols:**
- ψ = 60°–90°: Fillet weld.
- ψ = 40°–60°: V-groove weld with "W = (value)".
- ψ = 30°–40°: Not recommended; welding tests needed.

## 5.10 Weld Discontinuities

| Discontinuity | Description | Impact |
|---|---|---|
| Porosity | Gas entrapment cavities during solidification | Reduced strength and ductility |
| Undercut | Groove melted into base metal at weld toe, left unfilled | Stress concentration, fatigue failure |
| Overlap | Weld metal protrusion beyond weld toe or root | Poor fusion, stress concentration |
| Underfill | Weld face/root below adjacent base metal surface | Reduced cross-section |
| Excessive Convexity | Excessive reinforcement on fillet weld | Can be detrimental despite appearing "strong" |
| Incorrect Weld Size | Weld too big or too small | Structural inadequacy or excess cost |
| Incomplete Fusion (LOF) | No fusion between weld metal and base metal | Joint failure |
| Incomplete Penetration (LOP) | Weld metal doesn't extend through joint thickness | Joint failure |
| Inclusion | Entrapped slag, flux, tungsten, or oxide | Reduced strength |
| Crack | Fracture-type discontinuity with sharp tip | Most serious — immediate failure risk |
| Spatter | Metal particles expelled during welding | Cosmetic; not part of weld |

**Key principle:** Not all discontinuities are defects — acceptance criteria in each code determine the threshold.

## 5.11 Inspection Methods

| Method | Type | Detects |
|---|---|---|
| Visual (VT) | Surface | Size, length, location, surface defects |
| Penetrant Testing (PT) | Surface | Surface cracks, porosity, incomplete fusion |
| Magnetic Particle (MT) | Surface/subsurface | Surface and near-surface defects |
| Radiographic (RT) | Volumetric | Internal porosity, incomplete penetration, inclusions, cracks |
| Ultrasonic (UT) | Volumetric | Internal defects, incomplete penetration, porosity, cracks |

## 5.12 Filler Materials

| Base Material | Filler | Notes |
|---|---|---|
| Carbon/structural steel (Group I/II) | ER70S-6 (GMAW) or E70C-6 (MCAW) | 70 ksi minimum tensile strength |
| Aluminum | ER4043 (preferred) | Easier welding, better surface quality |
| Aluminum | ER5356 | Slightly higher strength |
| Stainless Steel | Per AWS standards | Consult for specific alloy combinations |

- Aluminum weld strength depends on base metal alloy and temper, NOT filler type.
- Refer to AWS A5.10 Annex A for aluminum filler selection guide.

## 5.13 Prototyping vs Volume Production

| Phase | Method | Tooling | Notes |
|---|---|---|---|
| Prototyping | Manual welding | Modular bench (Bluco tables) | Flexible clamps; consistency limited to operator skill |
| Low Volume | Manual welding | Dedicated weld tooling | Improved holding accuracy; reduced setup time |
| Medium–High Volume | Robotic welding | Dedicated weld cell | Consistent throughput and quality |

**Robotic welding limitations:**
- Limited flexibility for design changes.
- Long lead time for tooling and cell procurement.
- May limit weld access to joints accessible in manual process.

## 5.14 Design for Manufacturing & Assembly

**Good Design = Good Access = Good Quality Weld**

Key access factors:
- Welding gun access to joint (angles, stickout, arc visibility).
- Weld pool access to root (groove angle, root opening, welding position).

**Design considerations:**
- Drain holes: Required for cleaning process during finishing.
- Outgassing holes: Required for components welded all around.
- Fixturing: Based on datum structure; review with supplier. Tooling/location holes for consistency.
- Part warpage: Assess for assemblies with long continuous welds.
- Finishing: Paint/powder coat hang locations may require tooling holes.

## 5.15 Design Checklist

- Welding standard selected (AWS D1.1, D1.2, D1.3, or D1.6).
- Weld joint type selected (fillet, groove, plug, slot).
- Weld access verified (gun can reach joint).
- Welding angle optimized for fusion and penetration.
- Groove angle meets material requirements.
- Root opening and root face specified.
- Fillet weld sizing adequate for strength.
- Skewed joints properly handled (beveling, symbols).
- Weld penetration requirements specified (CJP or PJP).
- Weld discontinuity risks assessed.
- Drain holes and outgassing holes identified.
- Fixturing locations reviewed with supplier.
- Paint/powder coat hang locations identified.
- WPS prepared, PQR completed, welder WPQR verified.
- Inspection plan includes appropriate NDE methods.
- Part warpage assessment completed.
- Material and filler compatibility verified.


---

# 6. Integral Skin PU Foam Molding

**Source:** 930-00163_R01 Design Guideline — Integral Skin PU Foam Molding
**Process Owner:** Advanced Manufacturing Engineering

## 6.1 Process Overview

Integral skin PU foam molding ("self-skinning foam") produces a microcellular core with a tough, abrasion-resistant outer skin. The skin forms by condensation of material on the tool surface during curing (typically a few mm thick).

**Process steps:**
1. Mix polyol and isocyanate via metering unit and mix head.
2. Pour liquid mix into aluminum or steel mold.
3. Maintain mold closed during curing (chemical reaction forms PU).
4. Mold temperature controlled by cooling/heating water lines (affects skin thickness).
5. Demold finished part.

**Equipment:** Metering unit (e.g., Esco, Bolair) + Mix head (e.g., Cannon) + Tool.

**Key characteristics:**
- Tough, flexible, tear-resistant outer skin over softer foam core.
- Wide range of molded densities.
- Ideal for soft-touch, durable applications.
- Multiple polyols/isocyanates can be used for varying hardness in different areas of same part.

## 6.2 Applicability

- Annual volume: >5,000–10,000 pieces/year to justify manufacturing cell investment.
- No upper volume limit; operations can be automated with robotic work cells.
- Raw material shelf life: 3–6 months. Batch size must align with demand to consume within shelf life.

## 6.3 Materials and Finishes

### In-Mold Painting
- Recommended because PU foam (aromatic isocyanates) turns yellow-brown under UV exposure.
- Multiple colors achievable with masking.

### In-Mold Label
- Most durable labeling option.
- Custom label placed in tool before in-mold painting step.
- Chemically bonded to part during PU curing.

### Other Marking Options
- Silk screen printing, label application, pad printing (secondary operations).

## 6.4 Process Capabilities

| Parameter | Capability |
|---|---|
| Min part mass | 30–50 g |
| Max part mass | 4 kg |
| Part hardness range | 20 Shore 00 to 90 Shore A (gummy bear to golf ball) |
| Hardness control | Quantity of material poured into tool |
| Feature constraints | Limited by PU foam thickness, feature depth, and vent positioning |
| Filling | Viscosity close to water — filling is rarely the issue; venting is more critical |

## 6.5 Insert Material

- Any material can be used for inserts, with or without finishes.
- PU does NOT stick to inserts — features must be added for adhesion.
- Hole pattern on insert allows material to flow through and "bond" with the insert.

## 6.6 Part Design Guidelines

### Insert Hole Pattern
- Hole pattern required along edges of sheet metal insert.
- Allows PU material to flow through insert and properly affix over-molded foam.

### Transition Lip
- Thin lip required to transition from over-molded area to non-over-molded area of insert.
- Acts as "foam feature flash mitigation."

### Locating Features
- Features on part required to locate insert in tool.
- Also used to control foam thickness on each side of insert.

### Moldability
- Part must be extractable from tool cavity (no trapped geometry).
- Standard molding constraints apply (draft, undercuts, etc.).

## 6.7 Design Checklist

- Annual volume justifies process investment (>5K–10K pieces/year).
- Raw material batch size aligned with demand (3–6 month shelf life).
- Part mass within 30 g – 4 kg range.
- Hardness requirement within 20 Shore 00 – 90 Shore A.
- In-mold painting specified (UV protection).
- Insert hole pattern designed for PU adhesion.
- Transition lips at foam-to-bare boundaries.
- Locating features for insert positioning in tool.
- Vent locations reviewed (venting > filling concern).
- Part geometry extractable from mold (no trapped features).
- Supplier DFM review completed.


---

*End of DFM Rules Comprehensive Guide. This document consolidates all manufacturing process DFM rules from the Process Specs library and enhanced configuration files. For process-specific deep dives, refer to the individual specification documents and enhanced YAML configuration files.*
