"""
Check which dependencies are installed
"""
import sys

print("=" * 60)
print("DFM Inspector - Installation Check")
print("=" * 60)
print()

print(f"Python version: {sys.version}")
print()

# Check core dependencies
print("Core Dependencies:")
print("-" * 60)

dependencies = {
    'yaml': 'PyYAML',
    'numpy': 'NumPy',
    'scipy': 'SciPy',
    'matplotlib': 'Matplotlib',
    'pandas': 'Pandas',
    'jinja2': 'Jinja2',
}

for module, name in dependencies.items():
    try:
        __import__(module)
        print(f"✓ {name} installed")
    except ImportError:
        print(f"✗ {name} not installed - pip install {module if module != 'yaml' else 'pyyaml'}")

print()

# Check CAD libraries
print("CAD File Support:")
print("-" * 60)

try:
    from OCC.Core.STEPControl import STEPControl_Reader
    print("✓ PythonOCC installed - STEP/IGES support available")
except ImportError:
    print("✗ PythonOCC not installed - STEP/IGES not supported")
    print("  Install: conda install -c conda-forge pythonocc-core")

try:
    import trimesh
    print("✓ trimesh installed - STL support available")
except ImportError:
    print("✗ trimesh not installed - STL not supported")
    print("  Install: pip install trimesh")

try:
    import cadquery
    print("✓ CadQuery installed - Additional CAD support")
except ImportError:
    print("  CadQuery not installed (optional)")

print()

# Check visualization
print("Visualization:")
print("-" * 60)

try:
    import plotly
    print("✓ Plotly installed - 3D visualization available")
except ImportError:
    print("✗ Plotly not installed - 3D visualization not available")
    print("  Install: pip install plotly")

try:
    import vtk
    print("✓ VTK installed - Advanced visualization available")
except ImportError:
    print("  VTK not installed (optional)")

print()

# Summary
print("=" * 60)
print("Summary:")
print("-" * 60)

# Count installed
core_installed = 0
for module in dependencies.keys():
    try:
        __import__(module)
        core_installed += 1
    except ImportError:
        pass
total_core = len(dependencies)

print(f"Core dependencies: {core_installed}/{total_core} installed")

# Check if basic functionality is available
try:
    import yaml
    import numpy
    basic_ok = True
except ImportError:
    basic_ok = False

if basic_ok:
    print("✓ Basic functionality available")
else:
    print("✗ Install core dependencies first:")
    print("  pip install pyyaml numpy scipy matplotlib pandas jinja2")

# Check if any CAD support
try:
    import trimesh
    cad_ok = True
except ImportError:
    try:
        from OCC.Core.STEPControl import STEPControl_Reader
        cad_ok = True
    except ImportError:
        cad_ok = False

if cad_ok:
    print("✓ CAD file support available")
else:
    print("⚠ No CAD file support - install trimesh or pythonocc-core")

print()
print("=" * 60)
print("Ready to use!" if basic_ok and cad_ok else "Please install missing dependencies")
print("=" * 60)
