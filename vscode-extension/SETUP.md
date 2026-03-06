# Ultrathink VS Code Extension - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd vscode-extension
npm install
```

### 2. Configure Ultrathink Path

Create `.vscode/settings.json` in your workspace:

```json
{
  "ultrathink.ultrathinkPath": "c:\\Cloop\\ultrathink"
}
```

### 3. Compile Extension

```bash
npm run compile
```

### 4. Run Extension

Press **F5** in VS Code to launch the Extension Development Host.

## Testing the Extension

1. Open a Python file in the Extension Development Host
2. Right-click → "Ultrathink: Analyze Current File"
3. Check the Ultrathink sidebar (activity bar icon)
4. Run "Ultrathink: Learn Patterns" from command palette
5. Try "Ultrathink: Scaffold New Project"

## Configuration Options

In VS Code settings (Ctrl+,):

```json
{
  "ultrathink.ultrathinkPath": "c:\\Cloop\\ultrathink",
  "ultrathink.pythonPath": "python",
  "ultrathink.autoAnalyze": false,
  "ultrathink.defaultModel": "bedrock"
}
```

## Packaging for Distribution

```bash
npm install -g @vscode/vsce
vsce package
```

This creates `ultrathink-0.1.0.vsix` that can be installed via:
- VS Code → Extensions → Install from VSIX

## Development Workflow

1. Make changes to TypeScript files in `src/`
2. Run `npm run watch` for auto-compilation
3. Press Ctrl+R in Extension Development Host to reload
4. Check Debug Console for logs

## Troubleshooting

**Extension not activating:**
- Check Output → Ultrathink for errors
- Verify Ultrathink is installed: `poetry run ultrathink --help`

**Commands not working:**
- Ensure `ultrathink.ultrathinkPath` is set correctly
- Check that Poetry environment is activated

**No findings showing:**
- Run analysis first
- Check that Python files exist in workspace
- Verify Ultrathink CLI works: `poetry run ultrathink analyze --path .`
