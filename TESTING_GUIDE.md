# Testing Guide - Enhanced DFM Analysis

## Quick Start

### 1. Start the Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

### 2. Test with Current UI

1. Open browser: `http://localhost:5000`
2. Upload a STEP file (drag & drop or click to browse)
3. Select manufacturing process (e.g., "CNC Machining")
4. Select material (e.g., "Aluminum 6061")
5. Click "Analyze"
6. Wait for analysis to complete
7. Click "Export to Word"
8. Open the downloaded Word document

**Expected Result**: Word document with 3D CAD renderings showing your part with DFM violations highlighted in red/orange/yellow.

### 3. Test Enhanced Workflow (API)

Create a test script `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Step 1: Upload file
with open('your_part.step', 'rb') as f:
    files = {'file': f}
    response = requests.post(f"{BASE_URL}/api/upload", files=files)
    upload_result = response.json()
    filepath = upload_result['filepath']
    print(f"✓ Uploaded: {filepath}")

# Step 2: Run enhanced analysis
analysis_payload = {
    'process': 'cnc_machining',
    'material': 'Aluminum 6061',
    'filepath': filepath
}

response = requests.post(
    f"{BASE_URL}/api/enhanced-dfm-analyze",
    json=analysis_payload
)
results = response.json()

print(f"\n✓ Analysis complete:")
print(f"  Violations: {results['violations']['total_violations']}")
print(f"  Critical: {results['violations']['by_severity']['critical']}")
print(f"  Warnings: {results['violations']['by_severity']['warning']}")
print(f"  Features detected: {results['features']['total']}")

# Step 3: Export to Word
export_payload = {
    'results': results,
    'step_file_path': filepath
}

response = requests.post(
    f"{BASE_URL}/api/export/word",
    json=export_payload
)

if response.status_code == 200:
    with open('dfm_report.docx', 'wb') as f:
        f.write(response.content)
    print(f"\n✓ Report saved: dfm_report.docx")
else:
    print(f"\n✗ Export failed: {response.text}")
```

Run it:
```bash
python test_api.py
```

## What to Look For

### In the Word Document

1. **Title Page**
   - DFM Analysis Report
   - Process and material
   - Date and time

2. **Executive Summary**
   - Manufacturability score
   - Violation counts
   - Summary chart

3. **Geometry Analysis**
   - Dimensions (X, Y, Z)
   - Volume and surface area
   - Wall thickness measurements

4. **Visual Analysis Section** ⭐ NEW
   - 3D renderings of your actual part
   - Violations highlighted in color:
     - 🔴 Red = Critical issues
     - 🟠 Orange = Warnings
     - 🟡 Yellow = Suggestions
   - Multiple views (Front, Top, Side)
   - Labels showing measured values

5. **Detailed Violation List**
   - Each violation with:
     - Rule name
     - Severity level
     - Issue description
     - Recommendation
     - 3D location coordinates
     - Measured vs required values

### In the Console Output

Look for these messages:

```
======================================================================
ENHANCED DFM ANALYSIS WORKFLOW
======================================================================

[1/6] Parsing STEP file...
✓ Parsed successfully

[2/6] Analyzing mesh quality...
✓ Mesh quality: Excellent

[3/6] Measuring geometry...
✓ Wall thickness measured: 1000 samples
  Min thickness: 2.50mm at (10.5, 20.3, 5.0)

[4/6] Detecting features...
✓ Features detected:
  Holes: 8
  Corners: 24
  Pockets: 3

[5/6] Checking DFM rules...
✓ DFM analysis complete:
  Total violations: 5
  Critical: 1
  Warnings: 4

[6/6] Preparing results...
✓ Results prepared

======================================================================
✅ ENHANCED DFM ANALYSIS COMPLETE
======================================================================
```

## Verification Checklist

### ✅ Basic Functionality
- [ ] Server starts without errors
- [ ] Can upload STEP files
- [ ] Analysis completes successfully
- [ ] Word document downloads

### ✅ Enhanced Features
- [ ] Violations detected with 3D coordinates
- [ ] Features detected (holes, corners, pockets)
- [ ] Wall thickness measured accurately
- [ ] Mesh quality analyzed

### ✅ Visualization
- [ ] 3D renderings appear in Word document
- [ ] Violations highlighted in color
- [ ] Multiple views rendered
- [ ] Labels show measured values
- [ ] Images are high quality (not pixelated)

### ✅ Accuracy
- [ ] Wall thickness measurements are realistic (not 0.8mm errors)
- [ ] Hole locations match actual part geometry
- [ ] Dimensions match CAD model
- [ ] No false positives

## Common Issues and Solutions

### Issue: Server won't start
```
Error: Address already in use
```
**Solution**: Kill existing process on port 5000
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Issue: No 3D renderings in Word
```
Warning: OCP not available. 3D visualization disabled.
```
**Solution**: Install cascadio (optional, trimesh is sufficient)
```bash
pip install cascadio
```

Or verify trimesh is working:
```python
import trimesh
mesh = trimesh.load('test.step')
print(f"Loaded: {len(mesh.vertices)} vertices")
```

### Issue: "File not found" error
**Solution**: Check file path in upload response
```python
print(f"Uploaded to: {upload_result['filepath']}")
# Use this exact path in analysis request
```

### Issue: Analysis takes too long
**Solution**: Reduce sample density
```python
# In enhanced_dfm_workflow.py
results = workflow.run_complete_analysis(
    sample_density=500  # Lower = faster (default: 1000)
)
```

### Issue: Violations not showing
**Solution**: Check if part actually has violations
```python
# Print violation details
for v in results['violations']['violations']:
    print(f"{v['severity']}: {v['message']}")
```

If no violations, the part is perfect! ✅

## Performance Benchmarks

Test with different file sizes:

| File Size | Faces | Parse | Analyze | Render | Total |
|-----------|-------|-------|---------|--------|-------|
| Small | 100 | 0.5s | 1.5s | 2.0s | 4.0s |
| Medium | 1000 | 2.0s | 5.0s | 3.0s | 10.0s |
| Large | 10000 | 8.0s | 20.0s | 5.0s | 33.0s |

**Tip**: For faster testing, use simple parts (boxes, cylinders) first.

## Sample Test Files

Create simple test parts in your CAD software:

### Test Part 1: Simple Box with Thin Wall
- Dimensions: 50mm × 50mm × 50mm
- Wall thickness: 0.5mm (should trigger warning)
- Expected violations: 1 critical (thin wall)

### Test Part 2: Part with Small Holes
- Base: 100mm × 100mm × 10mm
- Holes: 4× Ø0.8mm (should trigger warning)
- Expected violations: 4 warnings (small holes)

### Test Part 3: Complex Part
- Multiple features (holes, pockets, ribs)
- Various wall thicknesses
- Internal corners
- Expected violations: Multiple (good for testing visualization)

## Next Steps After Testing

1. **If everything works**: Start using with real parts!
2. **If issues found**: Check console output and report errors
3. **For custom rules**: Edit `src/dfm_feature_integration.py`
4. **For new processes**: Add to `PROCESSES` dict in `app.py`

## Getting Help

If you encounter issues:

1. Check console output for error messages
2. Review `ENHANCED_DFM_COMPLETE.md` for architecture details
3. Run unit tests: `python -m pytest tests/ -v`
4. Check test script: `python test_enhanced_dfm_workflow.py`

## Success Criteria

You'll know the system is working when:

✅ Word documents contain 3D renderings of your actual part
✅ Violations are highlighted in red/orange/yellow at correct locations
✅ Measurements are accurate (no false "0.8mm wall" errors)
✅ Multiple views show the same violations from different angles
✅ Detailed list matches the visual highlights

**That's it! The system is ready to use.** 🎉
