# Simple Test Instructions

## The Problem
Extension isn't showing commands because it's not activating properly.

## Solution: Test Directly from CLI

Skip the VS Code extension for now and test Ultrathink CLI directly:

### 1. Test Analysis
```bash
cd c:\Cloop\ultrathink
poetry run ultrathink analyze --path vscode-extension\test-file.py
```

### 2. Test Learning
```bash
poetry run ultrathink learn --threshold 2
```

### 3. Test Stats
```bash
poetry run ultrathink stats
```

### 4. Test Scaffolding
```bash
poetry run ultrathink scaffold --name test-project --author "Your Name"
```

## Why Skip Extension for Now?

The extension is complete but needs debugging:
- Activation events may need adjustment
- Path configuration needs testing
- VS Code extension host environment is complex

## Alternative: Use VS Code Tasks Instead

Create `.vscode/tasks.json` in your workspace:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Ultrathink: Analyze File",
      "type": "shell",
      "command": "cd c:\\Cloop\\ultrathink && poetry run ultrathink analyze --path ${file}",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Ultrathink: Learn Patterns",
      "type": "shell",
      "command": "cd c:\\Cloop\\ultrathink && poetry run ultrathink learn --threshold 2",
      "presentation": {
        "reveal": "always"
      }
    }
  ]
}
```

Then use `Ctrl+Shift+P` → "Tasks: Run Task" → Select Ultrathink task.

This gives you Ultrathink in VS Code without the extension complexity.
