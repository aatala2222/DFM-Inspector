# 🚀 DFM Inspector - Quick Start Guide

## What is DFM Inspector?

DFM Inspector is a comprehensive Design for Manufacturing (DFM) analysis tool that evaluates CAD files against industry-standard manufacturing guidelines. Upload a STEP file and get instant feedback on manufacturability, cost optimization opportunities, and design improvements.

## 🎯 Supported Manufacturing Processes

1. **CNC Machining** - 6 rules based on ISO 2768, ASME Y14.5
2. **Sheet Metal** - 6 rules from Amazon Robotics guidelines (930-00172)
3. **Injection Molding** - 5 rules from thermoplastic guidelines (930-00164)
4. **Die Casting** - 6 rules for HPDC & Permanent Mold (930-00166)
5. **Welding** - Industry best practices
6. Plus: Investment Casting, MIM, Rotational Molding, Wire Forming, Vacuum Forming

## 🏃 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
python app.py
```

### Step 3: Open Your Browser
Navigate to: **http://127.0.0.1:5000**

## 📁 Project Structure

```
DFM PRO/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── check_installation.py           # Verify installation
├── README.md                       # Project overview
│
├── src/                            # Source code
│   ├── step_parser.py             # STEP file parser
│   ├── cnc_machining_enhanced.py  # CNC analysis
│   ├── sheet_metal_enhanced.py    # Sheet metal analysis
│   ├── injection_molding_enhanced.py  # Injection molding
│   ├── die_casting_enhanced.py    # Die casting analysis
│   └── word_report_generator.py   # Word export
│
├── templates/                      # Web interface
│   └── interface.html             # Main UI
│
├── config/                         # Configuration files
│   ├── cnc_machining_rules.yaml
│   ├── welding_rules.yaml
│   └── inspection_rules.yaml
│
├── docs/                           # Documentation
│   ├── guides/                    # User guides
│   ├── enhancements/              # Enhancement history
│   └── rules/                     # Extracted design rules
│
├── reference_pdfs/                 # Source design guidelines
│   ├── 930-00164_R01.pdf         # Injection molding
│   ├── 930-00166_R01.pdf         # Die casting
│   └── 930-00172_R01-1.pdf       # Sheet metal
│
└── sample_files/                   # Test STEP files
    ├── 420-21634.STEP
    └── SM Sample.STEP
```

## 🎨 Features

### 1. Comprehensive Analysis
- Rule-by-rule evaluation with PASS/FAIL/WARNING status
- Detailed explanations of WHY each rule matters
- Specific measurements from your CAD geometry
- Cost impact calculations

### 2. Professional Reports
- Export to Word document (.docx)
- Color-coded status indicators
- Executive summary
- Detailed recommendations

### 3. Real-Time Feedback
- Upload STEP files
- Instant analysis (5-10 seconds)
- Interactive web interface
- Visual geometry preview

### 4. Industry Standards
- Based on ISO, ASME, and company-specific guidelines
- Quantified scrap rates and cost impacts
- Process-specific parameters
- Material-specific recommendations

## 📖 Documentation

- **Quick Start**: `docs/guides/QUICK_START.md`
- **Installation**: `docs/guides/INSTALLATION_GUIDE.md`
- **Web Interface**: `docs/guides/WEB_INTERFACE_GUIDE.md`
- **Adding Rules**: `docs/guides/HOW_TO_ADD_DESIGN_RULES.md`
- **All Enhancements**: `docs/ENHANCEMENTS_HISTORY.md`

## 🔧 Troubleshooting

### Can't connect to http://localhost:5000?
Try: **http://127.0.0.1:5000**

### Server won't start?
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Verify Python installation
python --version

# Check dependencies
python check_installation.py
```

### STEP file won't upload?
- Ensure file is valid STEP format (.step or .stp)
- Check file size (<50MB recommended)
- Verify file is not corrupted

## 🎓 Example Workflow

1. **Design your part** in CAD software (SolidWorks, Fusion 360, etc.)
2. **Export as STEP** file (.step or .stp format)
3. **Upload to DFM Inspector** at http://127.0.0.1:5000
4. **Select manufacturing process** (CNC, Sheet Metal, etc.)
5. **Review analysis** - see PASS/FAIL/WARNING for each rule
6. **Export Word report** for documentation
7. **Make design changes** based on recommendations
8. **Re-analyze** to verify improvements

## 💡 Key Design Rules Examples

### CNC Machining
- Wall thickness ≥1.0mm (aluminum), ≥1.5mm (steel)
- Internal corner radius ≥0.5mm (sharp corners require EDM)
- Standard hole sizes: 3, 4, 5, 6, 8, 10, 12mm
- Tolerances: ±0.1mm standard, ±0.02mm critical only

### Sheet Metal
- Material thickness: 0.5-3.0mm standard
- Hole diameter ≥1.33T (1.33× thickness)
- Hole to edge ≥2T
- Bend radius ≥1.0T or 0.6mm

### Injection Molding
- Wall thickness: 0.75-3.0mm optimal
- Draft angles: 1-3° minimum
- Uniform wall thickness (<25% variation)
- Ribs: 50-60% of wall thickness

### Die Casting
- Wall thickness: HPDC 3mm nominal, Perm Mold 4mm
- Draft angles: HPDC 1.5°, Perm Mold 3.0°
- Corner radius ≥0.5mm internal
- Machining stock: HPDC 1mm, Perm Mold 1.5-2mm

## 🚀 Next Steps

1. **Try the sample files** in `sample_files/` folder
2. **Read the guides** in `docs/guides/`
3. **Analyze your own parts**
4. **Export Word reports** for your team
5. **Customize rules** using `docs/guides/HOW_TO_ADD_DESIGN_RULES.md`

## 📞 Support

- Check documentation in `docs/` folder
- Review enhancement history in `docs/ENHANCEMENTS_HISTORY.md`
- See latest updates in `docs/LATEST_UPDATES.md`

## 🎉 You're Ready!

Start the server with `python app.py` and open http://127.0.0.1:5000 in your browser!
