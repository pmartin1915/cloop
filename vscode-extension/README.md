# Ultrathink VS Code Extension

Self-improving development framework with AI-powered code analysis, integrated directly into VS Code.

## Features

- **Analyze Files**: Right-click any Python file → "Ultrathink: Analyze"
- **Learn Patterns**: Detect recurring issues and generate fixes
- **Scaffold Projects**: Generate FastAPI projects with learned improvements
- **Visual Feedback**: Sidebar panels for findings, patterns, and statistics
- **Auto-Analyze**: Optional analysis on file save

## Requirements

- Python 3.13+
- Ultrathink installed via Poetry
- AWS/Claude/Gemini API credentials configured

## Installation

1. Install Ultrathink:
```bash
cd ultrathink
poetry install
```

2. Install extension:
   - Open VS Code
   - Press F5 to launch extension development host
   - Or package: `vsce package` and install .vsix

## Configuration

Set in VS Code settings:

- `ultrathink.ultrathinkPath`: Path to Ultrathink directory
- `ultrathink.pythonPath`: Python interpreter path
- `ultrathink.autoAnalyze`: Auto-analyze on save (default: false)
- `ultrathink.defaultModel`: AI model (claude/gemini/bedrock)

## Usage

### Command Palette (Ctrl+Shift+P)

- `Ultrathink: Analyze Current File`
- `Ultrathink: Analyze Workspace`
- `Ultrathink: Learn Patterns`
- `Ultrathink: Scaffold New Project`
- `Ultrathink: Show Statistics`

### Sidebar

Click the Ultrathink icon in the activity bar to view:
- **Findings**: Issues grouped by severity
- **Patterns**: Learned patterns with frequency
- **Statistics**: Real-time metrics

### Status Bar

Shows pattern count. Click for detailed statistics.

## Development

```bash
npm install
npm run compile
npm run watch  # Auto-compile on changes
```

## License

MIT
