# Setup Guide

## Quick Start

### 1. Install Python Dependencies

```bash
# Install basic dependencies
pip install pyyaml numpy scipy matplotlib pandas jinja2

# Install CAD parsing libraries (choose based on your needs)
pip install trimesh  # For STL files (easiest to install)

# Optional: For STEP/IGES support (more complex installation)
pip install pythonocc-core  # May require conda
# OR
conda install -c conda-forge pythonocc-core

# Optional: For advanced visualization
pip install plotly vtk
```

### 2. Verify Installation

```bash
# Run basic tests
python tests/test_basic.py

# Try example usage
python example_usage.py
```

### 3. Test with Sample File

```bash
# If you have a CAD file
python main.py your_model.step

# Generate HTML report
python main.py your_model.step -o report.html

# With visualization
python main.py your_model.stl --visualize
```

## Installation Options

### Option 1: Minimal Installation (STL only)
```bash
pip install pyyaml numpy scipy matplotlib pandas jinja2 trimesh
```
This supports STL files and basic functionality.

### Option 2: Full Installation (All formats)
```bash
# Using conda (recommended for PythonOCC)
conda create -n dfm-inspector python=3.10
conda activate dfm-inspector
conda install -c conda-forge pythonocc-core
pip install pyyaml numpy scipy matplotlib pandas jinja2 trimesh plotly vtk
```

### Option 3: Docker (Coming Soon)
```bash
docker build -t dfm-inspector .
docker run -v $(pwd):/data dfm-inspector /data/model.step
```

## Troubleshooting

### PythonOCC Installation Issues

If `pip install pythonocc-core` fails:

1. **Use Conda** (recommended):
   ```bash
   conda install -c conda-forge pythonocc-core
   ```

2. **Use pre-built wheels** (Windows):
   - Download from: https://github.com/tpaviot/pythonocc-core/releases
   - Install: `pip install pythonocc_core-7.7.0-*.whl`

3. **Skip STEP/IGES support**:
   - Use STL files instead
   - Convert STEP to STL using FreeCAD or online converters

### Import Errors

If you get `ModuleNotFoundError`:
```bash
# Make sure you're in the project root directory
cd /path/to/dfm-inspector

# Install missing package
pip install <package-name>
```

### Visualization Not Working

If 3D visualization doesn't work:
```bash
# Install plotly
pip install plotly

# For offline use
pip install kaleido
```

## Platform-Specific Notes

### Windows
- Use Anaconda for easiest PythonOCC installation
- PowerShell or CMD both work

### macOS
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10

# Use conda for PythonOCC
brew install miniconda
conda install -c conda-forge pythonocc-core
```

### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-dev

# Install packages
pip3 install -r requirements.txt

# For PythonOCC
conda install -c conda-forge pythonocc-core
```

## Verifying Your Installation

Run this Python script to check what's available:

```python
import sys

print("Python version:", sys.version)

# Check core dependencies
try:
    import yaml
    print("✓ PyYAML installed")
except ImportError:
    print("✗ PyYAML not installed")

try:
    import numpy
    print("✓ NumPy installed")
except ImportError:
    print("✗ NumPy not installed")

# Check CAD libraries
try:
    from OCC.Core.STEPControl import STEPControl_Reader
    print("✓ PythonOCC installed (STEP/IGES support)")
except ImportError:
    print("✗ PythonOCC not installed (STEP/IGES not supported)")

try:
    import trimesh
    print("✓ trimesh installed (STL support)")
except ImportError:
    print("✗ trimesh not installed (STL not supported)")

# Check visualization
try:
    import plotly
    print("✓ Plotly installed (3D visualization)")
except ImportError:
    print("✗ Plotly not installed (visualization limited)")
```

Save as `check_installation.py` and run:
```bash
python check_installation.py
```

## Next Steps

1. Review `README.md` for usage instructions
2. Customize `config/inspection_rules.yaml` for your needs
3. Add your custom rules using `CUSTOM_RULES_TEMPLATE.md`
4. Test with your CAD files

## Getting Help

- Check the README.md for usage examples
- Review example_usage.py for code samples
- See CUSTOM_RULES_TEMPLATE.md for adding rules
