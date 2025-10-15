# Ultrathink Dashboard

Beautiful web interface for Ultrathink - your AI-powered code quality companion.

## 🚀 Quick Start

### Option 1: Using CLI
```bash
poetry run ultrathink ui
```

### Option 2: Using Batch Script (Windows)
```bash
launch_ui.bat
```

### Option 3: Direct Streamlit
```bash
poetry run streamlit run ui/app.py
```

The dashboard will open automatically at **http://localhost:8501**

## 📱 Features

### 🏠 Dashboard
- Real-time statistics on findings, patterns, and improvements
- Visual severity breakdown with charts
- Top issues at a glance
- Quick navigation to all features

### 🔍 Analysis
- Analyze files or directories for code issues
- Live progress indicators
- Beautiful results visualization
- Severity-coded findings
- Save to knowledge base option

### 🧬 Learning
- Identify recurring patterns automatically
- Configure detection thresholds
- View generated patches
- Learning statistics and metrics
- Top issues tracking

### 🚀 Projects
- Scaffold new FastAPI projects
- Automatic improvement application
- One-click VS Code integration
- Project configuration wizard
- See exactly what improvements were applied

### 📚 Knowledge
- Browse all findings, patterns, and improvements
- Search and filter capabilities
- Knowledge base management
- Export/import (coming soon)

## 🎨 Design Philosophy

- **Clean & Intuitive**: No learning curve, just start using
- **Visual Feedback**: Charts, colors, and icons for quick understanding
- **Workflow-Oriented**: Guides you through Analyze → Learn → Build
- **VS Code Integration**: Works alongside your IDE, not instead of it

## 🔧 Configuration

The UI uses your existing `ultrathink.yaml` configuration. No additional setup needed!

## 💡 Tips

1. **Keep it running**: Leave the dashboard open while coding in VS Code
2. **Quick analysis**: Drag-drop files directly into the Analysis tab
3. **Watch patterns emerge**: Run analysis on multiple projects to see patterns
4. **One-click scaffolding**: Generate new projects with all improvements applied

## 🐛 Troubleshooting

**Dashboard won't start?**
- Ensure Streamlit is installed: `poetry install`
- The UI automatically finds an available port (8501-8510)
- If all ports busy: `poetry run streamlit run ui/app.py --server.port 8520`

**Can't see findings?**
- Run an analysis first from the Analysis tab
- Check that `--save-findings` is enabled (default: on)

**Improvements not applying?**
- Run the Learning process from the Learning tab
- Ensure threshold is set appropriately (default: 2)

## 🚀 Next Steps

1. **Analyze** your existing code
2. **Learn** patterns from findings
3. **Build** new projects with improvements

Happy coding! 🧠✨
