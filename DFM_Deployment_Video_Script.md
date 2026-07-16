# DFM Inspector — Deployment Walkthrough Video Script

**Target Length:** 15-20 minutes
**Audience:** Engineers and TPMs who want to deploy similar Python tools internally
**Format:** Screen recording with voiceover + occasional webcam overlay
**Tools Suggested:** OBS Studio, Loom, or Camtasia

---

## 📋 Pre-Recording Checklist

- [ ] Clean desktop background
- [ ] Browser bookmarks bar hidden (or curated)
- [ ] All notifications silenced (Slack, Outlook, Teams)
- [ ] Microphone tested — no echo, no fan noise
- [ ] Have sample STEP file ready (`sample_files/sheet_metal_test.STEP`)
- [ ] PowerShell window pre-sized to ~1280x720
- [ ] Browser zoom at 110% for screen readability
- [ ] Test recording 30 seconds first to check audio/video quality

---

## 🎬 Scene 1: Introduction (0:00 - 1:30)

**[Webcam shot of presenter, then transition to screen]**

> "Hi, I'm Alex Atala, a Senior Product Development Engineer at Amazon Robotics. In this video, I'll walk you through how I deployed the DFM Inspector — a Python web app that analyzes 3D CAD files for manufacturing best practices. By the end, you'll know how to take any local Python tool and share it with your team through `code.amazon.com` and AgentSpaces."

**[Show the running app in browser briefly — user uploads a STEP file, sees analysis results]**

> "Here's the end goal — a working app where team members can upload STEP files and get DFM analysis based on Amazon Robotics design guidelines like 930-00172 for sheet metal and 930-00166 for casting."

**[Show flowchart diagram - DFM_Deployment_Flowchart.svg]**

> "We'll go through four phases: local development, source control backup, code review and merge, and finally sharing with the team. I'll show you what worked, what didn't, and the workarounds I found along the way."

---

## 🎬 Scene 2: Phase 1 - Local Development (1:30 - 4:00)

**[Screen recording: PowerShell in project directory]**

> "Phase 1 is the easy part — get the app running locally. I assume you already have your Python code working. The DFM Inspector is a Flask app, so getting it running is straightforward."

**[Type into PowerShell]**
```
pip install -r requirements.txt
```

> "First, install dependencies. The DFM Inspector uses Flask for the web framework, Trimesh and Cascadio for STEP file parsing, NumPy for math, and CadQuery with OpenCascade for B-Rep feature extraction. CadQuery is the heavyweight here — about 500 megabytes of native libraries — but it's what gives us accurate hole and bend detection."

**[Wait for install to complete, then run]**
```
python app.py
```

> "Now I run the app. The Flask dev server starts on port 5000."

**[Open browser to http://localhost:5000]**

> "I navigate to localhost colon 5000 and the DFM Inspector loads. Quick warning — if you're connected to Zscaler or some corporate VPNs, localhost may not work. Disconnect VPN to test the local app."

**[Upload sample_files/sheet_metal_test.STEP, run analysis]**

> "Let me upload a sample sheet metal part. The analyzer detects the holes, bends, material thickness, and runs all 14 design rules from the 930-00172 guideline. This part has 2mm thickness, three holes, and various bends. The system flags rules that fail — for example, hole-to-edge distance violations."

**[Show desktop shortcut creation]**

> "To make this one-click, I created a desktop shortcut. The launcher is just a batch file that starts the Flask server and opens the browser. After you create the shortcut, double-clicking it launches everything."

---

## 🎬 Scene 3: Phase 2 - Backing Up to code.amazon.com (4:00 - 8:00)

**[Switch to PowerShell]**

> "Now Phase 2 — getting the code into Amazon's source control. This protects your work and sets up for team collaboration."

**[Show Cisco AnyConnect connection in system tray]**

> "First — connect to Amazon VPN. Everything from here on requires VPN. I use Cisco AnyConnect."

**[Type into PowerShell]**
```
mwinit -f
```

> "Run mwinit with the -f flag for FIDO2 authentication. It prompts for my Midway PIN and a YubiKey touch. Once it succeeds, you'll see SSH certificate saved — that's what authenticates you to git.amazon.com for about 20 hours."

**[Open browser to code.amazon.com]**

> "Now I create a Brazil package. Open code.amazon.com and click Create Package. Select the Python Brazil template — that gives you a Python project skeleton with pytest, mypy, flake8 already configured."

**[Fill out the form]**

> "Fill in:
> - Package name in CamelCase — I used DFMAnalyzer
> - A brief description
> - Your team's Bindle for permissions — that's your security group
> - Export control: None for internal tools
> - Leave the other defaults
>
> Click Create. After a couple minutes, you'll have an empty package ready for your code."

**[Switch to PowerShell, clone the package]**

```
cd C:\Users\<your-username>
git clone ssh://git.amazon.com:2222/pkg/DFMAnalyzer
cd DFMAnalyzer
```

> "Clone the package. You'll see a skeleton with Config, setup.py, pyproject.toml, and a src folder with an empty package directory. Now I copy my code in. The skeleton expects your Python modules in src slash package_name slash."

**[Show the copy commands]**

```powershell
Copy-Item "C:\Path\To\YourProject\src\*.py" "src\dfm_analyzer\" -Force
Copy-Item "C:\Path\To\YourProject\app.py" "."
Copy-Item "C:\Path\To\YourProject\templates" "templates" -Recurse -Force
```

> "Watch out for one gotcha — Brazil has a file called `Config` (capital C). On Windows, the filesystem is case-insensitive, so a folder called `config` will conflict with `Config`. I renamed mine to `dfm_config` to avoid that."

```powershell
New-Item -ItemType Directory -Path "dfm_config" -Force | Out-Null
Copy-Item "C:\Path\To\YourProject\config\*" "dfm_config\" -Recurse -Force
```

**[Commit and push]**

```
git add .
git commit -m "feat: Initial import of DFM Inspector tool"
git push origin HEAD:refs/heads/initial-import
```

> "Commit and push to a feature branch — `initial-import`. Don't try to push directly to mainline. It's protected, and GitFarm will reject your push with a hook decline error. Always go through a feature branch."

**[Refresh code.amazon.com browser to show the code is now uploaded]**

> "Great — code is now on code.amazon.com on the initial-import branch. It's safely backed up."

---

## 🎬 Scene 4: Phase 3 - The Merge Bottleneck (8:00 - 11:00)

> "Phase 3 is where things got tricky for me. To merge a feature branch to mainline at Amazon, you create a Code Review — a CR — using the `cr` CLI tool. The problem? The cr tool is not available on Windows."

**[Show various failed installation attempts in PowerShell]**

```
toolbox install cr        # Not recognized
pip install cruxcr        # Not on PyPI
pip install amzn-cr       # Internal artifactory unreachable
```

> "I tried multiple ways to install cr from Windows. None worked. The Amazon CR creation workflow assumes you have a Cloud Desktop or proper internal Linux environment."

**[Show the protected branch error when trying to push to mainline]**

> "I also tried pushing directly to mainline, but GitFarm blocked it because mainline is protected."

> "If you hit the same situation, you have three options:"

**[Show three options on screen as bullets]**

> "**Option A: Get a Cloud Desktop.** A Cloud Desktop is a remote Linux VM Amazon provides. It has all the internal tools pre-installed. This is the right long-term answer."

> "**Option B: Ask a teammate.** If someone on your team has a Cloud Desktop, send them the package URL and branch name. They run `cr` from their machine. That's a 2-minute task for them."

> "**Option C: Stay on the feature branch.** Your code is safely backed up on `initial-import`. You can keep developing locally and push updates without merging to mainline. You'll just delay the pipeline setup."

> "I recommend Option A long-term. Talk to your manager about getting Cloud Desktop access. For this video, I'll proceed assuming you've completed the merge somehow."

---

## 🎬 Scene 5: Phase 4A - AgentSpaces Dashboard (11:00 - 14:00)

> "Now the fun part — sharing with the team. I'll show two paths. Path A is an AgentSpaces dashboard for documentation."

**[Open the DFM_RULES_REFERENCE.md file]**

> "First I curated all the DFM rules into a single markdown file — DFM_RULES_REFERENCE.md. It catalogs every rule the analyzer checks, organized by manufacturing process, with the standards they reference."

**[Scroll through the document showing each section]**

> "Sheet Metal rules per 930-00172, CNC machining rules, die casting per 930-00166 and NADCA, injection molding per the Shinkansan presentation, welding per AWS standards. Each section shows the rule, the threshold, and the cost impact of violations."

**[Switch to AgentSpaces in the browser]**

> "Now I create an AgentSpaces space. I upload the markdown file along with the original source PDFs from our Process Specs folder. AgentSpaces ingests them and builds context."

**[Type prompt to AgentSpaces]**

> "Then I prompt: 'Create an HTML dashboard from these DFM rules. Include tabs for each manufacturing process, color-coded rule cards for fail-warning-pass, and a search bar.'"

**[Show the generated dashboard]**

> "AgentSpaces generates a dashboard. It's not a live app — users can browse the rules but can't analyze STEP files. But it's a great quick-share for documentation. The URL is shareable with anyone in the team via Slack or email."

> "**Pro tip:** This took me about an hour total — even without finishing Phase 3. So if you need a quick win to share with your team this week, do Phase 1 then Phase 4A and skip the rest temporarily."

---

## 🎬 Scene 6: Phase 4B - Live App Deployment Options (14:00 - 17:30)

> "Path B is sharing the actual working app. There are three sub-paths based on effort budget."

### Method B1: Local Installer

> "**B1: Local installer.** Write a setup script that installs Python, dependencies, and creates the desktop shortcut on each user's machine. Distribute via Quip or SharePoint."

> "Pros: zero hosting infrastructure. Cons: each user installs separately. Effort: 1-2 days."

> "This is what I'd start with for a small team — 5 to 10 people."

### Method B2: Shared Cloud Desktop

> "**B2: Shared Cloud Desktop.** Run the app once on a team-shared Cloud Desktop and have everyone access via the URL. You configure auto-start so the Flask server stays up, open port 5000 to your corp network, and you're done."

> "Pros: centralized, instant updates. Cons: limited to corp network, single user at a time. Effort: 3-5 days."

> "Good for medium teams — 10 to 30 people."

### Method B3: Production Pipeline

> "**B3: Full production pipeline.** This is the proper Amazon-style deployment with a Pipeline at pipelines.amazon.com, an Apollo environment, gunicorn instead of Flask dev server, S3 for file storage, Midway auth, CloudWatch logging."

> "Pros: scales to hundreds of users, persistent, monitored. Cons: significant initial effort, ongoing maintenance, requires AppSec review. Effort: 1 to 3 weeks."

> "This is for tools that become critical infrastructure — used by 50+ engineers, integrated with other systems, etc."

**[Show flowchart again, highlighting the three B methods]**

> "Match the deployment method to your audience size and how critical the tool is."

---

## 🎬 Scene 7: Recap & Next Steps (17:30 - 19:30)

**[Switch to webcam, then back to slide]**

> "Let's recap. You've seen how to take a local Python app and turn it into something your team can use:"

**[Show summary slide]**

> "1. **Phase 1:** Get it running locally. Hours."
> "2. **Phase 2:** Push to code.amazon.com on a feature branch. Hour."
> "3. **Phase 3:** Merge to mainline via Cloud Desktop. Day."
> "4. **Phase 4A:** AgentSpaces dashboard for docs. Hour."
> "5. **Phase 4B:** Live deployment via local installer, shared Cloud Desktop, or full pipeline. Days to weeks."

> "If you're starting today and want fast results, do Phase 1 plus Phase 4A. That's a working local app for yourself plus a shareable rules dashboard for your team. Two hours of work."

> "If this becomes a real tool that your team relies on, work toward the full pipeline deployment in Phase 4B Method 3. Get yourself a Cloud Desktop, AppSec review, and ship it properly."

> "All the documentation, checklists, and source code are linked in the description. Reach out on Slack if you get stuck on any step — especially the Cloud Desktop setup, that's the biggest blocker most people hit."

> "Thanks for watching. Now go ship something."

**[End screen with links to documentation and Slack contact]**

---

## 🎬 Optional Scenes / B-Roll

**For longer/extended cut, add these:**

### Scene: Common Errors (3 min)
- Show each error message and fix from the troubleshooting table
- Most useful for new Amazon devs

### Scene: Code Architecture Walkthrough (5 min)
- Show the analyzer code structure
- Explain CadQuery feature extraction
- Show how rules are organized per manufacturing process

### Scene: Live Demo of Analysis (3 min)
- Upload a real bad part
- Walk through every flagged rule
- Show how the rule references back to 930-00172

### Scene: Updating the App (2 min)
- How to make code changes locally
- Sync to Brazil package
- Push update to feature branch

---

## 📦 Deliverables for the Video

When publishing, include in the description:

1. **Documentation links:**
   - `DEPLOYMENT_GUIDE.md` — full step-by-step guide
   - `DFM_Deployment_Checklist.md` — printable checklist
   - `DFM_Deployment_Flowchart.svg` — visual diagram
   - `DFM_RULES_REFERENCE.md` — rules catalog

2. **Source code link:**
   - `https://code.amazon.com/packages/DFMAnalyzer/`

3. **Internal references:**
   - 930-00172 sheet metal guideline
   - 930-00166 casting guideline
   - NADCA 11th Edition

4. **Tags:** `#DFM`, `#manufacturing`, `#python`, `#brazil`, `#code-amazon`, `#deployment`, `#tutorial`

---

## 🎤 Voice Recording Tips

- **Pace:** Aim for 130-150 words per minute. Faster than normal conversation.
- **Energy:** Stay enthusiastic. People notice flat delivery.
- **Pauses:** Pause briefly between major sections — gives viewers time to absorb.
- **Mistakes:** If you fumble a line, pause for 3 seconds, then redo. Easier to edit out.
- **Mic distance:** 6-8 inches from your mouth, slightly off-axis to avoid plosives.
- **Background noise:** Record in a quiet room. AC and computer fans audible? Try a different room or post-process noise removal.
