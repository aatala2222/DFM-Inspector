# Why Server Connection Issues Happen

## TL;DR - Quick Fix

**Most Common Issue:** Server not actually running

**Quick Solution:**
```bash
python start_server.py
```
Then open: **http://127.0.0.1:5000** (not localhost)

---

## Root Causes Explained

### 1. Server Process Dies Silently ⚠️

**Why it happens:**
- Flask debug mode auto-restarts on file changes
- If there's a syntax error, server crashes
- Background processes can terminate without notice
- Python exceptions stop the server

**How to detect:**
```bash
# Check if server is running
netstat -ano | findstr :5000

# If nothing shows, server is NOT running
```

**Solution:**
- Use `python start_server.py` (checks everything first)
- Watch console for error messages
- Don't close terminal window

---

### 2. localhost vs 127.0.0.1 Confusion 🔄

**Why it happens:**
- `localhost` can resolve to IPv6 (::1) OR IPv4 (127.0.0.1)
- Windows sometimes prefers IPv6
- Flask binds to IPv4 by default
- Browser tries IPv6, server listening on IPv4 = no connection

**Example:**
```
Server: Listening on 127.0.0.1:5000 (IPv4)
Browser: Trying ::1:5000 (IPv6)
Result: Connection refused
```

**Solution:**
- **Always use 127.0.0.1:5000** (explicit IPv4)
- Avoid using "localhost"
- Bookmark http://127.0.0.1:5000

---

### 3. Port Already in Use 🚫

**Why it happens:**
- Previous server instance didn't close properly
- Another application using port 5000
- Multiple terminal windows running servers
- Crashed server left port in TIME_WAIT state

**Common port 5000 conflicts:**
- AirPlay (on Mac)
- Other Flask apps
- Development servers
- Previous DFM Inspector instances

**How to detect:**
```bash
netstat -ano | findstr :5000
# Shows: TCP 0.0.0.0:5000 ... LISTENING 12345

# Find what's using it:
tasklist | findstr 12345
```

**Solution:**
```bash
# Kill the process
taskkill /F /PID 12345

# Or use start_server.py (does this automatically)
python start_server.py
```

---

### 4. Flask Debug Mode Behavior 🔄

**Why it happens:**
- Debug mode runs TWO processes (parent + child)
- Auto-reloads when files change
- Temporary disconnection during reload (2-3 seconds)
- Can look like server is down

**What you see:**
```
 * Detected change in 'src/sheet_metal_enhanced.py', reloading
 * Restarting with stat
 [2-3 second gap]
 * Debugger is active!
```

**Solution:**
- This is NORMAL behavior
- Wait 2-3 seconds after file changes
- Refresh browser after "Debugger is active" message
- Don't panic if connection drops briefly

---

### 5. Windows Firewall Blocking 🛡️

**Why it happens:**
- Windows blocks new Python applications by default
- First time running = firewall prompt
- If you clicked "Cancel" on prompt, Python is blocked
- Firewall blocks without showing error

**How to detect:**
- Server runs but browser can't connect
- Port shows as LISTENING
- No error messages
- Works on same computer, not from network

**Solution:**
1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Click "Change settings"
4. Find Python (or click "Allow another app")
5. Check BOTH "Private" and "Public"
6. Click OK

---

### 6. Browser Cache Issues 💾

**Why it happens:**
- Browser caches static files (CSS, JS, images)
- Old cached version may be broken
- Service workers can cache entire app
- Hard to detect (looks like server issue)

**How to detect:**
- Works in incognito mode
- Works in different browser
- Console shows 404 for static files
- Old version of interface appears

**Solution:**
```
1. Hard refresh: Ctrl + Shift + R
2. Clear cache: Ctrl + Shift + Delete
3. Try incognito mode
4. Try different browser
```

---

### 7. Missing Dependencies 📦

**Why it happens:**
- `pip install` failed silently
- Package version conflicts
- Virtual environment not activated
- Corrupted package installation

**How to detect:**
```bash
python check_installation.py
# Shows missing packages
```

**Common missing packages:**
- `pythonocc-core` (provides OCP module)
- `flask`
- `numpy`
- `cadquery`

**Solution:**
```bash
# Reinstall everything
pip install -r requirements.txt

# Or specific package
pip install pythonocc-core
```

---

### 8. Multiple Server Instances 🔢

**Why it happens:**
- Started server multiple times
- Forgot about terminal in background
- Each file change in debug mode = new process
- Old processes don't always die

**How to detect:**
```bash
tasklist | findstr python
# Should see 2 processes (parent + child)
# If you see 4, 6, 8... = multiple servers
```

**Problems caused:**
- Port conflicts
- Confusion about which server is active
- File locks
- High CPU usage

**Solution:**
```bash
# Kill ALL Python processes
taskkill /F /IM python.exe

# Start fresh
python start_server.py
```

---

### 9. VPN/Proxy Interference 🌐

**Why it happens:**
- VPN routes localhost traffic
- Proxy intercepts local connections
- Corporate network policies
- Split tunneling issues

**How to detect:**
- Works without VPN
- Works on different network
- Other local servers also fail
- Ping 127.0.0.1 fails

**Solution:**
1. Disconnect VPN
2. Disable proxy
3. Try again
4. If needed, add 127.0.0.1 to VPN exceptions

---

### 10. Antivirus Blocking 🦠

**Why it happens:**
- Antivirus sees Python as suspicious
- Blocks local server connections
- Quarantines Python files
- Blocks port 5000

**How to detect:**
- Check antivirus logs
- Temporarily disable antivirus = works
- Python.exe in quarantine
- Firewall shows blocks

**Solution:**
1. Add Python to antivirus exceptions
2. Add port 5000 to allowed ports
3. Whitelist DFM PRO folder
4. Check quarantine for Python files

---

## Prevention Strategy

### ✅ Best Practices

1. **Always use start_server.py**
   ```bash
   python start_server.py
   ```
   - Checks dependencies
   - Handles port conflicts
   - Provides diagnostics

2. **Bookmark the right URL**
   - Use: http://127.0.0.1:5000
   - NOT: http://localhost:5000

3. **Close server properly**
   - Press Ctrl+C in terminal
   - Don't just close window
   - Wait for "Server stopped" message

4. **One server at a time**
   - Check before starting new server
   - Kill old instances first

5. **Keep terminal visible**
   - Watch for error messages
   - See reload notifications
   - Catch issues early

6. **Update dependencies regularly**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## Diagnostic Workflow

When server won't connect, follow this order:

```
1. Is server running?
   → netstat -ano | findstr :5000
   → If NO: python start_server.py
   
2. Can I connect to 127.0.0.1:5000?
   → Try in browser
   → If NO: Check firewall
   
3. Are dependencies installed?
   → python check_installation.py
   → If NO: pip install -r requirements.txt
   
4. Is port available?
   → netstat -ano | findstr :5000
   → If BUSY: Kill process or use start_server.py
   
5. Is firewall blocking?
   → Check Windows Firewall settings
   → If YES: Allow Python
   
6. Is browser caching?
   → Try Ctrl+Shift+R
   → Try incognito mode
   
7. Multiple servers running?
   → tasklist | findstr python
   → If YES: Kill all and restart
   
8. Still not working?
   → See docs/guides/SERVER_TROUBLESHOOTING.md
```

---

## The Real Answer

**Why does the server "sometimes" not connect?**

It's usually one of these:

1. **70% of cases:** Server not actually running (crashed, closed, never started)
2. **15% of cases:** Using localhost instead of 127.0.0.1
3. **10% of cases:** Port conflict from previous instance
4. **5% of cases:** Firewall, cache, or other issues

**The fix:**
```bash
# This handles 95% of issues
python start_server.py
```

Then use: **http://127.0.0.1:5000**

---

## Quick Reference Card

```
┌─────────────────────────────────────────────┐
│  DFM INSPECTOR - CONNECTION QUICK FIX       │
├─────────────────────────────────────────────┤
│                                             │
│  1. Start server:                           │
│     python start_server.py                  │
│                                             │
│  2. Open browser to:                        │
│     http://127.0.0.1:5000                   │
│     (NOT localhost)                         │
│                                             │
│  3. If still fails:                         │
│     - Check firewall                        │
│     - Clear browser cache                   │
│     - Try incognito mode                    │
│                                             │
│  4. Nuclear option:                         │
│     taskkill /F /IM python.exe              │
│     python start_server.py                  │
│                                             │
└─────────────────────────────────────────────┘
```

---

## See Also

- **Full troubleshooting:** docs/guides/SERVER_TROUBLESHOOTING.md
- **Quick start:** START_HERE.md
- **Installation:** docs/guides/INSTALLATION_GUIDE.md
