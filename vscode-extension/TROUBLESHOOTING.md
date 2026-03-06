# Troubleshooting

## Right-click menu not showing

**Solution:**
1. In Extension Development Host, press **Ctrl+R** to reload window
2. Or close and press **F5** again in main VS Code window
3. Make sure you're right-clicking in the editor (not just file explorer)

## Commands to try instead:

1. **Command Palette (Ctrl+Shift+P):**
   - Type: "Ultrathink: Analyze Current File"
   - This always works

2. **Or use the sidebar:**
   - Click Ultrathink icon in activity bar (left side)
   - Use the refresh button in panels

## Quick Test Without Right-Click:

1. Open `test-file.py`
2. Press `Ctrl+Shift+P`
3. Type "Ultrathink: Analyze"
4. Select "Ultrathink: Analyze Current File"
5. Wait for notification
6. Check Ultrathink sidebar

## If extension doesn't activate:

1. Check Debug Console (Ctrl+Shift+Y)
2. Look for errors
3. Verify settings:
   ```json
   {
     "ultrathink.ultrathinkPath": "c:\\Cloop\\ultrathink"
   }
   ```

## If commands fail:

1. Open terminal in Extension Development Host
2. Test manually:
   ```
   cd c:\Cloop\ultrathink
   poetry run ultrathink analyze --path vscode-extension\test-file.py
   ```
3. If this works, extension should work too
