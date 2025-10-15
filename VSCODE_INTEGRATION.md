# Ultrathink VS Code Integration

## ✅ Setup Complete!

VS Code tasks are now configured. You can use Ultrathink directly from VS Code.

## How to Use

### Method 1: Command Palette (Recommended)

1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. Select an Ultrathink task:
   - **Analyze Current File** - Analyzes the file you have open
   - **Analyze Workspace** - Analyzes entire workspace
   - **Learn Patterns** - Learns from stored findings
   - **Show Statistics** - Displays stats
   - **Scaffold Project** - Creates new project (prompts for details)

### Method 2: Keyboard Shortcuts

- `Ctrl+Shift+U` then `A` - Analyze current file
- `Ctrl+Shift+U` then `L` - Learn patterns
- `Ctrl+Shift+U` then `S` - Show statistics

### Method 3: Terminal Menu

1. Click "Terminal" menu
2. Select "Run Task..."
3. Choose Ultrathink task

## Quick Test

1. Open any Python file (or create one)
2. Press `Ctrl+Shift+P`
3. Type "run task"
4. Select "Ultrathink: Analyze Current File"
5. Watch the terminal output

## Example Workflow

```
1. Write some Python code
2. Ctrl+Shift+U A (analyze file)
3. Review findings in terminal
4. Write more code
5. Ctrl+Shift+U L (learn patterns)
6. Ctrl+Shift+U S (check stats)
7. Create new project with learned improvements
```

## Output

All Ultrathink output appears in the VS Code terminal panel. You'll see:
- Detailed analysis results
- Severity breakdowns
- Learning statistics
- Pattern information

## Customization

Edit `.vscode/tasks.json` to:
- Change default threshold for learning
- Add custom flags
- Modify output behavior

Edit `.vscode/keybindings.json` to:
- Change keyboard shortcuts
- Add more shortcuts

## Troubleshooting

**Task not found:**
- Make sure you're in the ultrathink workspace folder
- Reload VS Code window (Ctrl+R)

**Poetry not found:**
- Ensure Poetry is in your PATH
- Or modify tasks.json to use full Poetry path

**Command fails:**
- Check terminal output for errors
- Verify Ultrathink CLI works: `poetry run ultrathink --help`
