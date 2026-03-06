# 🤝 AI Handoff Feature

## Quick Start

Generate a concise, AI-ready prompt with all code issues:

```bash
poetry run ultrathink handoff --path ./your_code
```

This creates `ultrathink_handoff.md` with:
- ✅ Best practice guidelines
- ✅ All issues organized by file
- ✅ Severity-based prioritization
- ✅ Specific line numbers and fixes
- ✅ Ready to paste into any AI assistant

## Example Usage

### 1. Analyze and Generate Handoff

```bash
# Analyze a single file
poetry run ultrathink handoff --path example_handoff_demo.py

# Analyze entire project
poetry run ultrathink handoff --path ./src
```

### 2. Copy the Output

The command displays the prompt and saves it to `ultrathink_handoff.md`:

```markdown
# Code Review - Fix Request

## Context
I analyzed `example_handoff_demo.py` and found **8 issues** that need fixing.

## Best Practices to Follow
- **Type Safety**: Add type hints to all functions
- **Error Handling**: Use specific exceptions, validate inputs
- **Security**: Avoid eval(), use parameterized queries
- **Code Quality**: Add docstrings, remove unused code
- **Performance**: Optimize loops, avoid redundant operations

## Issues Found (8 total)

⚠️ **Priority**: 2 critical, 3 high-severity issues

### `example_handoff_demo.py`

🔴 **Line 12** [CRITICAL] - security
- Issue: Use of eval() allows arbitrary code execution
- Fix: Replace eval() with ast.literal_eval() or safe alternatives

🟠 **Line 8** [HIGH] - bug
- Issue: Division by zero not handled
- Fix: Add zero check before division

🟡 **Line 15** [MEDIUM] - quality
- Issue: Missing docstring
- Fix: Add function docstring

## Your Task
Fix these issues following the best practices above. For each fix:
1. Show the corrected code
2. Explain what changed and why
3. Start with critical/high-severity issues
```

### 3. Paste into AI Assistant

Copy the entire prompt and paste it into:
- Amazon Q
- Claude
- ChatGPT
- Cline
- Any AI coding assistant

The AI will have full context and best practices to fix your code properly.

## Benefits

✅ **Concise** - Only essential information, no fluff
✅ **Prioritized** - Critical issues first
✅ **Actionable** - Specific line numbers and fixes
✅ **Best Practices** - AI knows your coding standards
✅ **Universal** - Works with any AI assistant

## Workflow Integration

### With Amazon Q
```bash
# 1. Generate handoff
poetry run ultrathink handoff --path ./src

# 2. Open Amazon Q in IDE
# 3. Paste ultrathink_handoff.md content
# 4. Q fixes issues following best practices
```

### With VSCode Extension
```bash
# Coming soon: Right-click → "Generate Handoff Prompt"
```

## Tips

- **Focus on specific files** for faster analysis
- **Review the prompt** before sending to AI
- **Iterate**: Fix critical issues, re-analyze, repeat
- **Save handoffs** for documentation/team sharing

## Example Output

See `ultrathink_handoff.md` after running the command.
