# Word Export Button Troubleshooting

## Issue: "Nothing happens" when clicking Export to Word

### Quick Fixes (Try in order):

#### 1. Check Browser Console
**Open browser console** (Press F12 or Right-click → Inspect → Console tab)

Look for error messages when you click the button. You should see:
```
Export button clicked
Current results: {process: "...", score: ...}
Sending export request...
```

If you see:
- `No analysis results to export` → **Run analysis first**
- `Failed to fetch` → **Server connection issue**
- Other errors → **See specific error below**

#### 2. Verify Analysis Was Run
The export button only works AFTER you've run an analysis.

**Steps:**
1. Upload a STEP file
2. Select manufacturing process
3. Click "Analyze" button
4. Wait for results to appear
5. THEN click "Export to Word Document"

#### 3. Restart Server
The server needs to be restarted to pick up code changes.

**Method 1: Kill and restart**
```bash
# Kill all Python processes
taskkill /F /IM python.exe

# Restart server
python app.py
```

**Method 2: Use Ctrl+C**
1. Go to terminal running server
2. Press Ctrl+C
3. Run `python app.py` again

#### 4. Check Server Logs
After clicking export button, check terminal for:
```
======================================================================
WORD EXPORT REQUEST RECEIVED
======================================================================
```

If you DON'T see this → **JavaScript not sending request**
If you DO see this → **Server-side error (check error message)**

#### 5. Test with Browser Developer Tools
Open browser console (F12) and run:
```javascript
// Check if results exist
console.log(window.currentAnalysisResults);

// Should show analysis data
// If undefined → run analysis first
```

### Common Issues and Solutions

#### Issue A: "No analysis results to export"
**Cause**: Button clicked before running analysis

**Solution**:
1. Upload STEP file
2. Select process (CNC, Sheet Metal, etc.)
3. Click "Analyze" button
4. Wait for results
5. Then click export

#### Issue B: Button does nothing, no console messages
**Cause**: JavaScript error or button not connected

**Solution**:
1. Hard refresh page: Ctrl+Shift+R
2. Clear browser cache
3. Try different browser
4. Check browser console for errors

#### Issue C: "Failed to fetch" error
**Cause**: Server not running or connection issue

**Solution**:
1. Check server is running: http://127.0.0.1:5000
2. Restart server
3. Check firewall settings
4. Try http://127.0.0.1:5000 instead of localhost

#### Issue D: Server error 500
**Cause**: Python error during report generation

**Solution**:
1. Check server terminal for error traceback
2. Common causes:
   - Missing `python-docx`: `pip install python-docx`
   - Missing `matplotlib`: `pip install matplotlib`
   - File permission issues
3. Check error message in terminal

#### Issue E: Download starts but file is corrupt
**Cause**: Error during document generation

**Solution**:
1. Check server logs for errors
2. Verify all dependencies installed:
   ```bash
   pip install python-docx matplotlib pillow
   ```
3. Try simpler analysis (fewer rules)

### Debugging Steps

#### Step 1: Verify Button Exists
Open browser console and run:
```javascript
document.querySelector('button[onclick="exportToWord()"]')
```
Should return the button element. If null → page not loaded correctly.

#### Step 2: Manually Trigger Export
Open browser console and run:
```javascript
exportToWord()
```
Watch console for error messages.

#### Step 3: Check Network Tab
1. Open browser DevTools (F12)
2. Go to "Network" tab
3. Click export button
4. Look for POST request to `/api/export/word`
5. Check status code and response

**Expected:**
- Status: 200 OK
- Type: application/vnd.openxmlformats...
- Size: ~500KB - 2MB

**If 400:** No analysis results sent
**If 500:** Server error (check terminal)
**If no request:** JavaScript not running

#### Step 4: Test Server Endpoint Directly
Use PowerShell to test:
```powershell
# First, run an analysis and save results
# Then test export endpoint

$body = @{
    results = @{
        process = "Test"
        score = 85
        material = "Aluminum"
        # ... other fields
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/export/word" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body `
    -OutFile "test_report.docx"
```

If this works → JavaScript issue
If this fails → Server issue

### Still Not Working?

#### Collect Debug Information:

1. **Browser Console Output**
   - Press F12
   - Click export button
   - Copy all console messages

2. **Server Terminal Output**
   - Copy last 50 lines from terminal
   - Include any error messages

3. **Network Request Details**
   - F12 → Network tab
   - Click export button
   - Right-click request → Copy → Copy as cURL

4. **System Information**
   - Browser: Chrome/Firefox/Edge version
   - Python version: `python --version`
   - Installed packages: `pip list | findstr "docx matplotlib"`

#### Temporary Workaround

If export still doesn't work, you can generate reports via Python:

```python
# In Python console or script
from src.word_report_generator import generate_word_report

# Your analysis results (copy from web interface)
results = {
    'process': 'Sheet Metal',
    'material': 'Aluminum',
    'score': 85,
    # ... rest of results
}

# Generate report
report_path = generate_word_report(results)
print(f"Report saved to: {report_path}")
```

### Prevention

To avoid this issue in future:

1. **Always restart server after code changes**
   ```bash
   # Ctrl+C to stop
   python app.py  # Start again
   ```

2. **Hard refresh browser after server restart**
   ```
   Ctrl+Shift+R
   ```

3. **Check console for errors regularly**
   ```
   F12 → Console tab
   ```

4. **Keep dependencies updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Quick Test Procedure

To verify export is working:

1. ✅ Server running: http://127.0.0.1:5000 loads
2. ✅ Upload sample file: `sample_files/420-21634.STEP`
3. ✅ Select process: "Sheet Metal"
4. ✅ Click "Analyze" - wait for results
5. ✅ Open browser console (F12)
6. ✅ Click "Export to Word Document"
7. ✅ Check console for "Export button clicked"
8. ✅ Check server terminal for "WORD EXPORT REQUEST RECEIVED"
9. ✅ File should download automatically

If any step fails, that's where the problem is!

### Contact Information

If still having issues, provide:
- Browser console output
- Server terminal output
- Steps you followed
- What you expected vs what happened
