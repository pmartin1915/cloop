# Quick Start - Use Ultrathink Now

## Step 1: Close Git Editor
Close the COMMIT_EDITMSG file you have open.

## Step 2: Open Ultrathink Workspace
In VS Code:
- File → Open Folder
- Navigate to: `c:\Cloop\ultrathink`
- Click "Select Folder"

## Step 3: Test Ultrathink CLI
Open terminal in VS Code (Ctrl+`) and run:
```bash
poetry run ultrathink --help
```

You should see the help menu.

## Step 4: Run Your First Analysis
```bash
poetry run ultrathink analyze --path vscode-extension\test-file.py
```

## Step 5: Use VS Code Tasks
Now that you're in the right workspace:
1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. You should see Ultrathink tasks

## If Tasks Still Don't Show
The .vscode folder needs to be in your workspace root. Check:
```bash
dir .vscode
```

You should see tasks.json and keybindings.json.

## Alternative: Use Terminal Directly
Just use the terminal in VS Code:
```bash
# Analyze a file
poetry run ultrathink analyze --path src\ultrathink\framework.py

# Learn patterns
poetry run ultrathink learn --threshold 2

# Show stats
poetry run ultrathink stats
```

This works immediately without any VS Code configuration.
