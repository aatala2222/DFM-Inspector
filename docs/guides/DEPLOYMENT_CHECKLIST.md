# ✅ Deployment Checklist - Get Your Public URL

## Pre-Deployment Verification

Run this command to verify everything is ready:
```bash
python verify_deployment.py
```

Expected output: ✅ ALL REQUIRED FILES PRESENT

---

## 🚀 Deployment Steps

### ☐ Step 1: Set Up Git (2 minutes)

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "DFM Inspector - Initial deployment"
```

**Verify**: Run `git status` - should show "nothing to commit, working tree clean"

---

### ☐ Step 2: Create GitHub Repository (3 minutes)

1. Go to: https://github.com/new
2. Repository name: `dfm-inspector`
3. Description: "DFM Inspector - Manufacturing Design Analysis Tool"
4. Visibility: Public (or Private if you prefer)
5. **DO NOT** check "Initialize with README"
6. Click "Create repository"

**Verify**: You should see an empty repository with setup instructions

---

### ☐ Step 3: Push Code to GitHub (2 minutes)

Copy the commands from GitHub (replace YOUR_USERNAME with your actual username):

```bash
git remote add origin https://github.com/YOUR_USERNAME/dfm-inspector.git
git branch -M main
git push -u origin main
```

**Verify**: Refresh GitHub page - you should see all your files

---

### ☐ Step 4: Deploy on Render.com (5 minutes)

#### 4a. Sign Up
1. Go to: https://render.com
2. Click "Get Started"
3. Sign up with GitHub account
4. Authorize Render to access your repositories

#### 4b. Create Web Service
1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect GitHub"
4. Find and select `dfm-inspector` repository
5. Click "Connect"

#### 4c. Configure Service
Render should auto-fill most fields. Verify:

- **Name**: `dfm-inspector` (or your choice)
- **Region**: Oregon (or closest to you)
- **Branch**: `main`
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements-cloud.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
- **Instance Type**: Free

#### 4d. Deploy
1. Click "Create Web Service"
2. Wait for build (5-10 minutes first time)
3. Watch the logs for progress

**Verify**: Build should complete with "Your service is live 🎉"

---

### ☐ Step 5: Get Your Public URL (1 minute)

1. Look at the top of your Render dashboard
2. You'll see a URL like: `https://dfm-inspector-xxxx.onrender.com`
3. Click the URL to open your app

**Verify**: You should see the DFM Inspector interface

---

### ☐ Step 6: Test Your Deployment (3 minutes)

1. **Upload a file**: Drag a STEP file to the upload zone
2. **Select process**: Click "CNC Machining" or "Welding"
3. **Choose material**: Select from dropdown
4. **Run analysis**: Click "Run DFM Analysis"
5. **View results**: Check the manufacturability score and recommendations

**Verify**: Analysis completes and shows results

---

### ☐ Step 7: Share With Team (1 minute)

Copy your public URL and share it with team members:

```
https://dfm-inspector-xxxx.onrender.com
```

They can access it immediately - no installation needed!

**Verify**: Open URL in incognito/private browser window to test public access

---

## 📋 Quick Reference

### Your Public URL
```
https://dfm-inspector-xxxx.onrender.com
```
(Replace xxxx with your actual subdomain)

### GitHub Repository
```
https://github.com/YOUR_USERNAME/dfm-inspector
```

### Render Dashboard
```
https://dashboard.render.com
```

---

## 🔧 Troubleshooting

### Build Fails

**Check**: Render logs (click "Logs" tab)

**Common issues**:
- Missing dependencies → Verify `requirements-cloud.txt` exists
- Python version → Should be 3.11
- Build command → Should use `requirements-cloud.txt`

**Solution**: Check `DEPLOYMENT_GUIDE.md` for detailed troubleshooting

### App Won't Start

**Check**: Render logs for startup errors

**Common issues**:
- Port binding → Verify start command includes `--bind 0.0.0.0:$PORT`
- Missing files → Verify all files pushed to GitHub
- Import errors → Check Python dependencies

**Solution**: Try deploying on Railway.app instead (simpler)

### Slow First Load

**This is normal!** Free tier apps sleep after 15 minutes of inactivity.

**First request**: 30-60 seconds (waking up)
**Subsequent requests**: <2 seconds

**Solution**: Upgrade to paid tier ($7/month) for instant response

---

## 🎯 Alternative: Railway.app (Faster!)

If Render.com has issues, try Railway.app:

1. Go to: https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `dfm-inspector`
6. Click "Deploy"
7. Click "Generate Domain"

**Done!** Railway auto-configures everything.

---

## ✅ Success Criteria

You're done when:

- ☐ Code is on GitHub
- ☐ App is deployed on Render/Railway
- ☐ Public URL is accessible
- ☐ File upload works
- ☐ Analysis runs successfully
- ☐ Results display correctly
- ☐ Team members can access the URL

---

## 📞 Need Help?

### Documentation
- `START_DEPLOYMENT.md` - Quick start
- `QUICK_DEPLOY.md` - Step-by-step guide
- `DEPLOYMENT_GUIDE.md` - Detailed troubleshooting
- `DEPLOYMENT_STATUS.md` - Technical overview

### Platform Support
- Render: https://community.render.com
- Railway: https://discord.gg/railway
- GitHub: https://docs.github.com

### Verification
```bash
python verify_deployment.py
```

---

## 🎉 You're Ready!

Follow the steps above in order. Total time: ~15 minutes.

**Result**: A public URL that anyone can use to analyze CAD files for manufacturability.

**Start with Step 1 above!**
