# Welding DFM Guide

Based on document 960-00169_R01: Welding Fundamentals & AWS Basics

## Overview

This guide integrates AWS (American Welding Society) standards and welding best practices into the DFM Inspector tool for checking weldability of CAD designs.

## Applicable AWS Standards

- **AWS D1.1/D1.1M** - Structural Welding Code - Steel
- **AWS D1.2/D1.2M** - Structural Welding Code - Aluminum  
- **AWS D1.3/D1.3M** - Structural Welding Code - Sheet Steel
- **AWS D1.6/D1.6M** - Structural Welding Code - Stainless Steel
- **AWS A2.4** - Standard Symbols for Welding, Brazing, and Nondestructive Examination
- **AWS A3.0** - Standard Welding Terms and Definitions

## Material Requirements

### Steel Structural (AWS D1.1)
- **Minimum thickness**: 3.0mm (1/8")
- **Maximum yield strength**: 690 MPa (100 ksi)
- **Filler material**: ER70S-6 (GMAW) or E70C-6 (MCAW)

### Aluminum Structural (AWS D1.2)
- **Minimum thickness**: 1.5mm (any thickness for structural alloys)
- **Filler material**: ER4043 (preferred for quality) or ER5356 (higher strength)

### Sheet Steel (AWS D1.3)
- **Maximum thickness**: 5.0mm (less than 3/16")
- **Maximum yield strength**: 550 MPa (80 ksi)

### Stainless Steel (AWS D1.6)
- **Minimum thickness**: 1.5mm (1/16" or 16 gage)

## Critical Design Parameters

### 1. Groove Angles

Proper groove angles ensure adequate fusion and penetration:

| Material | Min Angle | Max Angle | Recommended |
|----------|-----------|-----------|-------------|
| Carbon Steel | 50° | 60° | 55° |
| Stainless Steel | 55° | 60° | 57.5° |
| Aluminum | 60° | 65° | 62.5° |

**Why it matters**: Insufficient groove angle leads to incomplete fusion and weak welds.

### 2. Root Opening (Gap)

The gap between parts is critical for:
- Proper weld penetration
- Complete fusion through joint thickness
- Avoiding lack of penetration (LOP) defects

### 3. Root Face

- **Required**: When bevel angle ≥ 30°, minimum 1.0mm (0.040")
- **Not required**: When bevel angle < 30°
- **Alignment**: Root face aligned with contact surface

### 4. Skewed Joints

Special rules apply when parts meet at angles other than 90°:

#### Inclination Angle (β) Rules:
- **β ≤ 10°**: Beveling NOT mandatory, use fillet weld symbol
- **β > 10°**: Beveling IS mandatory
  - Calculate bevel angle: δ = γ - β
  - Where γ is the required groove angle

#### Angle Between Parts (α) Rules:
- **60° ≤ α < 90°**: Use fillet weld
- **40° ≤ α < 60°**: Use V-groove weld with W dimension specified
- **30° ≤ α < 40°**: NOT RECOMMENDED - welding tests required
- **α ≤ 30°**: Use fillet weld if groove angle γ ≥ 60°

## Weld Access Requirements

### Good Design = Good Access = Good Quality Weld

Critical access considerations:

1. **Welding Gun Access**
   - Adequate space for gun positioning
   - Clear path to joint

2. **Welding Angles**
   - Affects fusion quality
   - Affects penetration depth
   - Affects weld symmetry
   - Affects surface quality

3. **Stickout Distance**
   - Distance from contact tip to workpiece
   - Affects amperage and heat input
   - Affects fusion and penetration

4. **Arc Accessibility**
   - Visibility to weld pool
   - Access to root of joint
   - Critical for quality control

## Weld Types and Throat Dimensions

### Fillet Welds

Three throat measurements:

1. **Theoretical Throat**: Distance from root perpendicular to hypotenuse (assumes zero gap)
2. **Actual Throat**: Shortest distance from root to weld face
3. **Effective Throat**: Minimum distance from face (minus convexity) to root
   - Used for strength calculations

### Groove Welds

- **Complete Joint Penetration (CJP)**: Weld metal extends through entire joint thickness
- **Partial Joint Penetration (PJP)**: Incomplete joint penetration exists

## Common Weld Discontinuities

The tool checks for conditions that lead to these defects:

| Discontinuity | Description | Severity |
|---------------|-------------|----------|
| Porosity | Gas entrapment cavities | Warning |
| Undercut | Groove melted into base metal | Critical |
| Overlap | Weld metal protrusion | Critical |
| Underfill | Weld face below base metal | Warning |
| Excessive Convexity | Weld face too high | Warning |
| Incorrect Size | Weld too big or small | Critical |
| Incomplete Fusion (LOF) | No fusion between metals | Critical |
| Incomplete Penetration (LOP) | Weld doesn't extend through joint | Critical |
| Inclusion | Foreign material trapped | Critical |
| Crack | Fracture-type discontinuity | Critical |
| Spatter | Expelled metal particles | Info |

## Design Considerations

### Drain Holes
- **Required for**: Cleaning process during finishing
- **Required for**: Out-gassing in all-around welds
- **Action**: Add drain holes in enclosed sections

### Fixturing
- **Base on**: Datum structure from drawings
- **Include**: Tooling/location holes
- **Consider**: Part warpage for long continuous welds

### Finishing
- **Plan for**: Paint/powder coating hang locations
- **May require**: Additional tooling holes

### Slot and Plug Welds
- **Too small**: Insufficient strength
- **Too large**: Excessive heat input and distortion
- **Action**: Optimize diameter/width

## Production Volume Considerations

### Prototyping / Low Volume
- **Method**: Manual welding
- **Tooling**: Modular weld tables (e.g., Bluco)
- **Consistency**: Depends on operator skill
- **Flexibility**: High - easy to modify

### Medium / High Volume
- **Method**: Robotic welding
- **Advantages**: 
  - Consistent throughput
  - Consistent quality
- **Limitations**:
  - Limited flexibility for changes
  - Long lead time for tooling
  - May limit weld access to some joints

## Quality Requirements

### Welding Qualification

Three key documents required:

1. **WPS (Welding Procedure Specification)**
   - The "recipe" for successful welds
   - Specifies all essential variables
   - Based on qualified PQR

2. **PQR (Procedure Qualification Record)**
   - Written confirmation of successful qualification
   - Documents actual test conditions
   - Records all essential variables

3. **WPQR (Welder Performance Qualification Record)**
   - Certifies welder's ability
   - Documents welder qualification tests
   - Required for each welder

### Inspection Methods

- **VT (Visual Testing)**: Surface inspection for size, length, location
- **PT (Penetrant Testing)**: Surface discontinuities
- **MT (Magnetic Particle Testing)**: Surface and sub-surface discontinuities
- **RT (Radiographic Testing)**: Volumetric inspection
- **UT (Ultrasonic Testing)**: Volumetric inspection

## Using the Welding DFM Inspector

### Command Line

```bash
# Basic welding inspection
python welding_main.py model.step

# Specify material type
python welding_main.py model.step -m aluminum_structural

# Show applicable standards
python welding_main.py --show-standards -m stainless_steel

# Show recommended filler material
python welding_main.py --filler-material -m steel_structural

# Generate report with visualization
python welding_main.py model.step -m sheet_steel -o report.html --visualize
```

### Python API

```python
from src import CADParser
from src.welding_inspector import WeldingInspector

# Load CAD file
parser = CADParser('weldment.step')
parser.load()

# Run welding inspection
inspector = WeldingInspector('config/welding_rules.yaml')
results = inspector.inspect(parser, material_type='steel_structural')

# Check weldability score
print(f"Weldability Score: {results['summary']['weldability_score']}/100")

# Get applicable standards
standards = inspector.get_applicable_standards('steel_structural')
print(f"Standards: {standards}")

# Get filler material recommendation
filler = inspector.get_filler_material_recommendation('steel_structural', 'gmaw')
print(f"Recommended Filler: {filler}")
```

## Checklist for Welding Design Review

Use this checklist when designing welded assemblies:

- [ ] Material thickness meets AWS standard requirements
- [ ] Groove angles within specified range for material
- [ ] Root opening (gap) specified and adequate
- [ ] Root face specified where required (bevel ≥ 30°)
- [ ] Skewed joints properly designed with correct beveling
- [ ] Adequate welding gun access to all joints
- [ ] Proper welding angles achievable
- [ ] Arc accessibility and visibility to weld pool
- [ ] Drain holes provided for cleaning and out-gassing
- [ ] Fixturing and tooling holes included
- [ ] Finishing hang locations considered
- [ ] Slot/plug weld sizes optimized
- [ ] Long continuous welds reviewed for warpage
- [ ] Production volume considered (manual vs robotic)
- [ ] WPS/PQR/WPQR requirements understood
- [ ] Inspection method specified

## References

- Document 960-00169_R01: Welding Fundamentals & AWS Basics
- AWS D1.1/D1.1M:2020 - Structural Welding Code - Steel
- AWS D1.2/D1.2M:2014 - Structural Welding Code - Aluminum
- AWS D1.3/D1.3M:2018 - Structural Welding Code - Sheet Steel
- AWS D1.6/D1.6M:2017 - Structural Welding Code - Stainless Steel
- AWS A2.4:2012 - Standard Symbols for Welding
- AWS A3.0M/A3.0:2010 - Standard Welding Terms and Definitions

## Contact

For questions about welding design or this tool:
- Review the AWS standards applicable to your project
- Consult with welding engineers during design phase
- Perform DFM reviews with manufacturing team
- Consider production volume when selecting welding method

---

**Remember**: Good Design = Good Access = Good Quality Weld
