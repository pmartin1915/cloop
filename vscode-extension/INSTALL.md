# VSCode Extension Installation

## Quick Install

1. **Install dependencies:**
```bash
cd vscode-extension
npm install
```

2. **Compile TypeScript:**
```bash
npm run compile
```

3. **Install extension:**
   - Press `F5` in VSCode (opens Extension Development Host)
   - OR package and install:
```bash
npm install -g @vscode/vsce
vsce package
code --install-extension ultrathink-0.1.0.vsix
```

## Usage

### Right-Click → Generate Amazon Q Handoff

1. Right-click any file in editor or explorer
2. Select **"Ultrathink: Generate Amazon Q Handoff"**
3. Prompt is copied to clipboard
4. Click "Open Q" to paste directly into Amazon Q

### Keyboard Shortcut (Optional)

Add to `keybindings.json`:
```json
{
  "key": "ctrl+shift+u",
  "command": "ultrathink.generateHandoff",
  "when": "editorTextFocus"
}
```

## Configuration

Settings → Extensions → Ultrathink:

- **Ultrathink Path**: Path to Ultrathink installation (e.g., `C:\Cloop\ultrathink`)
- **Auto Analyze**: Analyze files on save
- **Project Profile**: `auto`, `medical`, `game`, or `general`

## Workflow

```
1. Working on Burn Wizard
2. Right-click file → "Generate Amazon Q Handoff"
3. Click "Open Q"
4. Paste (Ctrl+V)
5. Q analyzes with medical context
6. Apply fixes
```

Time: **5 seconds** vs 2 minutes manually
