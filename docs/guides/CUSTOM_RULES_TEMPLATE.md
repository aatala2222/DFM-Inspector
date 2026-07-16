# Custom DFM Rules Template

Use this template to document and implement your custom manufacturing rules based on your specific requirements and industry standards.

## How to Add Custom Rules

1. **Document your rules** in this file
2. **Update** `config/inspection_rules.yaml` with thresholds
3. **Implement** check methods in `src/dfm_inspector.py`
4. **Test** with sample CAD files

---

## Your Custom Rules

### Rule Category: [e.g., Material-Specific Requirements]

#### Rule 1: [Rule Name]
- **Description**: [What does this rule check?]
- **Threshold**: [Numeric value and unit]
- **Severity**: [critical / warning / info]
- **Rationale**: [Why is this important?]
- **Standard Reference**: [ISO standard, company guideline, etc.]
- **Recommendation**: [How to fix violations]

**Example:**
```yaml
# Add to config/inspection_rules.yaml
material_specific:
  aluminum_6061:
    min_wall_thickness: 2.0  # mm
    min_bend_radius: 1.5     # mm
```

---

### Rule Category: Assembly Requirements

#### Rule 2: Fastener Clearance
- **Description**: Minimum clearance around fastener holes for tool access
- **Threshold**: 5.0 mm
- **Severity**: warning
- **Rationale**: Ensures assembly tools can access fasteners
- **Standard Reference**: Company assembly guidelines
- **Recommendation**: Increase clearance or use alternative fastener type

---

### Rule Category: Surface Finish

#### Rule 3: [Your Rule]
- **Description**: 
- **Threshold**: 
- **Severity**: 
- **Rationale**: 
- **Standard Reference**: 
- **Recommendation**: 

---

## Amazon Robotics Specific Rules

### Rule Category: Structural Integrity

#### Rule 4: Dynamic Load Bearing
- **Description**: Components subject to dynamic loads require increased safety factors
- **Threshold**: Safety factor ≥ 3.0
- **Severity**: critical
- **Rationale**: Robotics applications involve repeated loading cycles
- **Standard Reference**: ISO 3691-4:2020
- **Recommendation**: Increase cross-sectional area or use higher-strength material

---

### Rule Category: Electrical Safety

#### Rule 5: Clearance for High Voltage
- **Description**: Minimum clearance between conductive parts and high-voltage components
- **Threshold**: 10.0 mm (for voltages up to 60V)
- **Severity**: critical
- **Rationale**: Prevents electrical hazards and ensures operator safety
- **Standard Reference**: IEC 61010, UL 3100
- **Recommendation**: Increase spacing or add insulation barriers

---

## Process-Specific Rules

### Injection Molding

#### Rule 6: Gate Location
- **Description**: Gate should be located at thickest section
- **Threshold**: N/A (qualitative check)
- **Severity**: warning
- **Rationale**: Ensures proper material flow and minimizes defects
- **Standard Reference**: Industry best practices
- **Recommendation**: Relocate gate to thicker wall section

---

### CNC Machining

#### Rule 7: Tool Access
- **Description**: All features must be accessible by standard tooling
- **Threshold**: Minimum tool diameter: 3.0 mm
- **Severity**: critical
- **Rationale**: Non-standard tools increase cost and lead time
- **Standard Reference**: Shop capabilities
- **Recommendation**: Redesign feature or specify custom tooling

---

### 3D Printing / Additive Manufacturing

#### Rule 8: Overhang Angle
- **Description**: Maximum overhang angle without support
- **Threshold**: 45 degrees
- **Severity**: warning
- **Rationale**: Prevents print failures and reduces support material
- **Standard Reference**: FDM printing guidelines
- **Recommendation**: Add support structures or redesign geometry

---

## Material-Specific Rules

### Material: [Your Material]

#### Rule 9: [Material Property]
- **Description**: 
- **Threshold**: 
- **Severity**: 
- **Rationale**: 
- **Standard Reference**: 
- **Recommendation**: 

---

## Implementation Checklist

- [ ] Rules documented in this file
- [ ] Thresholds added to `config/inspection_rules.yaml`
- [ ] Check methods implemented in `src/dfm_inspector.py`
- [ ] Unit tests created (optional)
- [ ] Tested with sample CAD files
- [ ] Documentation updated in README.md

---

## Notes and References

Add any additional notes, references to standards, or links to documentation here:

- [ISO 3691-4:2020](https://www.iso.org/standard/73933.html) - Industrial trucks safety
- [ISO 13849-1:2015](https://www.iso.org/standard/69883.html) - Safety control systems
- Your company design guidelines
- Material datasheets
- Manufacturing process specifications

---

## Example Implementation

Here's how to implement a custom rule in `src/dfm_inspector.py`:

```python
def _check_custom_rule(self, parser, results: Dict):
    """Check your custom manufacturing rule"""
    rules = self.rules['your_category']
    
    # Extract relevant geometry
    features = parser.extract_features()
    
    # Check against threshold
    for feature in features:
        if feature.value < rules['threshold']:
            results['issues'].append({
                'category': 'Your Category',
                'severity': 'critical',
                'location': feature.location,
                'message': f'Value {feature.value} below threshold {rules["threshold"]}',
                'recommendation': 'Your recommendation here'
            })
```

Then add the check to the `inspect()` method:
```python
def inspect(self, cad_parser) -> Dict:
    # ... existing code ...
    self._check_custom_rule(cad_parser, results)
    # ... rest of code ...
```
