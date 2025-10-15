# 🎯 Ultrathink for Personal/Recreational Coding

## Your Simple 3-Step Workflow

### Step 1: Write Code in VSCode
Just code normally. Don't worry about perfection.

### Step 2: Generate Handoff (30 seconds)
```bash
# In VSCode terminal (Ctrl+`)
cd c:\Cloop\ultrathink
poetry run ultrathink handoff --path "path\to\your\file.py"
```

### Step 3: Paste into Amazon Q
1. Open `ultrathink_handoff.md`
2. Copy all (Ctrl+A, Ctrl+C)
3. Paste into Amazon Q chat
4. Q fixes your code with explanations!

---

## Quick Setup (One-Time)

### Add to VSCode Tasks
Create `.vscode/tasks.json` in your project:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Ultrathink: Generate Handoff",
      "type": "shell",
      "command": "cd c:\\Cloop\\ultrathink && poetry run ultrathink handoff --path \"${file}\"",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

**Now**: Press `Ctrl+Shift+P` → "Run Task" → "Ultrathink: Generate Handoff"

### Add Keyboard Shortcut
Create `.vscode/keybindings.json`:

```json
[
  {
    "key": "ctrl+shift+u",
    "command": "workbench.action.tasks.runTask",
    "args": "Ultrathink: Generate Handoff"
  }
]
```

**Now**: Press `Ctrl+Shift+U` on any file!

---

## Real-World Example

### You Write This:
```python
def calculate(x, y, op):
    if op == "divide":
        return x / y
    return eval(f"{x} {op} {y}")
```

### Press Ctrl+Shift+U

### Ultrathink Creates:
```markdown
# Code Review - Fix Request

## Issues Found (2 total)

[!] **Line 4** [CRITICAL] - security
- Issue: eval() allows code injection
- Fix: Use ast.literal_eval() or match/case

[!!] **Line 3** [HIGH] - bug  
- Issue: Division by zero not handled
- Fix: Add if y == 0: raise ValueError
```

### Paste into Amazon Q

### Q Responds:
```python
import ast

def calculate(x: float, y: float, op: str) -> float:
    """Calculate with safety checks.
    
    Args:
        x: First number
        y: Second number
        op: Operation (add, subtract, multiply, divide)
        
    Returns:
        Result of calculation
        
    Raises:
        ValueError: If operation invalid or division by zero
    """
    if op == "divide":
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y
    elif op == "add":
        return x + y
    elif op == "subtract":
        return x - y
    elif op == "multiply":
        return x * y
    else:
        raise ValueError(f"Unknown operation: {op}")
```

**Q explains**: "I fixed the eval() security issue by using explicit operations, added type hints, handled division by zero, and added proper error handling."

---

## What Makes This Useful for You

### ✅ Learn While You Code
- See what issues you're making
- Understand why they're problems
- Learn best practices naturally

### ✅ No Context Switching
- Stay in VSCode
- One keyboard shortcut
- Amazon Q does the heavy lifting

### ✅ Build Better Habits
- Over time, you'll write fewer issues
- Ultrathink learns your patterns
- Future projects start cleaner

---

## Pro Tips for Recreational Coding

### 1. Use It Before Sharing Code
```bash
# Before pushing to GitHub
poetry run ultrathink handoff --path .\src
# Fix issues Q finds
# Push clean code!
```

### 2. Learn from Patterns
```bash
# After a few projects
poetry run ultrathink learn --threshold 2
# See what mistakes you repeat
# Focus on improving those
```

### 3. Quick File Check
```bash
# Right-click file in VSCode → "Run Task" → "Ultrathink"
# Instant feedback!
```

---

## Troubleshooting

### "AWS Throttling Error"
Wait 1-2 minutes between analyses. AWS has rate limits.

### "No Issues Found"
The AI might be rate-limited. Try again in a minute.

### "Encoding Error"
Already fixed! Update to latest version.

---

## What You DON'T Need

❌ Don't use `analyze` command (too verbose)
❌ Don't use `learn` until you have 5+ projects
❌ Don't use `scaffold` unless starting new projects
❌ Don't worry about the VSCode extension (not needed)

## What You DO Need

✅ `handoff` command (that's it!)
✅ Amazon Q in VSCode
✅ 30 seconds per file

---

## Your Typical Session

```
1. Code for 30 minutes
2. Press Ctrl+Shift+U
3. Copy ultrathink_handoff.md
4. Paste into Amazon Q
5. Review Q's fixes
6. Apply the good ones
7. Keep coding!
```

**Time investment**: 2 minutes per coding session
**Value**: Learn best practices, write better code, impress yourself!

---

## Next Level (Optional)

Once comfortable, try:

### Auto-Open Handoff
Add to tasks.json:
```json
"command": "cd c:\\Cloop\\ultrathink && poetry run ultrathink handoff --path \"${file}\" && code ultrathink_handoff.md"
```

Now it auto-opens the handoff file!

### Batch Check
```bash
# Check all Python files in project
poetry run ultrathink handoff --path .\
```

---

## Bottom Line

**Ultrathink = Your Code → Perfect Prompt → Amazon Q Fixes It**

That's it. Simple, fast, educational.

Press `Ctrl+Shift+U`, paste into Q, learn and improve! 🚀
