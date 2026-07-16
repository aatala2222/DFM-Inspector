# DFM Inspector — One-Page Deployment Checklist

**Print this page. Check off as you go.**

---

## ☐ PHASE 1: Local Development (Hours)

- [ ] Install Python 3.11+ on Windows
- [ ] `pip install -r requirements.txt`
- [ ] Run `python app.py` — verify localhost:5000 works
- [ ] Upload a sample STEP file — verify analysis runs
- [ ] Create desktop shortcut for one-click launch
- [ ] **Disconnect VPN** when testing localhost (Zscaler blocks it)

✅ **Done when:** Double-click desktop icon → app opens in browser → can analyze a STEP file

---

## ☐ PHASE 2: Source Control Backup (Hour)

### Connect & Authenticate
- [ ] Connect to Amazon VPN (Cisco AnyConnect)
- [ ] Run `mwinit -f` in PowerShell
- [ ] Verify success: "SSH certificate was saved..."

### Create Package
- [ ] Open `https://code.amazon.com/`
- [ ] Click **Create Package** → Select **Python Brazil** template
- [ ] Fill form:
  - Package name (CamelCase, unique, e.g., `DFMAnalyzer`)
  - Description
  - Bindle (your team's)
  - Export Control: None
- [ ] Click Create

### Clone & Copy
- [ ] `git clone ssh://git.amazon.com:2222/pkg/<PackageName>`
- [ ] `cd <PackageName>`
- [ ] Copy code:
  - `*.py` → `src/<package_name>/`
  - `app.py`, `start_server.py`, `requirements.txt` → root
  - `templates/` → `templates/`
  - `rules/` → `rules/`
  - `config/*` → `dfm_config/` ⚠️ NOT `config/` (Brazil has `Config` file)
  - `tests/*.py` → `test/` (singular)

### Push to Feature Branch
- [ ] `git add .`
- [ ] `git commit -m "feat: Initial import of DFM Inspector tool"`
- [ ] `git push origin HEAD:refs/heads/initial-import` ⚠️ NOT mainline (protected)

✅ **Done when:** Code visible at `https://code.amazon.com/packages/<PackageName>/trees/initial-import`

---

## ☐ PHASE 3: Merge to Mainline (Day)

> ⚠️ **Blocker:** Requires `cr` CLI tool — NOT available on Windows.

Pick ONE option:

### Option A: Cloud Desktop (Best Long-Term)
- [ ] Request Cloud Desktop at `https://clouddesktop.amazon.com/`
- [ ] Wait for provisioning (manager approval may be needed)
- [ ] SSH into Cloud Desktop
- [ ] Run `mwinit` on Cloud Desktop
- [ ] Clone, checkout `initial-import`, run `cr --destination-branch mainline`
- [ ] Get reviewers to approve
- [ ] Merge

### Option B: Ask Teammate (Fastest)
- [ ] Send teammate the package URL + branch name
- [ ] Teammate runs `cr` from their Cloud Desktop
- [ ] Teammate reviews and merges

### Option C: Defer (Ship Path A First)
- [ ] Skip mainline merge for now
- [ ] Code stays safely on `initial-import` branch
- [ ] Keep developing locally; push updates to feature branch
- [ ] Come back when Cloud Desktop available

✅ **Done when:** `mainline` branch contains your code

---

## ☐ PHASE 4: Share With Team

### Path A: AgentSpaces Dashboard (Hour)

- [ ] Generate `DFM_RULES_REFERENCE.md` (already created)
- [ ] Open AgentSpaces — Create new Space
- [ ] Upload `DFM_RULES_REFERENCE.md` + source PDFs
- [ ] Prompt AgentSpaces: "Generate an HTML dashboard from these DFM rules"
- [ ] Get shareable URL
- [ ] Send URL to team via Slack/email

✅ **Done when:** Team can browse rules at AgentSpaces URL

### Path B: Live Working App (Days–Weeks)

Pick ONE deployment method:

#### B1: Local Installer (1-2 Days)
- [ ] Write `setup.ps1` that installs Python, deps, creates shortcut
- [ ] Write troubleshooting README
- [ ] Distribute via Quip/SharePoint
- [ ] Each team member runs setup script

#### B2: Shared Cloud Desktop (3-5 Days)
- [ ] Provision team Cloud Desktop
- [ ] Configure auto-start of Flask app
- [ ] Open port 5000 to corp network
- [ ] Set up process supervisor for auto-restart
- [ ] Document URL: `http://<host>:5000`

#### B3: Production Pipeline (1-3 Weeks)
- [ ] Mainline merge complete (Phase 3)
- [ ] Create pipeline at `https://pipelines.amazon.com/`
- [ ] Add stages: Build → Test → Beta → Approval → Prod
- [ ] Configure Apollo environment
- [ ] Replace Flask dev server with gunicorn
- [ ] Add Midway auth, S3 storage, CloudWatch logs
- [ ] AppSec review
- [ ] Launch

✅ **Done when:** Team can upload STEP files and get DFM analysis

---

## 🚨 Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `Permission denied (publickey)` on git | `mwinit -f` |
| `gitfarm-branch-protection hook declined` | Push to feature branch, not mainline |
| `Container cannot be copied onto existing leaf item` | Folder named same as file (e.g., `config` vs `Config`) — rename folder |
| `cr is not recognized` | Use Cloud Desktop, not Windows |
| `mwinit timeout` | Connect to Amazon VPN first |
| `localhost doesn't load` | Disconnect Zscaler/VPN, app is local-only |

---

## 📞 Escalation Path

| Stuck on... | Ask... |
|------------|--------|
| VPN setup | IT Helpdesk |
| Cloud Desktop access | Your manager |
| Bindle / package permissions | Your team's owner |
| Pipeline/Apollo setup | Senior dev on team |
| AppSec review | Security partner |

---

## 🎯 Minimum Viable Path

If you only have 1 day, skip to:
1. ✅ Phase 1 (local app working)
2. ✅ Phase 4A (AgentSpaces rules dashboard)

That gives your team a shareable rules reference. Phase 2-3 and live app come later.
