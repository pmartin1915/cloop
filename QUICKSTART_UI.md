# 🚀 Ultrathink UI - Quick Start Guide

## Launch the Dashboard

**Option 1: Double-click** `launch_ui.bat`

**Option 2: Command line**
```bash
cd c:\Cloop\ultrathink
poetry run ultrathink ui
```

Dashboard opens at: **http://localhost:8501**

---

## 🎯 Your First Session (5 minutes)

### Step 1: Analyze the Demo Code (2 min)

1. Go to **🔍 Analysis** tab
2. Enter path: `c:\Cloop\flawed_demo`
3. Keep "💾 Save to KB" checked
4. Click **🚀 Run Analysis**

You'll see findings for:
- Division by zero bugs
- Missing type hints
- Security issues (eval usage)
- Missing docstrings

### Step 2: Learn Patterns (1 min)

1. Go to **🧬 Learning** tab
2. Set threshold to `2` (default)
3. Click **🚀 Learn Patterns**

Ultrathink identifies recurring patterns and generates fixes!

### Step 3: Build a Project (2 min)

1. Go to **🚀 Projects** tab
2. Enter project name: `test_api`
3. Click **🚀 Generate Project**

Your new project has all learned improvements automatically applied!

---

## 💡 Daily Workflow

### Morning: Analyze Yesterday's Code
```
1. Open dashboard
2. Analysis tab → Enter your project path
3. Run analysis
```

### Afternoon: Learn & Improve
```
1. Learning tab → Learn patterns
2. Review what Ultrathink discovered
```

### Evening: Build New Features
```
1. Projects tab → Scaffold new service
2. All improvements auto-applied
3. Open in VS Code and code!
```

---

## 🎨 Dashboard Overview

### 🏠 Dashboard
- See total findings, patterns, improvements
- Visual charts of severity breakdown
- Top issues at a glance

### 🔍 Analysis
- Analyze files or folders
- Beautiful results with color-coded severity
- Save findings to knowledge base

### 🧬 Learning
- Identify recurring patterns
- Generate automatic fixes
- View learning statistics

### 🚀 Projects
- Scaffold FastAPI projects
- Auto-apply improvements
- One-click VS Code integration

### 📚 Knowledge
- Browse all findings
- Search and filter
- View patterns and improvements

---

## 🔧 Tips for VS Code + Amazon Q Workflow

1. **Keep Dashboard Open**: Run it in a browser tab while coding
2. **Quick Analysis**: After Q generates code, analyze it immediately
3. **Learn Often**: Run learning after every 2-3 analyses
4. **Handoff Ready**: Knowledge base persists between Q sessions
5. **Visual Feedback**: See patterns emerge across projects

---

## 🐛 Troubleshooting

**Port already in use?**
- The UI automatically finds an available port (8501-8510)
- If all ports are busy, you'll see a helpful error message
- Manually specify a port:
```bash
poetry run streamlit run ui/app.py --server.port 8520
```

**Can't see findings?**
- Make sure you ran an analysis first
- Check "Save to KB" was enabled

**Improvements not applying?**
- Run the Learning process first
- Need at least 2 occurrences of an issue

---

## 🎯 Next Steps

1. **Analyze your real projects**: Point it at your actual code
2. **Build knowledge base**: More analyses = better learning
3. **Generate projects**: Use scaffolding for new features
4. **Share with Q**: Mention findings in your Q conversations

---

**Happy coding! 🧠✨**

*The more you use Ultrathink, the smarter it gets!*
