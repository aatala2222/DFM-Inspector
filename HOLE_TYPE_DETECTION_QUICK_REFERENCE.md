# Hole Type Detection - Quick Reference

## What Changed?

The DFM Inspector now **automatically detects and classifies holes** as counterbore, countersink, or simple holes. Each type gets specific DFM rules applied.

---

## How to Identify Holes in Your Design

### Counterbore
- **Shape:** Flat-bottomed cylinder with two diameters
- **Purpose:** Socket head cap screw or bolt head sits flush
- **Machining:** 2 operations (pilot hole + counterbore)
- **Cost:** Moderate
- **Best for:** Aluminum, brass, soft materials

**Visual:**
```
    ┌─────────────┐
    │   Bolt      │
    │   Head      │
    ├─────────────┤  ← Flat bottom
    │             │
    │  Pilot      │
    │  Hole       │
    └─────────────┘
```

### Countersink
- **Shape:** Conical recess (tapered)
- **Purpose:** Flat-head screw sits flush
- **Machining:** 1 operation (countersink drill)
- **Cost:** Low
- **Best for:** Steel, hard materials
- **Angle:** 82° (metric) or 90° (imperial)

**Visual:**
```
    ╱─────────╲
   ╱  Screw   ╲
  ╱            ╲
 ╱              ╲
╱________________╲
```

### Simple Hole
- **Shape:** Straight cylindrical hole
- **Purpose:** Fastener passes through
- **Machining:** 1 operation (drill)
- **Cost:** Low
- **Best for:** Any material

**Visual:**
```
    ┌─────────┐
    │         │
    │  Hole   │
    │         │
    └─────────┘
```

---

## What the System Detects

When you run a DFM inspection, the system automatically:

1. ✓ Finds all holes in your model
2. ✓ Measures their geometry
3. ✓ Classifies each as counterbore, countersink, or simple
4. ✓ Applies specific DFM rules for that type
5. ✓ Reports findings with recommendations

---

## DFM Rules by Hole Type

### Counterbore Rules

| Rule | Requirement | Why |
|------|-------------|-----|
| Depth | ≤ 1.5 × bolt head height | Avoid unnecessary machining |
| Diameter | ≥ bolt head diameter + 0.5mm | Clearance for bolt head |
| Wall Thickness | ≥ 1.5mm | Structural integrity |
| Perpendicularity | ≤ 0.05mm | Proper bolt seating |
| Material | Soft preferred | Easier to machine |

### Countersink Rules

| Rule | Requirement | Why |
|------|-------------|-----|
| Angle | 82° or 90° (±2°) | Standard screw angles |
| Diameter | ≥ screw head diameter + 0.2mm | Clearance for screw |
| Depth | = screw head height | Flush seating |
| Material | Hard preferred | Better angle control |
| Thickness | ≥ 1.5mm | Sufficient material |

### Simple Hole Rules

| Rule | Requirement | Why |
|------|-------------|-----|
| Diameter | Standard sizes | Reduce tool inventory |
| Depth | ≤ 4 × diameter | Avoid tool breakage |
| Edge Distance | ≥ 1.5 × diameter | Prevent breakout |
| Hole Spacing | ≥ 2 × diameter | Structural integrity |

---

## Example Report Output

```
HOLE ANALYSIS REPORT
====================

Hole #1: Location (10.0, 20.0, 0.0)
├─ Type: COUNTERBORE ✓
├─ Primary Diameter: 8.0mm
├─ Counterbore Diameter: 12.0mm
├─ Counterbore Depth: 3.5mm
├─ Wall Angle: 89.8° ✓
├─ Bottom Surface: Flat ✓
├─ Confidence: 95%
└─ DFM Status: PASS
    ✓ Depth within limits
    ✓ Diameter adequate
    ✓ Wall thickness sufficient

Hole #2: Location (30.0, 20.0, 0.0)
├─ Type: COUNTERSINK ✓
├─ Diameter: 6.5mm
├─ Angle: 82.1° ✓
├─ Depth: 2.8mm
├─ Confidence: 92%
└─ DFM Status: PASS
    ✓ Angle within tolerance
    ✓ Diameter adequate
    ✓ Depth correct

Hole #3: Location (50.0, 20.0, 0.0)
├─ Type: SIMPLE HOLE ✓
├─ Diameter: 5.0mm
├─ Depth: 15.0mm
├─ Confidence: 98%
└─ DFM Status: PASS
    ✓ Standard size
    ✓ Depth ratio acceptable
    ✓ Edge distance adequate
```

---

## How Detection Works (Technical)

The system analyzes your CAD model's geometry:

1. **Finds Holes** - Looks for circular features
2. **Extracts Geometry** - Collects surface data around each hole
3. **Measures Characteristics:**
   - Diameter(s)
   - Depth
   - Surface angles
   - Bottom surface flatness
4. **Classifies:**
   - Two diameters + flat bottom = **Counterbore**
   - Conical surface + 82°/90° angle = **Countersink**
   - Single cylinder = **Simple Hole**
5. **Applies Rules** - Specific checks for each type

---

## Confidence Scores

Each detected hole has a confidence score (0-100%):

- **90-100%** - Reliable detection, trust the result
- **70-89%** - Likely correct, review if uncertain
- **50-69%** - Uncertain, verify manually
- **<50%** - Not recommended, check CAD model

**Factors affecting confidence:**
- Mesh quality
- Hole geometry clarity
- Surface finish
- Hole size

---

## Common Issues & Solutions

### "Hole Not Detected"
- **Cause:** Hole too small (<1mm) or too large (>100mm)
- **Solution:** Check hole diameter, improve mesh resolution

### "Wrong Type Detected"
- **Cause:** Mesh artifacts, unusual geometry
- **Solution:** Check confidence score, verify CAD model

### "Counterbore Detected as Countersink"
- **Cause:** Rounded edges, wall angle not exactly 90°
- **Solution:** Check wall angle tolerance in config

---

## Next Steps

1. **Run DFM Inspection** - Analyze your part
2. **Review Hole Types** - Check detected classifications
3. **Check Confidence** - Verify high-confidence detections
4. **Apply Recommendations** - Follow DFM suggestions
5. **Optimize Design** - Adjust holes for manufacturability

---

## Files to Reference

- **Detection Guide:** `config/cnc_machining_rules_enhanced.md`
- **DFM Rules:** `config/cnc_machining_rules.yaml`
- **Implementation:** `docs/enhancements/HOLE_TYPE_DETECTION_IMPLEMENTATION.md`
- **Feature Detector:** `src/feature_detector.py`

---

## Questions?

Refer to the detailed implementation guide for technical details:
`docs/enhancements/HOLE_TYPE_DETECTION_IMPLEMENTATION.md`

