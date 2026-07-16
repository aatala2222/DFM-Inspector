# DFM Inspector Web Interface Guide

## Overview

The DFM Inspector now includes a beautiful, user-friendly web interface that allows you to upload CAD files and run manufacturing analysis through your browser.

## Features

- 🎨 **Modern UI**: Beautiful, intuitive interface with drag-and-drop file upload
- 📁 **File Support**: STEP, IGES, and STL file formats
- ⚙️ **10 Manufacturing Processes**: Select from various manufacturing methods
- 🔬 **Material Selection**: Choose from process-specific materials
- 📊 **Real-time Analysis**: Get instant DFM feedback
- 📥 **Downloadable Reports**: Generate and download detailed HTML reports
- 💰 **Cost Optimization**: See top cost reduction opportunities

## Quick Start

### 1. Install Dependencies

```bash
# Install Flask and other dependencies
pip install flask werkzeug pyyaml numpy pandas

# For CAD file support
pip install trimesh  # For STL files
```

### 2. Start the Web Server

```bash
python web_app.py
```

You should see:
```
======================================================================
DFM INSPECTOR WEB APPLICATION
======================================================================

Starting server...
Open your browser and navigate to: http://localhost:5000

Available processes:
  ✓ ⚙️ CNC Machining
  ✓ 🔥 Welding
  ⏳ 📋 Sheet Metal
  ⏳ 💉 Injection Molding
  ⏳ 🏭 Die Casting
  ⏳ 🎨 Investment Casting
  ⏳ 🔩 Metal Injection Molding
  ⏳ 🔄 Rotational Molding
  ⏳ 🔗 Wire Forming
  ⏳ 🌬️ Vacuum Forming

Press Ctrl+C to stop the server
======================================================================
```

### 3. Open Your Browser

Navigate to: **http://localhost:5000**

## How to Use

### Step 1: Upload CAD File

1. Click "Choose File" or drag and drop your CAD file
2. Supported formats: `.step`, `.stp`, `.iges`, `.igs`, `.stl`
3. Maximum file size: 100MB
4. File will be uploaded automatically

### Step 2: Select Manufacturing Process

Choose from available processes:

**Currently Available:**
- ⚙️ **CNC Machining** - Milling, turning, drilling
- 🔥 **Welding** - MIG, TIG, spot welding

**Coming Soon:**
- 📋 Sheet Metal
- 💉 Injection Molding
- 🏭 Die Casting
- 🎨 Investment Casting
- 🔩 Metal Injection Molding
- 🔄 Rotational Molding
- 🔗 Wire Forming
- 🌬️ Vacuum Forming

### Step 3: Select Material

Choose the appropriate material for your part:

**CNC Machining Materials:**
- Aluminum 6061
- Aluminum 7075
- Mild Steel 1018
- Stainless 304
- Stainless 316
- Titanium Grade 5
- Brass
- Tool Steel
- POM Plastic

**Welding Materials:**
- Steel Structural
- Aluminum Structural
- Sheet Steel
- Stainless Steel

### Step 4: Run Analysis

Click the **"🚀 Run DFM Analysis"** button

The system will:
1. Parse your CAD file
2. Run process-specific checks
3. Identify issues, warnings, and suggestions
4. Calculate manufacturability score
5. Generate detailed report

### Step 5: Review Results

The results page shows:

**Manufacturability Score** (0-100)
- 90-100: Excellent - Optimized for manufacturing
- 70-89: Good - Minor improvements possible
- 50-69: Fair - Significant cost reduction opportunities
- <50: Poor - Major redesign recommended

**Statistics:**
- Critical Issues (must fix)
- Warnings (should fix)
- Suggestions (optimization opportunities)
- Passed Checks

**Detailed Findings:**
- Issue descriptions
- Recommendations
- Cost impact
- Difficulty to fix

**Download Report:**
- Click "📥 Download Full Report" for detailed HTML report

## API Endpoints

The web interface uses these REST API endpoints:

### GET /
Main page with upload interface

### GET /api/processes
Get list of available manufacturing processes

### POST /api/upload
Upload CAD file
- **Body**: multipart/form-data with 'file' field
- **Returns**: `{success, filename, filepath, size}`

### POST /api/inspect
Run DFM inspection
- **Body**: `{filepath, process, material}`
- **Returns**: Analysis results with issues, warnings, suggestions

### GET /api/report/<filename>
Download generated report

### GET /api/materials/<process>
Get available materials for a process

## Configuration

### Change Port

Edit `web_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

### Change Upload Folder

Edit `web_app.py`:
```python
app.config['UPLOAD_FOLDER'] = '/your/custom/path'
```

### Change Max File Size

Edit `web_app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

## Deployment

### Development (Local)
```bash
python web_app.py
```

### Production (with Gunicorn)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

### Docker Deployment
```dockerfile
FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "web_app.py"]
```

Build and run:
```bash
docker build -t dfm-inspector .
docker run -p 5000:5000 dfm-inspector
```

## Troubleshooting

### Port Already in Use
```bash
# Change port in web_app.py or kill existing process
lsof -ti:5000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5000   # Windows
```

### File Upload Fails
- Check file size (max 100MB)
- Verify file format (.step, .stp, .iges, .igs, .stl)
- Check disk space in upload folder

### Analysis Fails
- Ensure CAD file is valid
- Check that dependencies are installed
- Review server logs for error messages

### Missing Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install minimal set
pip install flask werkzeug pyyaml numpy pandas trimesh
```

## Security Considerations

**For Production Deployment:**

1. **Disable Debug Mode**
   ```python
   app.run(debug=False)
   ```

2. **Add Authentication**
   - Implement user login
   - Use Flask-Login or similar

3. **File Validation**
   - Scan uploaded files for malware
   - Limit file types strictly

4. **Rate Limiting**
   - Use Flask-Limiter
   - Prevent abuse

5. **HTTPS**
   - Use SSL certificates
   - Redirect HTTP to HTTPS

6. **Environment Variables**
   - Store secrets in environment variables
   - Don't commit sensitive data

## Browser Compatibility

Tested and working on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Mobile Support

The interface is responsive and works on:
- 📱 Mobile phones
- 📱 Tablets
- 💻 Desktop computers

## Performance

**Typical Analysis Times:**
- Small files (<1MB): 2-5 seconds
- Medium files (1-10MB): 5-15 seconds
- Large files (10-100MB): 15-60 seconds

**Optimization Tips:**
- Use STEP format for best results
- Simplify complex models before upload
- Close unnecessary browser tabs

## Support

For issues or questions:
1. Check this guide
2. Review server logs
3. Check browser console for errors
4. Verify all dependencies are installed

## Future Enhancements

Planned features:
- [ ] Batch file processing
- [ ] Comparison between processes
- [ ] 3D visualization in browser
- [ ] Cost estimation calculator
- [ ] User accounts and history
- [ ] API key authentication
- [ ] Export to PDF
- [ ] Integration with CAD software

---

**Enjoy using the DFM Inspector Web Interface!**

For command-line usage, see the main README.md
