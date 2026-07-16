# Server Connection Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: "Cannot connect to localhost:5000"

**Symptoms:**
- Browser shows "This site can't be reached"
- "Connection refused" error
- Page keeps loading but never connects

**Causes & Solutions:**

#### A. Server Not Running
**Check:**
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

**Solution:**
```bash
# Start the server
python app.py

# Or use the reliable startup script
python start_server.py
```

#### B. Wrong URL
**Problem:** Using `http://localhost:5000` when IPv6 is causing issues

**Solution:** Try these URLs in order:
1. **http://127.0.0.1:5000** (IPv4 loopback - most reliable)
2. **http://localhost:5000** (may resolve to IPv6 ::1)
3. **http://192.168.1.221:5000** (your network IP)

#### C. Port Already in Use
**Check:**
```bash
# Windows
netstat -ano | findstr :5000

# Find the process ID (PID) and kill it
taskkill /F /PID <PID>
```

**Solution:**
```bash
# Use the startup script - it handles this automatically
python start_server.py
```

#### D. Firewall Blocking
**Check:** Windows Firewall may be blocking Python

**Solution:**
1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Find Python and check both Private and Public
4. Or temporarily disable firewall to test

#### E. Browser Cache
**Problem:** Old cached data causing issues

**Solution:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Try incognito/private mode
3. Try a different browser

---

### Issue 2: "Server Starts Then Stops"

**Symptoms:**
- Server starts but immediately crashes
- Error messages in console
- Process terminates unexpectedly

**Causes & Solutions:**

#### A. Missing Dependencies
**Check:**
```bash
python check_installation.py
```

**Solution:**
```bash
pip install -r requirements.txt
```

#### B. Python Version
**Check:**
```bash
python --version
```

**Requirement:** Python 3.8 or higher

**Solution:**
```bash
# Install Python 3.8+
# Download from python.org
```

#### C. Import Errors
**Check:** Look for error messages like "ModuleNotFoundError"

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or install specific package
pip install flask
pip install cadquery
```

#### D. Syntax Errors in Code
**Check:** Look for Python syntax errors in console

**Solution:**
- Check recent code changes
- Restore from backup if needed
- Check file encoding (should be UTF-8)

---

### Issue 3: "Server Running But Page Won't Load"

**Symptoms:**
- Port 5000 shows as LISTENING
- Python process is running
- Browser still can't connect

**Causes & Solutions:**

#### A. Server Bound to Wrong Interface
**Check:** Look for "Running on 127.0.0.1:5000" in console

**Solution:** Ensure app.py has:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

#### B. Antivirus Blocking
**Check:** Antivirus may be blocking local connections

**Solution:**
1. Temporarily disable antivirus
2. Add Python to antivirus exceptions
3. Add port 5000 to allowed ports

#### C. VPN or Proxy
**Check:** VPN/proxy may be interfering

**Solution:**
1. Disconnect VPN
2. Disable proxy settings
3. Try again

---

### Issue 4: "Intermittent Connection Issues"

**Symptoms:**
- Sometimes works, sometimes doesn't
- Random disconnections
- Inconsistent behavior

**Causes & Solutions:**

#### A. Debug Mode Auto-Reload
**Problem:** Flask debug mode restarts server on file changes

**Solution:**
- This is normal behavior
- Wait 2-3 seconds after file changes
- Refresh browser after restart

#### B. Multiple Server Instances
**Check:**
```bash
# Windows - count Python processes
tasklist | findstr python

# Should see only 2 processes (parent + child for debug mode)
```

**Solution:**
```bash
# Kill all Python processes
taskkill /F /IM python.exe

# Restart server
python start_server.py
```

#### C. System Resources
**Check:** High CPU/memory usage

**Solution:**
- Close unnecessary applications
- Restart computer
- Check for memory leaks

---

## Quick Diagnostic Checklist

Run through this checklist when server won't connect:

```
□ 1. Is Python installed? (python --version)
□ 2. Are dependencies installed? (python check_installation.py)
□ 3. Is port 5000 available? (netstat -ano | findstr :5000)
□ 4. Is server running? (Check console for "Running on...")
□ 5. Tried http://127.0.0.1:5000 instead of localhost?
□ 6. Firewall allowing Python?
□ 7. Browser cache cleared?
□ 8. Tried different browser?
□ 9. VPN/proxy disabled?
□ 10. Only one server instance running?
```

---

## Reliable Startup Procedure

### Method 1: Use Startup Script (Recommended)
```bash
python start_server.py
```

This script:
- ✓ Checks dependencies
- ✓ Checks port availability
- ✓ Kills conflicting processes
- ✓ Provides clear diagnostics
- ✓ Starts server reliably

### Method 2: Manual Startup
```bash
# 1. Check dependencies
python check_installation.py

# 2. Kill any existing server
taskkill /F /IM python.exe

# 3. Start server
python app.py

# 4. Open browser to http://127.0.0.1:5000
```

### Method 3: Background Process (Advanced)
```bash
# Start in background (Windows)
start /B python app.py

# Or use PowerShell
Start-Process python -ArgumentList "app.py" -WindowStyle Hidden
```

---

## Testing Connection

### Test 1: Command Line
```bash
# Windows
curl http://127.0.0.1:5000

# Should return HTML content
```

### Test 2: PowerShell
```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 5000

# Should show TcpTestSucceeded: True
```

### Test 3: Browser Console
```javascript
// Open browser console (F12) and run:
fetch('http://127.0.0.1:5000')
  .then(r => r.text())
  .then(console.log)

// Should show HTML content
```

---

## Why These Issues Happen

### 1. localhost vs 127.0.0.1
- **localhost** can resolve to IPv6 (::1) or IPv4 (127.0.0.1)
- Some systems prefer IPv6, but Flask may bind to IPv4
- **Solution:** Always use 127.0.0.1 for reliability

### 2. Flask Debug Mode
- Debug mode runs TWO processes (parent + child)
- Auto-reloads on file changes
- Can cause temporary disconnections
- **Solution:** Wait 2-3 seconds after file changes

### 3. Port Conflicts
- Port 5000 is common (used by AirPlay on Mac, other apps)
- Previous server instances may not close cleanly
- **Solution:** Use start_server.py to handle conflicts

### 4. Windows Firewall
- Blocks new Python applications by default
- Requires explicit permission
- **Solution:** Allow Python through firewall

### 5. Browser Caching
- Browsers cache static files aggressively
- Can serve old/broken content
- **Solution:** Use Ctrl+Shift+R (hard refresh)

---

## Prevention Tips

### 1. Always Use start_server.py
```bash
python start_server.py
```
Handles most issues automatically.

### 2. Bookmark the Right URL
Use: **http://127.0.0.1:5000** (not localhost)

### 3. Close Server Properly
Press **Ctrl+C** in terminal (don't just close window)

### 4. One Server at a Time
Check for existing servers before starting new one

### 5. Keep Dependencies Updated
```bash
pip install --upgrade -r requirements.txt
```

---

## Still Not Working?

### Last Resort Steps:

1. **Complete Restart:**
```bash
# Kill all Python
taskkill /F /IM python.exe

# Restart computer
shutdown /r /t 0

# Start fresh
python start_server.py
```

2. **Reinstall Dependencies:**
```bash
# Remove and reinstall
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

3. **Check System:**
- Antivirus logs
- Windows Event Viewer
- Firewall logs
- Network adapter settings

4. **Try Different Port:**
Edit app.py:
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```
Then use: http://127.0.0.1:8080

---

## Getting Help

If still having issues, gather this information:

```bash
# 1. Python version
python --version

# 2. Installed packages
pip list

# 3. Port status
netstat -ano | findstr :5000

# 4. Python processes
tasklist | findstr python

# 5. Error messages
# Copy full error from console
```

Then check:
- docs/LATEST_UPDATES.md
- docs/ENHANCEMENTS_HISTORY.md
- README.md
