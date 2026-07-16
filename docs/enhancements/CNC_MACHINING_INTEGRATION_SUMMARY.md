# CNC Machining DFM Integration Summary

## Document Processed

**File**: CNC_DFM_Guidelines.md  
**Sections**: 25 main sections + 3 appendices  
**Guidelines**: 200+ specific rules and checks  
**Standards**: ISO 2768, ASME Y14.5, ISO 1302, ISO 965, ISO 286

## What Was Extracted

### 1. Tolerance Specifications (Section 1)
- **Standard tolerance**: ±0.1mm for non-critical features
- **Precision tolerance**: ±0.01-0.02mm for critical surfaces only
- **Target**: Only 5-10% of features should have tight tolerances
- **Cost impact**: Over-tolerancing increases cost by 40-80% per feature
- **Flag threshold**: >20% features with tight tolerances

### 2. Internal Corners and Radii (Section 2)
- **Minimum radius**: 0.5mm (absolute minimum)
- **Recommended**: radius = 1/3 × pocket depth
- **Standard sizes**: 0.5, 1, 3, 5mm
- **Sharp corners**: Require EDM (+200-400% cost)
- **Tool-to-radius relationship**: Documented for 3, 6, 10, 12mm tools

### 3. Wall Thickness by Material (Section 3)
| Material | Min (mm) | Recommended (mm) | Machinability |
|----------|----------|------------------|---------------|
| Aluminum 6061/7075 | 0.8 | 1.0 | Excellent |
| Mild Steel | 1.0 | 1.5 | Moderate |
| Stainless 304/316 | 1.2 | 1.5 | Fair |
| Brass/Copper | 0.8 | 1.0 | Excellent |
| Titanium | 1.5 | 2.0 | Poor |
| Plastics | 1.5 | 2.0 | Moderate |

- **Max aspect ratio**: 4:1 (height:thickness)
- **Recommend ribs**: For aspect ratio >3:1

### 4. Pocket and Cavity Depth (Section 4)
- **Maximum depth**: 4× tool diameter
- **Optimal depth**: 2-3× tool diameter
- **Deep cavities**: Require specialized long-reach tools (increased cost)
- **Design alternative**: Use stepped cavities

### 5. Hole Design (Section 5)
- **Standard metric sizes**: 3, 4, 5, 6, 8, 10, 12, 16, 20mm
- **Standard imperial**: 1/8", 3/16", 1/4", 5/16", 3/8", 1/2", 5/8", 3/4"
- **Max depth**: 4× hole diameter
- **Min edge distance**: 1.5× hole diameter
- **Min hole spacing**: 2× hole diameter
- **Preference**: Through-holes over blind holes

### 6. Thread Specifications (Section 6)
- **Standard metric**: M2, M2.5, M3, M4, M5, M6, M8, M10, M12, M16, M20
- **Standard imperial**: #4-40, #6-32, #8-32, #10-24, 1/4-20, 5/16-18, 3/8-16, 1/2-13
- **Standard depth**: 1.5× nominal diameter
- **Min depth**: 1× diameter (low-strength)
- **Max depth**: 2.5× diameter

### 7. Material Machinability Ratings (Section 7)
| Material | Rating | Cost | Tool Wear | Thermal Expansion |
|----------|--------|------|-----------|-------------------|
| Aluminum 6061 | ★★★★★ | 1.0× | Low | 23.0 µm/m·°C |
| Aluminum 7075 | ★★★★☆ | 1.2× | Low | 23.0 |
| Brass | ★★★★☆ | 1.5× | Very Low | 19.0 |
| Mild Steel 1018 | ★★★☆☆ | 1.3× | Moderate | 12.0 |
| Stainless 304 | ★★☆☆☆ | 2.0× | High | 17.0 |
| Stainless 316 | ★★☆☆☆ | 2.2× | High | 17.0 |
| Titanium Gr5 | ★☆☆☆☆ | 4.0× | Very High | 8.6 |
| Tool Steel | ★☆☆☆☆ | 3.5× | Very High | 12.0 |

### 8. Setup Minimization (Section 8)
- **Cost per setup**: 15-60 minutes, +30-40% cost
- **Alignment error**: ±0.02-0.05mm per setup
- **Target**: ≤2 setups on 3-axis machine
- **Machine types**:
  - 3-axis: 1-4 setups, 1.0× cost
  - 4-axis: 1-2 setups, 1.3× cost
  - 5-axis: 1 setup, 1.8-2.5× cost

### 9. Tool Access and Clearance (Section 9)
- **Minimum channel width**: 3× tool diameter
- **Recommended**: 4× tool diameter
- **Optimal**: 5× tool diameter
- **Chamfers for entry**: 0.5-1mm
- **Undercuts**: Require special tools or 5-axis

### 10. Surface Finish (Section 10)
| Finish Type | Ra (µm) | Application | Cost |
|-------------|---------|-------------|------|
| As-Machined | 3.2-6.3 | Functional | 1.0× |
| Fine Machined | 1.6-3.2 | Moving parts | 1.2× |
| Bead Blasted | 1.6-2.4 | Aesthetic | 1.3× |
| Anodized Type II | 0.8-1.6 | Corrosion | 1.5× |
| Anodized Type III | 0.4-0.8 | Aerospace | 2.0× |
| Polished | 0.4-0.8 | Medical | 2.5-3.0× |

### 11. Cost Drivers (Section 14)
1. **Machining time**: 40-60% of total cost
2. **Material cost**: 20-30%
3. **Setup time**: 10-20%
4. **Tooling**: 5-10%
5. **Finishing**: 5-15%

### Cost Reduction Opportunities
| Change | Time Savings | Cost Reduction | Difficulty |
|--------|--------------|----------------|------------|
| Relax tolerances | 30-50% | 40-80% | Easy |
| Reduce setups | 20-40% | 30-40% | Moderate |
| Add corner radii | 15-25% | 20-30% | Easy |
| Standardize holes | 10-20% | 15-25% | Easy |
| Simplify geometry | 20-40% | 25-40% | Moderate |

### 12. GD&T Tolerances (Section 17)
**Achievable on 3-axis CNC:**
- Flatness: 0.05mm typical, 0.01mm tight
- Perpendicularity: 0.05mm typical, 0.02mm tight
- Parallelism: 0.05mm typical, 0.02mm tight
- Position: 0.1mm typical, 0.02mm tight
- Concentricity: 0.05mm typical, 0.01mm tight

### 13. Batch Size Considerations (Section 18)
| Batch Size | Setup Impact | Unit Cost | Approach |
|------------|--------------|-----------|----------|
| 1-5 (Prototype) | 50-70% | Very High | Minimize setups |
| 10-50 (Low) | 30-40% | High | Optimize toolpaths |
| 50-500 (Medium) | 10-20% | Moderate | Custom fixtures |
| 500+ (High) | <10% | Low | Automation |

## Files Created

### 1. Configuration
- **config/cnc_machining_rules.yaml** - Complete CNC machining rules
  - Tolerance specifications
  - Corner radius requirements
  - Wall thickness by material
  - Pocket depth limits
  - Hole specifications
  - Thread standards
  - Material machinability ratings
  - Setup requirements
  - Tool access rules
  - Surface finish specifications
  - Cost optimization data
  - GD&T tolerances
  - Batch size considerations

### 2. Source Code
- **src/inspectors/cnc_machining_inspector.py** - CNC-specific inspector
  - Tolerance checking
  - Corner radius verification
  - Wall thickness validation
  - Pocket depth analysis
  - Hole specification checking
  - Thread verification
  - Material machinability assessment
  - Setup estimation
  - Tool access evaluation
  - Surface finish validation
  - Geometry complexity analysis
  - Cost opportunity identification

### 3. Main Script
- **cnc_machining_main.py** - Command-line interface
  - Material selection (9 materials)
  - Material ratings display
  - Standards reference
  - Cost analysis mode
  - Report generation
  - Visualization support

### 4. Documentation
- **CNC_MACHINING_INTEGRATION_SUMMARY.md** - This file

## How to Use

### Basic CNC Machining Inspection
```bash
python cnc_machining_main.py model.step -m aluminum_6061
```

### Show Material Ratings
```bash
python cnc_machining_main.py --show-materials
```

### Show Applicable Standards
```bash
python cnc_machining_main.py --show-standards
```

### With Cost Analysis
```bash
python cnc_machining_main.py model.step -m stainless_304 --cost-analysis
```

### Generate Report with Visualization
```bash
python cnc_machining_main.py model.step -m titanium_grade5 -o report.html --visualize
```

### Python API
```python
from src import CADParser
from src.inspectors.cnc_machining_inspector import CNCMachiningInspector

parser = CADParser('part.step')
parser.load()

inspector = CNCMachiningInspector()
results = inspector.inspect(parser, material='aluminum_6061')

print(f"Machinability Score: {results['summary']['machinability_score']}/100")
print(f"Material Rating: {results['summary']['material_rating']}/5")
print(f"Estimated Setups: {results['summary']['estimated_setups']}")

# Cost optimization opportunities
for opp in results['cost_optimization']:
    print(f"{opp['opportunity']}: {opp['cost_reduction']} savings")
```

## Inspection Checks Implemented

### ✓ Tolerances
- Standard vs precision tolerance distribution
- Over-tolerancing detection
- Cost impact analysis

### ✓ Internal Corners
- Minimum radius verification
- Tool-to-radius relationship
- EDM requirement detection

### ✓ Wall Thickness
- Material-specific minimums
- Aspect ratio checking
- Structural rigidity assessment

### ✓ Pockets and Cavities
- Depth-to-diameter ratio
- Stepped cavity recommendations
- Deep feature warnings

### ✓ Holes
- Standard size verification
- Depth limitations
- Edge distance checking
- Through-hole preferences

### ✓ Threads
- Standard size verification
- Depth requirements
- Wall thickness validation

### ✓ Material Selection
- Machinability rating
- Cost multiplier
- Tool wear assessment
- Thermal expansion warnings

### ✓ Setup Requirements
- Setup count estimation
- Cost per setup calculation
- Datum surface recommendations

### ✓ Tool Access
- Channel width verification
- Undercut detection
- Entry/exit relief recommendations

### ✓ Surface Finish
- Finish type recommendations
- Cost impact analysis
- Application-specific guidance

### ✓ Geometry Complexity
- Complexity cost impact
- Simplification opportunities
- Feature consolidation

### ✓ Standard Features
- Feature size standardization
- Tool change reduction
- Cost savings calculation

### ✓ Thermal Stability
- Thermal expansion warnings
- Stress relief requirements
- Structural rigidity checks

## Inspection Output

### Report Includes:
1. **Machinability Score** (0-100)
2. **Material Rating** (1-5 stars)
3. **Estimated Setups** (number)
4. **Critical Issues** - Must fix
5. **Warnings** - Should fix
6. **Suggestions** - Optimization opportunities
7. **Cost Optimization** - Top 3 opportunities with savings
8. **Passed Checks** - Compliant features

### Example Output:
```
CNC MACHINING DFM INSPECTION SUMMARY
======================================================================
Material: aluminum_6061
Machinability Score: 82.5/100
Material Rating: 5/5 stars
Estimated Setups: 2

Issues (Critical): 0
Warnings (Should Fix): 8
Suggestions (Optimization): 5
Passed Checks: 12
======================================================================

💰 TOP COST REDUCTION OPPORTUNITIES:

1. Relax tolerances to ±0.1mm for non-critical features
   Time Savings: 40%
   Cost Reduction: 60%
   Difficulty: Easy

2. Consolidate features to reduce setups
   Time Savings: 30%
   Cost Reduction: 35%
   Difficulty: Moderate

3. Add corner radii to eliminate EDM operations
   Time Savings: 20%
   Cost Reduction: 25%
   Difficulty: Easy
```

## Integration with Existing Tool

The CNC machining inspector integrates with the existing DFM Inspector:

- **Shared**: CAD parser, report generator, visualization
- **Process-specific**: CNC machining rules and checks
- **Compatible**: Can run alongside welding and general DFM inspections

## Next Steps

Ready to integrate additional manufacturing processes:
- ✓ Welding (AWS standards) - Complete
- ✓ CNC Machining (ISO 2768, ASME Y14.5) - Complete
- ⏳ Sheet Metal - Pending your document
- ⏳ Plastic Injection Molding - Pending
- ⏳ Investment Casting - Pending
- ⏳ Die Casting - Pending
- ⏳ Roll Forming - Pending
- ⏳ Wire Forms - Pending
- ⏳ Metal Injection Molding - Pending
- ⏳ Rotary Molding - Pending
- ⏳ Urethane Casting - Pending
- ⏳ Vacuum Forming - Pending

---

**Status**: ✓ Complete - CNC Machining DFM inspection fully integrated  
**Version**: 1.0.0  
**Date**: March 5, 2026  
**Standards**: ISO 2768, ASME Y14.5, ISO 1302, ISO 965, ISO 286
