# 🚀 DFM Inspector - Public Deployment Guide

## Quick Start: Deploy to Render.com (FREE)

Your DFM Inspector web application is ready to deploy! Follow these steps to get a public URL that anyone can access.

---

## Option 1: Render.com (Recommended - Easiest)

### Prerequisites
- GitHub account (free)
- Render.com account (free) - sign up at https://render.com

### Step-by-Step Instructions

#### 1. Push Your Code to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "DFM Inspector web application"

# Create a new repository on GitHub (go to github.com/new)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/dfm-inspector.git
git branch -M main
git push -u origin main
```

#### 2. Deploy on Render

1. Go to https://render.com and sign in
2. Click "New +" button → Select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `dfm-inspector` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

5. Click "Create Web Service"

#### 3. Wait for Deployment (5-10 minutes)

Render will:
- Clone your repository
- Install dependencies
- Start your application
- Provide a public URL like: `https://dfm-inspector.onrender.com`

#### 4. Access Your Application

Once deployed, you'll get a URL like:
```
https://dfm-inspector-xxxx.onrender.com
```

Share this URL with anyone - they can access it from anywhere!

---

## Option 2: Railway.app (Alternative)

### Steps:

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys
6. Get your public URL from the dashboard

**No configuration needed!** Railway automatically detects `requirements.txt` and `Procfile`.

---

## Option 3: Heroku (Classic Option)

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed

### Steps:

```bash
# Login to Heroku
heroku login

# Create new app
heroku create dfm-inspector

# Deploy
git push heroku main

# Open in browser
heroku open
```

Your app will be at: `https://dfm-inspector.herokuapp.com`

---

## Important Notes

### Free Tier Limitations

**Render.com Free Tier:**
- App sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (enough for continuous use)

**Railway.app Free Tier:**
- $5 free credit per month
- No sleep time
- Better for active development

**Heroku Free Tier:**
- Note: Heroku ended free tier in November 2022
- Now requires paid plan ($7/month minimum)

### File Upload Considerations

The current app uses temporary storage (`tempfile`). Uploaded files are:
- Stored temporarily during analysis
- Deleted when server restarts
- Not persisted between sessions

For production, consider:
- AWS S3 for file storage
- Database for analysis history
- User authentication

---

## Troubleshooting

### Build Fails on Render

**Issue**: `pythonocc-core` or `cadquery` installation fails

**Solution**: These packages require system dependencies. Update `render.yaml`:

```yaml
services:
  - type: web
    name: dfm-inspector
    env: python
    buildCommand: |
      apt-get update
      apt-get install -y libgl1-mesa-glx libglu1-mesa
      pip install -r requirements.txt
    startCommand: gunicorn app:app
```

### App Crashes on Startup

**Check logs**:
- Render: Click "Logs" tab in dashboard
- Railway: Click "Deployments" → View logs
- Heroku: `heroku logs --tail`

**Common issues**:
- Missing dependencies in `requirements.txt`
- Port binding (use `PORT` environment variable)

### Slow First Load

This is normal for free tiers. The app "wakes up" from sleep mode.

---

## Recommended: Render.com Deployment

For your use case, I recommend **Render.com** because:

✅ Completely free tier available
✅ No credit card required
✅ Automatic HTTPS
✅ Easy GitHub integration
✅ Simple dashboard
✅ Good for team sharing

---

## Next Steps After Deployment

1. **Test the public URL** - Upload a STEP file and run analysis
2. **Share with team** - Send them the public URL
3. **Monitor usage** - Check Render dashboard for traffic
4. **Upgrade if needed** - If you need 24/7 uptime, upgrade to paid tier ($7/month)

---

## Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] Render.com account created
- [ ] Web service created and connected to GitHub
- [ ] Build completed successfully
- [ ] Public URL accessible
- [ ] Test file upload and analysis
- [ ] Share URL with team

---

## Support

If you encounter issues:
1. Check Render logs for errors
2. Verify all files are committed to GitHub
3. Ensure `requirements.txt` and `render.yaml` are correct
4. Check Render community forum: https://community.render.com

---

**Your app is ready to deploy! Follow Option 1 (Render.com) for the fastest path to a public URL.**
