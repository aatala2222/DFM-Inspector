# Injection Molding Design Rules - Extracted from 930-00164_R01

## Key Design Guidelines from Document

### 1. Wall Thickness
- **Optimal Range**: 0.75mm - 3.0mm
- **Minimum**: 0.5mm (risk of short shots)
- **Maximum**: 6.0mm (risk of sink marks, warpage, longer cycle times)
- **Rule**: Maintain uniform wall thickness throughout part

### 2. Draft Angles
- **Minimum**: 1° per side for textured surfaces
- **Recommended**: 1-3° for smooth surfaces
- **Purpose**: Facilitate part ejection from mold

### 3. Ribs and Gussets
- **Rib Thickness**: 50-60% of nominal wall thickness
- **Rib Height**: Maximum 3× nominal wall thickness
- **Spacing**: Minimum 2× wall thickness between ribs
- **Purpose**: Add strength without increasing wall thickness

### 4. Radii and Chamfers
- **Internal Radii**: Minimum 0.5× wall thickness
- **External Radii**: Minimum 1.5× wall thickness
- **Sharp Corners**: Avoid - cause stress concentrations

### 5. Bosses
- **Boss Wall Thickness**: 60% of nominal wall thickness
- **Boss Height**: Maximum 2.5× outer diameter
- **Base Fillet**: Minimum 0.25× wall thickness
- **Gussets**: Required for tall bosses

### 6. Undercuts
- **Avoid if possible**: Require side actions (expensive)
- **Alternative**: Design for straight pull molds
- **If necessary**: Minimize depth and complexity

### 7. Gate Location
- **Considerations**: 
  - Avoid gating on show surfaces
  - Gate at thickest section
  - Consider weld lines
  - Multiple gates for large parts

### 8. Surface Finishes (SPI Standards)
- **A-1 to A-3**: High gloss (diamond polished)
- **B-1 to B-3**: Semi-gloss (paper polished)
- **C-1 to C-3**: Matte (stone finished)
- **D-1 to D-3**: Textured (media blasted)

### 9. Material-Specific Considerations
- **ABS**: Excellent flow, good for complex geometries
- **Polycarbonate**: Requires higher mold temperatures (80-100°C)
- **Nylon**: Hygroscopic - requires drying before molding
- **PP**: High shrinkage - account for 1.5-2.5%

### 10. Tolerances
- **Standard**: ±0.1mm for dimensions <25mm
- **Tight**: ±0.05mm (requires additional cost)
- **Across parting line**: Add ±0.05mm

## Implementation Priority

1. **Critical (FAIL if violated)**:
   - Wall thickness <0.5mm or >6.0mm
   - No draft angles
   - Sharp internal corners

2. **Important (WARNING if violated)**:
   - Non-uniform wall thickness
   - Insufficient rib thickness
   - Boss design issues

3. **Optimization (SUGGESTIONS)**:
   - Surface finish selection
   - Gate location optimization
   - Material selection guidance
