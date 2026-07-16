# 📦 DFM Inspector - Installation Guide

## What You Received

You've received the DFM Inspector application - a web-based tool for analyzing CAD files for manufacturability.

---

## Quick Start (3 Steps)

### Step 1: Install Python
Download and install Python 3.10 or higher from:
https://www.python.org/downloads/

**During installation:**
- ✅ Check "Add Python to PATH"
- ✅ Check "Install pip"

### Step 2: Install Dependencies
Open Command Prompt (Windows) or Terminal (Mac/Linux) in the extracted folder and run:

```bash
pip install -r requirements.txt
```

This installs all required libraries (takes 2-3 minutes).

### Step 3: Run the Application
```bash
python app.py
```

Open your browser and go to: **http://localhost:5000**

---

## Detailed Installation

### Windows

1. **Extract the ZIP file** to a folder (e.g., `C:\DFM_Inspector`)

2. **Open Command Prompt** in that folder:
   - Hold Shift + Right-click in the folder
   - Select "Open PowerShell window here" or "Open Command Prompt here"

3. **Install dependencies:**
   ```bash
   pip install flask trimesh numpy scipy matplotlib pyyaml werkzeug
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open browser:** http://localhost:5000

### Mac/Linux

1. **Extract the ZIP file**

2. **Open Terminal** in that folder:
   ```bash
   cd /path/to/extracted/folder
   ```

3. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python3 app.py
   ```

5. **Open browser:** http://localhost:5000

---

## What's Included

```
DFM_Inspector/
├── app.py                          # Main application
├── requirements.txt                # Dependencies list
├── templates/
│   └── interface.html             # Web interface
├── src/
│   ├── simple_cad_parser.py       # CAD file parser
│   ├── inspectors/
│   │   └── cnc_machining_inspector.py
│   ├── welding_inspector.py
│   └── ...
├── config/
│   ├── cnc_machining_rules.yaml   # CNC rules
│   └── welding_rules.yaml         # Welding rules
└── Documentation/
    ├── REAL_CAD_ANALYSIS_READY.md # Usage guide
    └── ...
```

---

## System Requirements

### Minimum:
- **OS:** Windows 10, macOS 10.14, or Linux
- **Python:** 3.10 or higher
- **RAM:** 4 GB
- **Disk:** 500 MB free space

### Recommended:
- **RAM:** 8 GB or more
- **Python:** 3.11
- **Browser:** Chrome, Firefox, or Edge (latest version)

---

## Using the Application

### 1. Upload CAD File
- Drag & drop or click to browse
- **Best support:** STL files (full geometry analysis)
- **Basic support:** STEP/IGES files

### 2. Select Manufacturing Process
- **CNC Machining** - Full analysis available
- **Welding** - Full analysis available
- **Others** - Basic analysis (coming soon)

### 3. Choose Material
- Process-specific materials available
- Affects recommendations and scoring

### 4. Run Analysis
- Click "Run DFM Analysis"
- View results:
  - Manufacturability score
  - Critical issues
  - Warnings
  - Cost optimization suggestions

---

## Features

### Real CAD Analysis
- ✅ Actual geometry parsing
- ✅ Dimension measurements
- ✅ Volume calculations
- ✅ Surface area analysis
- ✅ Wall thickness estimation

### Manufacturing Processes
- ✅ CNC Machining (200+ rules)
- ✅ Welding (AWS standards)
- ⏳ Sheet Metal (coming soon)
- ⏳ Injection Molding (coming soon)
- ⏳ 8 more processes

### Analysis Results
- Manufacturability score (0-100)
- Critical issues with recommendations
- Warnings and suggestions
- Cost optimization opportunities
- Geometry information

---

## Troubleshooting

### "Python not found"
**Solution:** Install Python from python.org and check "Add to PATH"

### "pip not found"
**Solution:** 
```bash
python -m ensurepip --upgrade
```

### "Module not found" errors
**Solution:** Install dependencies:
```bash
pip install flask trimesh numpy scipy matplotlib pyyaml werkzeug
```

### Port 5000 already in use
**Solution:** Change port in app.py (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Application won't start
**Solution:** Check Python version:
```bash
python --version
```
Must be 3.10 or higher.

---

## Sharing with Others on Your Network

Once running, others on your network can access it:

1. Find your IP address:
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`

2. Share the URL:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   Example: `http://192.168.1.221:5000`

3. Keep the application running on your computer

---

## Stopping the Application

Press `Ctrl+C` in the terminal/command prompt where it's running.

---

## Getting Help

### Documentation Files Included:
- `REAL_CAD_ANALYSIS_READY.md` - How to use the application
- `WEB_INTERFACE_GUIDE.md` - Interface guide
- `SHARING_GUIDE.md` - How to share with others

### Common Questions:

**Q: Can I use STEP files?**
A: Yes, but STL files provide better analysis. STEP files show basic info + general guidelines.

**Q: How accurate is the analysis?**
A: Very accurate for STL files. It measures actual geometry and applies industry-standard DFM rules.

**Q: Can I add more manufacturing processes?**
A: Yes! The framework is extensible. Contact the developer for customization.

**Q: Is internet required?**
A: No, runs completely offline on your computer.

**Q: Can multiple people use it?**
A: Yes, share the network URL (see "Sharing with Others" section above).

---

## Updates and Support

### To Update:
You'll receive a new ZIP file with updated version. Extract and replace files.

### For Support:
Contact the person who sent you this application.

---

## Quick Reference

### Start Application:
```bash
python app.py
```

### Access Application:
```
http://localhost:5000
```

### Stop Application:
```
Ctrl+C
```

### Reinstall Dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

---

## Security Notes

- Application runs locally on your computer
- No data is sent to external servers
- Files are processed locally
- Temporary files are deleted after analysis

---

## License and Credits

DFM Inspector - Manufacturing Design for Manufacturability Analysis

Built with:
- Flask (web framework)
- Trimesh (3D geometry processing)
- NumPy & SciPy (numerical computing)

Manufacturing standards:
- ISO 2768, ASME Y14.5 (CNC Machining)
- AWS D1.1, D1.2, D1.3, D1.6 (Welding)

---

## Success!

If you see this in your browser, you're ready to go:

```
🔍 DFM Inspector
Manufacturing Design Analysis Tool
```

Upload a CAD file and start analyzing!

---

**Need help? Check the included documentation files or contact your administrator.**
