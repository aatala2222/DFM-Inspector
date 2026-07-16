# Hole Type Detection Implementation Guide

## Overview

The DFM Inspector system now automatically detects and classifies holes as **counterbore**, **countersink**, or **simple holes** using geometric analysis. This enables precise DFM rule application specific to each hole type.

---

## How It Works

### Detection Process

When the system analyzes a CAD model, it:

1. **Identifies Holes** - Finds circular features using cross-section analysis
2. **Extracts Geometry** - Collects vertices and surface data around each hole
3. **Analyzes Characteristics** - Measures diameters, angles, and surface properties
4. **Classifies Type** - Determines if hole is counterbore, countersink, or simple
5. **Applies Rules** - Applies appropriate DFM checks for the detected type

---

## Technical Implementation

### Data Structure

The `Hole` class now includes hole type information:

```python
@dataclass
class Hole(Feature):
    # Basic properties
    diameter: float
    depth: float
    center: Tuple[float, float, float]
    
    # Hole type classification
    hole_type: str  # 'simple', 'counterbore', 'countersink'
    
    # Counterbore-specific
    counterbore_diameter: Optional[float]
    counterbore_depth: Optional[float]
    
    # Countersink-specific
    countersink_angle: Optional[float]
```

### Detection Algorithm

#### Step 1: Extract Hole Region
```python
hole_region_vertices = extract_hole_region(hole_center, hole_diameter * 2)
```
Collects all mesh vertices within 2× the hole diameter radius.

#### Step 2: Detect Multiple Diameters
```python
diameters = detect_diameter_changes(hole_region_vertices, hole_center)
```
Analyzes the distribution of vertex distances from hole center. If two distinct diameter peaks are found (30%+ difference), indicates counterbore.

#### Step 3: Measure Wall Angle
```python
wall_angle = measure_wall_angle(hole_region_vertices, diameters)
```
For counterbores, the wall angle between the pilot hole and counterbore should be ~90°.

#### Step 4: Check for Flat Bottom
```python
is_flat = has_flat_bottom(hole_region_vertices, hole_center)
```
Fits a plane to the bottom surface vertices. If planarity < 0.5mm, it's flat (counterbore indicator).

#### Step 5: Measure Cone Angle
```python
cone_angle = measure_cone_angle(hole_region_vertices, hole_center)
```
Analyzes the relationship between radius and depth. For countersinks, the angle should be ~82° or 90°.

---

## Detection Criteria

### Counterbore Detection

**Detected when ALL of these are true:**
- ✓ Two distinct diameters detected (30%+ difference)
- ✓ Wall angle ≈ 90° (within 5°)
- ✓ Flat bottom surface (planarity < 0.5mm)

**Result:** `hole_type = 'counterbore'`

**Properties captured:**
- `counterbore_diameter` - Larger diameter
- `counterbore_depth` - Depth of recess
- `diameter` - Pilot hole diameter

### Countersink Detection

**Detected when ALL of these are true:**
- ✓ Conical surface detected
- ✓ Cone angle ≈ 82° or 90° (within 5°)
- ✓ No flat bottom surface
- ✓ Single tapered hole (not two-step)

**Result:** `hole_type = 'countersink'`

**Properties captured:**
- `countersink_angle` - Taper angle (82° or 90°)
- `diameter` - Hole diameter at surface
- `depth` - Countersink depth

### Simple Hole Detection

**Detected when:**
- ✗ No multiple diameters
- ✗ No conical surface
- ✗ Single cylindrical hole

**Result:** `hole_type = 'simple'`

---

## DFM Rules Applied

### For Counterbores

```yaml
counterbore_rules:
  - Depth <= 1.5 × bolt head height
  - Diameter >= bolt head diameter + 0.5mm
  - Wall thickness >= 1.5mm
  - Perpendicularity <= 0.05mm
  - Material: Soft materials preferred (aluminum, brass)
```

**Cost Impact:** Moderate (2 operations)

### For Countersinks

```yaml
countersink_rules:
  - Angle = 82° or 90° (±2°)
  - Diameter >= screw head diameter + 0.2mm
  - Depth = screw head height
  - Angle tolerance <= 2°
  - Material: Hard materials preferred (steel)
```

**Cost Impact:** Low (1 operation)

### For Simple Holes

```yaml
simple_hole_rules:
  - Diameter in standard sizes
  - Depth <= 4 × diameter
  - Edge distance >= 1.5 × diameter
  - Hole spacing >= 2 × diameter
```

**Cost Impact:** Low (1 operation)

---

## Integration Points

### 1. Feature Detector (`src/feature_detector.py`)

The `FeatureDetector` class now includes:

```python
def detect_holes(self) -> List[Hole]:
    """Detects holes and classifies type"""
    holes = []
    # ... hole detection ...
    for hole in holes:
        hole = self.detect_hole_type(hole)  # Classify
    return holes

def detect_hole_type(self, hole: Hole) -> Hole:
    """Classifies hole as counterbore, countersink, or simple"""
    # ... detection logic ...
    return hole
```

### 2. DFM Inspector (`src/dfm_inspector.py`)

The inspector applies hole-type-specific rules:

```python
def evaluate_hole(self, hole: Hole) -> Dict:
    if hole.hole_type == 'counterbore':
        return self.evaluate_counterbore(hole)
    elif hole.hole_type == 'countersink':
        return self.evaluate_countersink(hole)
    else:
        return self.evaluate_simple_hole(hole)
```

### 3. CNC Machining Rules (`config/cnc_machining_rules.yaml`)

New sections added:
- `counterbore` - Counterbore-specific rules and tolerances
- `countersink` - Countersink-specific rules and tolerances

### 4. Reports

DFM reports now show:

```
Hole Analysis Report
====================

Hole #1: Location (10, 20, 0)
├─ Type: COUNTERBORE ✓
├─ Primary Diameter: 8.0mm
├─ Counterbore Diameter: 12.0mm
├─ Counterbore Depth: 3.5mm
├─ Wall Angle: 89.8° ✓
├─ Bottom Surface: Flat ✓
└─ DFM Status: PASS

Hole #2: Location (30, 20, 0)
├─ Type: COUNTERSINK ✓
├─ Diameter: 6.5mm
├─ Angle: 82.1° ✓
├─ Depth: 2.8mm
└─ DFM Status: PASS
```

---

## Usage Example

### Basic Usage

```python
from src.feature_detector import FeatureDetector
import trimesh

# Load CAD model
mesh = trimesh.load('part.step')

# Create detector
detector = FeatureDetector(mesh)

# Detect all features
features = detector.detect_all_features(detect_holes=True)

# Get holes
holes = detector.get_features_by_type('hole')

# Check hole types
for hole in holes:
    print(f"Hole at {hole.center}")
    print(f"  Type: {hole.hole_type}")
    
    if hole.hole_type == 'counterbore':
        print(f"  Counterbore Diameter: {hole.counterbore_diameter}mm")
        print(f"  Counterbore Depth: {hole.counterbore_depth}mm")
    
    elif hole.hole_type == 'countersink':
        print(f"  Countersink Angle: {hole.countersink_angle}°")
```

### With DFM Inspection

```python
from src.dfm_inspector import DFMInspector

# Create inspector
inspector = DFMInspector(config_path='config/inspection_rules.yaml')

# Evaluate holes
for hole in holes:
    results = inspector.evaluate_hole(hole)
    
    print(f"Hole Type: {hole.hole_type}")
    print(f"DFM Status: {results['status']}")
    
    for check in results['checks']:
        print(f"  {check['name']}: {check['result']}")
        if check['recommendation']:
            print(f"    → {check['recommendation']}")
```

---

## Accuracy and Limitations

### Accuracy Factors

- **Mesh Quality**: Higher resolution meshes improve detection accuracy
- **Hole Geometry**: Clear, well-defined holes are detected reliably
- **Surface Finish**: Smooth surfaces improve angle measurement
- **Confidence Score**: Each hole has a confidence value (0-1)

### Current Limitations

1. **Blind Holes**: Depth estimation may be approximate
2. **Partial Holes**: Holes cut off by model boundaries may not detect
3. **Complex Geometry**: Holes with irregular shapes may misclassify
4. **Very Small Holes**: Holes < 1mm may not detect reliably
5. **Threaded Holes**: Thread detection is separate from type classification

### Confidence Thresholds

```python
confidence_levels = {
    'high': 0.85,      # Reliable detection
    'medium': 0.70,    # Likely correct
    'low': 0.50,       # Uncertain
    'unreliable': 0.0  # Not recommended
}
```

---

## Troubleshooting

### Hole Not Detected

**Possible causes:**
- Hole diameter < 1mm (below minimum)
- Hole diameter > 100mm (above maximum)
- Mesh resolution too low
- Hole partially outside model bounds

**Solution:** Adjust detection parameters or improve mesh quality

### Wrong Hole Type Classification

**Possible causes:**
- Mesh artifacts or noise
- Unusual hole geometry
- Surface finish issues
- Confidence score too low

**Solution:** Review confidence score, check mesh quality, adjust thresholds

### Counterbore Detected as Countersink

**Possible causes:**
- Rounded edges instead of sharp corners
- Mesh smoothing applied
- Wall angle not exactly 90°

**Solution:** Check wall angle tolerance, verify CAD model

---

## Configuration

### Adjusting Detection Sensitivity

In `config/cnc_machining_rules.yaml`:

```yaml
counterbore:
  detection:
    wall_angle_tolerance: 5  # degrees (increase for more tolerance)
    diameter_difference_threshold: 0.3  # 30% (increase for smaller differences)
    flatness_tolerance: 0.5  # mm (increase for less flat bottoms)

countersink:
  detection:
    cone_angle_tolerance: 5  # degrees
    angle_standards: [82, 90]  # degrees
```

### Adjusting DFM Rule Thresholds

```yaml
counterbore:
  design_guidelines:
    min_wall_thickness: 1.5  # mm (increase for stronger parts)
    depth_ratio_max: 1.5  # × bolt head height

countersink:
  tolerances:
    angle: 2.0  # degrees (decrease for tighter tolerance)
```

---

## Performance

### Detection Speed

- **Per Hole:** ~50-100ms (depends on mesh resolution)
- **10 Holes:** ~0.5-1.0 seconds
- **100 Holes:** ~5-10 seconds

### Memory Usage

- **Mesh Storage:** Depends on model complexity
- **Detection Overhead:** ~10-20MB for typical models

---

## Future Enhancements

1. **Machine Learning**: Train model on known hole types for better accuracy
2. **Threaded Hole Detection**: Identify and classify threaded holes
3. **Blind Hole Depth Estimation**: Better depth prediction for blind holes
4. **Custom Hole Types**: Support for non-standard hole geometries
5. **Visualization**: 3D highlighting of detected hole types
6. **Batch Processing**: Optimize for multiple parts

---

## References

- **CNC Machining Rules**: `config/cnc_machining_rules.yaml`
- **Detection Guide**: `config/cnc_machining_rules_enhanced.md`
- **Feature Detector**: `src/feature_detector.py`
- **DFM Inspector**: `src/dfm_inspector.py`

