# Sheet Metal Design Rules - Extracted from 930-00172_R01-1

## Key Design Guidelines from Amazon Robotics Document (98 pages)

### Process Capabilities and Tolerances

#### Turret Press (Prototype/Low Volume)
- Feature to Feature: ±0.10mm (±0.004")
- Feature to Edge: ±0.10mm (±0.004"), minimum 1.33T
- Minimum Feature Size: 0.25T (25% of material thickness)

#### Laser Cutting
- Feature to Feature: ±0.10mm (±0.004")
- Feature to Edge: ±0.10mm (±0.004"), minimum 1.33T
- Minimum Kerf: ±0.2mm (±0.008")
- Minimum Feature Size: 0.25T

#### Hand Press Brake
- Fold to Fold: ±0.5mm (±0.020")
- Fold to Feature/Edge: ±0.4mm (±0.015")
- Bend Angle: ±1.5°
- Minimum Radius: 1.33T

#### Progressive Tool (Production)
- Features in Same Station: ±0.05mm (±0.002")
- Features in Different Stations: ±0.2mm (±0.008")
- Folds in Same Station: ±0.2mm (±0.008")
- Folds in Different Stations: ±0.4mm (±0.016")
- Fold to Feature/Edge: ±0.25mm (±0.010")
- Bend Angle: ±1°
- Minimum Hole Diameter/Slot Width: 1.33T
- Hole/Feature Size: ±0.08mm (±0.003")

### Critical Design Rules (Chapter 5: DFX Guidelines)

#### 1. Hole Specifications
- **Minimum Hole Diameter**: 1.33T (1.33× material thickness)
- **Minimum Distance Between Holes**: 1.2T
- **Hole to Edge Distance**: Minimum 2T (2× thickness)
- **Hole to Bend Distance**: 
  - Minimum: 2.0T + R (where R = bend radius)
  - Preferred: 3T + R for better quality

#### 2. Bend Radius
- **Minimum Bend Radius**: 1.0T or 0.6mm (whichever is greater)
- **Low Carbon Steel Only**: Can use 0.5T minimum
- **Standard**: R = 1.0T minimum for most materials

#### 3. Bend Relief
- **Relief Depth**: Must be greater than bend radius
- **Relief Width**: Minimum 1T (material thickness)
- **Purpose**: Prevents tearing when bend is close to edge
- **Rule**: Edge distance from bend must be ≥ bend radius

#### 4. Slot Distance from Bend
- **Short Slots** (L < 50mm): A = 3T + R
- **Long Slots** (L ≥ 50mm): A = 4T + R
- **Minimum Radius**: 1.0T or 0.6mm

#### 5. Flange Dimensions
- **Minimum Flange Length (A)**: 2B or 6T (whichever is less)
- **Minimum Flange Width (B)**: 1.33T
- **Minimum Edge Distance (C)**: 2T
- **Minimum Radius (R1, R2)**: 0.5T or 0.4mm

#### 6. Feature Spacing
- **Minimum Distance Between Features**: 2.0T
- **Maximum Unsupported Length**: 50mm when at minimum dimensions

#### 7. Z-Bends (Offsets)
- **90° Offset**: H ≤ 5T, R = 1.5T
- **45° Offset**: R = 0.2mm minimum

### Material Thickness Tolerances

#### Stainless Steel (Commercial Quality)
- 0.6-0.79mm: ±0.05mm
- 0.8-0.99mm: ±0.055mm
- 1.0-1.19mm: ±0.06mm
- 1.2-1.49mm: ±0.07mm
- 1.5-1.99mm: ±0.08mm
- 2.0-2.49mm: ±0.09mm
- 2.5-2.99mm: ±0.11mm
- 3.0mm: ±0.13mm

#### SECC Steel (Electro-Galvanized)
- 0.4-0.6mm: ±0.03mm
- 0.61-0.8mm: ±0.04mm
- 0.81-1.0mm: ±0.05mm
- 1.01-1.2mm: ±0.06mm
- 1.21-1.6mm: ±0.08mm
- 1.61-2.0mm: ±0.10mm

#### Aluminum (Group I: 1000, 3000, 5005, 5050 series)
- 0.6-0.8mm: ±0.03mm
- 0.81-1.0mm: ±0.04mm
- 1.01-1.2mm: ±0.04mm
- 1.21-1.5mm: ±0.05mm
- 1.51-1.8mm: ±0.06mm
- 2.01-2.5mm: ±0.07mm
- 2.51-3.0mm: ±0.08mm

### General Design Checklist

1. **Specify punch direction** - Critical for tooling
2. **Specify grain direction** - Affects formability
3. **Identify deburring areas** - Sharp edges need treatment
4. **Group features in single station** - Better tolerances
5. **Avoid secondary operations** - Use Taptite instead of tapping
6. **Keep embosses/draws shallow** - Easier forming
7. **Use standard materials** - Lower cost, better availability
8. **Use precoated materials** - Avoid secondary finishing
9. **Add tooling holes** - Consistent reference features
10. **Datum structure aligns with function** - Proper GD&T
11. **Use sheared edges for critical references** - Better accuracy
12. **Define max/min bend radius** - Manufacturing clarity

### Secondary Operation Alternatives

| Secondary Operation | Alternative |
|-------------------|-------------|
| Tapped Hole | Extruded hole + Taptite screw |
| Threaded Hardware | Extruded hole + Taptite |
| Spacers | Bridge feature or emboss |
| Standoffs | Bridge feature or emboss |
| Spot Welds | Tox/Tog-L-Loc, Swaging |
| Rivets | Tox/Tog-L-Loc, Swaging |

### Key Formulas (T = material thickness, R = bend radius)

1. **Minimum Hole Diameter**: 1.33T
2. **Hole to Edge**: ≥2T
3. **Hole to Bend**: ≥2T + R (minimum), ≥3T + R (preferred)
4. **Hole Spacing**: ≥1.2T
5. **Bend Radius**: ≥1.0T or 0.6mm
6. **Flange Length**: ≥1.33T
7. **Bend Relief Width**: ≥1T
8. **Bend Relief Depth**: >R

## Implementation Priority

### Critical (FAIL if violated):
1. Hole diameter < 1.33T
2. Hole to edge < 2T
3. Bend radius < 1.0T (or 0.6mm)
4. Hole spacing < 1.2T

### Important (WARNING if violated):
1. Hole to bend < 2T + R
2. Flange length < 1.33T
3. Missing bend relief when needed
4. Feature spacing < 2T

### Optimization (SUGGESTIONS):
1. Use Taptite instead of tapped holes
2. Avoid secondary operations
3. Use standard materials
4. Group features in single station
5. Add tooling holes for reference
