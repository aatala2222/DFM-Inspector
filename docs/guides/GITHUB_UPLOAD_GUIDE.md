# 📤 How to Upload Your Project to GitHub

## What is "Pushing to GitHub"?

"Pushing" means uploading your project files from your computer to GitHub (a website that stores code).

Think of it like uploading files to Google Drive, but for code projects.

---

## Why Do This?

- ✅ Backup your code online
- ✅ Share with others
- ✅ Required for free hosting (Render.com needs to access your code)

---

## Step-by-Step Guide

### Step 1: Create GitHub Account

1. Go to https://github.com
2. Click "Sign up" (top right)
3. Enter:
   - Email address
   - Password
   - Username
4. Verify your email
5. Done! You have a GitHub account

---

### Step 2: Create a Repository

A repository is like a folder on GitHub for your project.

1. **Log in to GitHub**
2. **Click the "+" icon** (top right corner)
3. **Select "New repository"**

4. **Fill in the form:**
   ```
   Repository name: dfm-inspector
   Description: DFM Inspector - Manufacturing Analysis Tool
   Public: ✓ (selected)
   Add a README file: ☐ (NOT checked)
   ```

5. **Click "Create repository"**

6. **Keep this page open!** You'll see instructions - we'll use them next.

---

### Step 3: Upload Your Files

Now we'll upload your project files from your computer to GitHub.

#### 3a. Open Terminal in Your Project Folder

**Windows:**
1. Open File Explorer
2. Navigate to your project folder (where `app.py` is)
3. Click in the address bar (top)
4. Type `cmd` and press Enter
5. A black window opens - this is the terminal

**Alternative (Windows):**
1. Navigate to your project folder
2. Hold Shift + Right-click in the folder
3. Select "Open PowerShell window here"

#### 3b. Check if Git is Installed

In the terminal, type:
```bash
git --version
```

**If you see a version number (like "git version 2.40.0"):**
✅ Git is installed - continue to Step 3c

**If you see "command not found" or error:**
❌ Git is not installed - follow "Install Git" section below

---

### Install Git (If Needed)

**Windows:**
1. Go to https://git-scm.com/download/win
2. Download the installer
3. Run the installer
4. Click "Next" through all options (defaults are fine)
5. Restart your terminal
6. Try `git --version` again

**Mac:**
```bash
brew install git
```
Or download from https://git-scm.com/download/mac

**Linux:**
```bash
sudo apt-get install git
```

---

### Step 3c: Upload Commands

Copy and paste these commands **one at a time** into your terminal:

#### Command 1: Initialize Git
```bash
git init
```
**What this does:** Prepares your folder for Git

**You should see:** "Initialized empty Git repository"

---

#### Command 2: Add All Files
```bash
git add .
```
**What this does:** Selects all your files to upload

**You should see:** Nothing (that's normal!)

---

#### Command 3: Commit (Save) Files
```bash
git commit -m "Initial commit - DFM Inspector"
```
**What this does:** Packages your files ready to upload

**You should see:** List of files being committed

---

#### Command 4: Connect to GitHub

**IMPORTANT:** Replace `YOUR_USERNAME` with your actual GitHub username!

```bash
git remote add origin https://github.com/YOUR_USERNAME/dfm-inspector.git
```

**Example:** If your GitHub username is "john_smith":
```bash
git remote add origin https://github.com/john_smith/dfm-inspector.git
```

**What this does:** Tells Git where to upload

**You should see:** Nothing (that's normal!)

---

#### Command 5: Set Branch Name
```bash
git branch -M main
```
**What this does:** Names your main code branch

**You should see:** Nothing (that's normal!)

---

#### Command 6: Upload (Push) to GitHub
```bash
git push -u origin main
```

**What this does:** Actually uploads your files to GitHub!

**You'll be asked for:**
1. **Username:** Your GitHub username
2. **Password:** Your GitHub password

**Note:** When typing password, you won't see any characters - that's normal! Just type and press Enter.

**You should see:** Progress bars showing files being uploaded

---

### Step 4: Verify Upload

1. Go back to your GitHub repository page
2. Refresh the page (F5)
3. You should see all your files!

**Files you should see:**
- app.py
- requirements.txt
- templates/
- src/
- config/
- And more...

✅ **Success!** Your code is now on GitHub!

---

## Troubleshooting

### "git: command not found"
**Solution:** Install Git (see "Install Git" section above)

### "Permission denied"
**Solution:** Use a Personal Access Token instead of password:

1. Go to GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. Select scopes: `repo` (check all boxes under repo)
5. Generate token
6. Copy the token (you won't see it again!)
7. Use this token as your password when pushing

### "Repository not found"
**Solution:** Check the URL - make sure you replaced `YOUR_USERNAME` with your actual GitHub username

### "Already exists"
**Solution:** Your folder already has Git initialized. Skip `git init` and continue with other commands.

---

## What Happens Next?

Once your code is on GitHub:

1. ✅ Your code is backed up online
2. ✅ You can share the GitHub URL with others
3. ✅ Render.com can access it for deployment
4. ✅ Ready for Step 2: Deploy to Render.com!

---

## Quick Reference

### All Commands in Order:
```bash
git init
git add .
git commit -m "Initial commit - DFM Inspector"
git remote add origin https://github.com/YOUR_USERNAME/dfm-inspector.git
git branch -M main
git push -u origin main
```

**Remember:** Replace `YOUR_USERNAME` with your GitHub username!

---

## Visual Guide

```
Your Computer                GitHub.com               Render.com
┌─────────────┐             ┌──────────┐            ┌──────────┐
│             │             │          │            │          │
│  app.py     │   PUSH →    │  Backup  │   READ →   │  Public  │
│  templates/ │   ═══════>  │  Online  │  ═══════>  │  Website │
│  src/       │             │          │            │          │
│  config/    │             │          │            │          │
└─────────────┘             └──────────┘            └──────────┘
```

1. **Push:** Upload from your computer to GitHub
2. **Read:** Render.com reads from GitHub
3. **Deploy:** Render.com creates public website

---

## Next Steps

After successfully pushing to GitHub:

1. ✅ Your code is on GitHub
2. ⏭️ Next: Deploy to Render.com
3. 🌐 Get your public URL!

**Continue to:** DEPLOY_TO_FREE_HOSTING.md → Step 2

---

## Need Help?

### Check if it worked:
1. Go to https://github.com/YOUR_USERNAME/dfm-inspector
2. You should see all your files

### Still stuck?
- Make sure Git is installed: `git --version`
- Make sure you're in the right folder (where app.py is)
- Check your GitHub username is correct
- Try using a Personal Access Token instead of password

---

**Once you see your files on GitHub, you're ready for Step 2: Deploy to Render.com!**
