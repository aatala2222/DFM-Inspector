# DFM Inspector

A comprehensive tool for checking product design manufacturability against industry standards and best practices.

## Features

- **Multi-format CAD Support**: Parse STEP, IGES, and STL files
- **Comprehensive DFM Checks**: 
  - Wall thickness analysis
  - Draft angle verification
  - Undercut detection
  - Corner radius inspection
  - Rib and boss design validation
  - Tolerance verification
- **Welding DFM Inspection** (NEW):
  - AWS standards compliance (D1.1, D1.2, D1.3, D1.6)
  - Groove angle verification
  - Skewed joint analysis
  - Weld access checking
  - Material-specific rules
  - Filler material recommendations
- **Industry Standards**: Based on ISO standards, AWS welding standards, and robotics best practices
- **Visual Reports**: Generate HTML, JSON, or text reports
- **3D Visualization**: Graphical inspection with issue highlighting
- **Customizable Rules**: Configure inspection criteria via YAML

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# For full functionality, install optional dependencies
pip install pythonocc-core  # For STEP/IGES support
pip install trimesh         # For STL support
pip install plotly          # For 3D visualization
```

## Quick Start

### General DFM Inspection
```bash
# Basic inspection
python main.py model.step

# Generate JSON report
python main.py model.step -f json -o report.json

# With visualization
python main.py model.stl --visualize

# Custom rules
python main.py model.iges -r custom_rules.yaml
```

### Welding DFM Inspection (NEW)
```bash
# Welding inspection for steel
python welding_main.py weldment.step -m steel_structural

# Aluminum welding inspection
python welding_main.py model.step -m aluminum_structural

# Show AWS standards
python welding_main.py --show-standards -m stainless_steel

# Get filler material recommendation
python welding_main.py --filler-material -m sheet_steel
```

## Usage

### Command Line

```bash
python main.py <input_file> [options]

Options:
  -o, --output PATH       Output report path (default: dfm_report.html)
  -f, --format FORMAT     Report format: html, json, text (default: html)
  -r, --rules PATH        Custom rules file (default: config/inspection_rules.yaml)
  -v, --visualize         Show 3D visualization
  --no-report            Skip report generation
```

### Python API

```python
from src import CADParser, DFMInspector, ReportGenerator

# Load CAD file
parser = CADParser('model.step')
parser.load()

# Run inspection
inspector = DFMInspector('config/inspection_rules.yaml')
results = inspector.inspect(parser)

# Generate report
report_gen = ReportGenerator()
report_gen.save_report(results, 'report.html', format='html')
```

## Configuration

Edit `config/inspection_rules.yaml` to customize inspection criteria:

```yaml
wall_thickness:
  min_thickness: 1.5  # mm
  max_thickness: 5.0
  uniform_variation_max: 2.0

draft_angles:
  min_draft_smooth: 1.0  # degrees
  min_draft_textured: 3.0
```

## DFM Rules

The tool checks against industry-standard DFM principles:

### General Manufacturing
1. **Wall Thickness**: Uniform thickness prevents warping and sink marks
2. **Draft Angles**: Facilitates part ejection from molds (1-5° recommended)
3. **Undercuts**: Detects features that prevent mold release
4. **Corner Radius**: Sharp corners create stress concentrations
5. **Ribs & Bosses**: Proper proportions prevent defects
6. **Tolerances**: Realistic tolerances reduce manufacturing costs

### Welding (AWS Standards)
1. **Groove Angles**: 50-65° depending on material for proper fusion
2. **Skewed Joints**: Beveling requirements based on joint angles
3. **Weld Access**: Adequate space for welding gun and arc visibility
4. **Material Thickness**: Minimum thickness per AWS D1.x standards
5. **Root Opening**: Proper gap for penetration
6. **Joint Design**: CJP vs PJP, fillet weld sizing

## Supported File Formats

- **STEP** (.step, .stp): Industry-standard CAD exchange format
- **IGES** (.iges, .igs): Legacy CAD exchange format
- **STL** (.stl): Mesh format for 3D printing and visualization

## Industry Standards

Based on:
- ISO 3691-4: Safety requirements for industrial trucks
- ISO 13849-1: Safety-related control systems
- AWS D1.1/D1.1M: Structural Welding Code - Steel
- AWS D1.2/D1.2M: Structural Welding Code - Aluminum
- AWS D1.3/D1.3M: Structural Welding Code - Sheet Steel
- AWS D1.6/D1.6M: Structural Welding Code - Stainless Steel
- AWS A2.4: Standard Symbols for Welding
- General DFM best practices for injection molding and CNC machining
- Amazon Robotics design guidelines (where applicable)

## Report Formats

### HTML Report
Interactive report with color-coded issues, warnings, and passed checks.

### JSON Report
Machine-readable format for integration with other tools.

### Text Report
Plain text format for command-line workflows.

## Extending the Tool

### Add Custom Rules

1. Edit `config/inspection_rules.yaml`
2. Add new rule categories and thresholds
3. Implement check methods in `src/dfm_inspector.py`

### Add New File Formats

1. Implement parser in `src/cad_parser.py`
2. Add format detection logic
3. Update documentation

## Troubleshooting

**PythonOCC not installing?**
- Try: `conda install -c conda-forge pythonocc-core`

**Visualization not working?**
- Install plotly: `pip install plotly`
- For offline use: `pip install kaleido`

**Large files slow?**
- Reduce mesh resolution in parser
- Use STL format for faster loading

## Contributing

Share your custom rules or improvements! This tool is designed to be extended with:
- Additional manufacturing processes
- Material-specific rules
- Industry-specific standards

## License

MIT License - See LICENSE file for details

## References

Content rephrased for compliance with licensing restrictions. Based on:
- [DFM Best Practices](https://www.analogydesign.co/blog/dfm-checklist)
- [Injection Molding Guidelines](https://sheridantech.io/2026/02/11/design-for-injection-moulding/)
- [ISO Standards](https://www.iso.org/standard/73933.html)
- [PythonOCC Documentation](https://pythonocc-doc.readthedocs.io/)
