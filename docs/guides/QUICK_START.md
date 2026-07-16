# DFM Inspector - Quick Start Guide

## How to Run the DFM Inspector

### Simple 2-Step Process:

#### Step 1: Start the Application
Open your terminal/command prompt in the project folder and run:
```bash
python app.py
```

You'll see:
```
🔍 DFM INSPECTOR - Web Application
======================================================================
✓ Server starting...
✓ Open your browser: http://localhost:5000
📋 Available Processes:
  ✓ ⚙️ CNC Machining
  ✓ 🔥 Welding
  ✓ 📋 Sheet Metal
  ✓ 💉 Injection Molding
  ✓ 🏭 Die Casting
  ✓ 🎨 Investment Casting
  ✓ 🔩 Metal Injection Molding
  ✓ 🔄 Rotational Molding
  ✓ 🔗 Wire Forming
  ✓ 🌬️ Vacuum Forming
⌨️  Press Ctrl+C to stop
```

#### Step 2: Open Your Browser
Go to: **http://localhost:5000**

That's it! The DFM Inspector is now running.

---

## Using the DFM Inspector

### 1. Upload Your CAD File
- Drag & drop your STEP, STL, or IGES file
- Or click "Choose File" to browse
- Supported formats: `.step`, `.stp`, `.stl`, `.iges`, `.igs`

### 2. Select Manufacturing Process
Choose from 10 available processes:
- ⚙️ CNC Machining
- 🔥 Welding
- 📋 Sheet Metal
- 💉 Injection Molding
- 🏭 Die Casting
- 🎨 Investment Casting
- 🔩 Metal Injection Molding
- 🔄 Rotational Molding
- 🔗 Wire Forming
- 🌬️ Vacuum Forming

### 3. Select Material
Pick your material from the dropdown:
- Aluminum 6061, 7075, 5052
- Steel (Mild, Stainless 304, 316)
- Brass, Copper
- Titanium
- Plastics (ABS, Polycarbonate, Polypropylene, Nylon)

### 4. Run Analysis
Click **"🚀 Run DFM Analysis"**

### 5. Review Results
You'll see:
- **Manufacturability Score** (0-100)
- **Critical Issues** (must fix)
- **Warnings** (should review)
- **Suggestions** (cost optimization)
- **Passed Checks** (good to go)
- **Complete Rule-by-Rule Breakdown** (every design rule evaluated)

---

## Stopping the Application

Press **Ctrl+C** in the terminal to stop the server.

---

## Troubleshooting

### Problem: "Module not found" error
**Solution**: Install dependencies
```bash
pip install flask trimesh numpy scipy matplotlib pyyaml
```

### Problem: Port 5000 already in use
**Solution**: The app will try another port automatically, or you can stop other applications using port 5000.

### Problem: File upload fails
**Solution**: 
- Check file size (max 100MB)
- Ensure file format is supported (.step, .stp, .stl, .iges, .igs)
- Try a different file

### Problem: Dimensions show as 0 mm
**Solution**: 
- STEP files work best - dimensions extracted from coordinates
- For most accurate results, export your CAD as STL format
- Check that your CAD file is valid (not empty or corrupted)

---

## File Formats

### Best Results: STL Files
- Most accurate dimension extraction
- Full geometry analysis
- Wall thickness estimation
- Volume and surface area calculations

### Good Results: STEP Files
- Dimensions extracted from coordinate points
- Tested with your files: 595.0 × 468.1 × 124.4 mm accuracy
- Volume and surface area estimated

### Limited Results: IGES Files
- Basic dimension estimation
- May use default values if parsing fails

---

## What Gets Analyzed

### Geometry Measurements:
- Overall dimensions (X × Y × Z)
- Volume (mm³)
- Surface area (mm²)
- Estimated wall thickness

### Design Rules Checked:
- **CNC Machining**: 13 rules (wall thickness, hole depth ratios, corner radii, tolerances, surface finish, material machinability, etc.)
- **Sheet Metal**: 10 rules (bend radius, flange length, hole-to-bend distance, material formability, etc.)
- **Injection Molding**: 12 rules (wall thickness, draft angles, rib design, boss design, gate location, etc.)
- **Die Casting**: 6 rules (wall thickness, draft angles, fillet radii, material selection, etc.)
- **Wire Forming**: 8 rules (bend radius, leg length, springback, material formability, etc.)
- **Other Processes**: Essential DFM checks

### Industry Standards Referenced:
- ISO 2768 (General tolerances)
- ASME Y14.5 (Dimensioning and tolerancing)
- ISO 1302 (Surface finish)
- ISO 965 (Thread standards)
- ISO 286 (Fits and tolerances)
- SPI Standards (Injection molding)
- AWS D1.1-D1.6 (Welding)

---

## Example Workflow

1. **Start**: `python app.py`
2. **Open**: http://localhost:5000
3. **Upload**: Your STEP file (e.g., `405-07128_P01.STEP`)
4. **Select**: CNC Machining
5. **Material**: Aluminum 6061
6. **Analyze**: Click the button
7. **Review**: 
   - Score: 75.5/100
   - 0 critical issues
   - 5 warnings (wall thickness, hole depth, corner radii, etc.)
   - 3 suggestions (use standard hole sizes, apply ISO tolerances, etc.)
8. **Action**: Review each rule, make design changes as needed
9. **Re-analyze**: Upload modified design to verify improvements

---

## Network Access

### Local Only:
- http://localhost:5000
- Only accessible from your computer

### Network Access:
- http://192.168.1.221:5000 (your local IP)
- Accessible from other devices on your network
- Share with team members on same WiFi

---

## Tips for Best Results

1. **Use STEP files** for accurate dimensions
2. **Export STL** from CAD for most accurate geometry analysis
3. **Check file validity** in your CAD software before uploading
4. **Review all warnings** - they indicate cost/quality impacts
5. **Use standard materials** from the dropdown for best analysis
6. **Read the rationale** for each rule to understand why it matters
7. **Check cost impact** to prioritize which issues to fix first

---

## Need Help?

- Check `ENHANCED_DFM_RULES_SUMMARY.md` for detailed rule explanations
- Review `GEOMETRY_ANALYSIS_FIX.md` for dimension extraction details
- See `RULE_BY_RULE_REPORTING.md` for understanding the analysis output

---

**That's it! You're ready to analyze your designs for manufacturability.**

**Current Status**: ✅ Application running at http://localhost:5000
