# 🚀 Quick Start: AI Handoff

## 30-Second Setup

```bash
cd c:\Cloop\ultrathink
poetry run ultrathink handoff --path ./your_code
```

That's it! Now copy `ultrathink_handoff.md` and paste into any AI assistant.

---

## Example

### 1. Run Command
```bash
poetry run ultrathink handoff --path example_handoff_demo.py
```

### 2. See Output
```
Generating AI handoff prompt...

╭─────────────── AI Handoff Prompt ───────────────╮
│ # Code Review - Fix Request                     │
│                                                  │
│ ## Context                                       │
│ I analyzed `example_handoff_demo.py` and found  │
│ **8 issues** that need fixing.                  │
│                                                  │
│ ## Best Practices to Follow                     │
│ - Type Safety, Error Handling, Security...      │
│                                                  │
│ ## Issues Found (8 total)                       │
│ 🔴 Line 12 [CRITICAL] - security                │
│ 🟠 Line 8 [HIGH] - bug                          │
│ ...                                              │
╰──────────────────────────────────────────────────╯

SUCCESS: Saved to ultrathink_handoff.md
```

### 3. Copy File Content
```bash
type ultrathink_handoff.md
```

### 4. Paste into AI
Open Amazon Q, Claude, or ChatGPT and paste the content.

### 5. Get Fixes
AI will fix your code following best practices!

---

## What You Get

✅ **Concise prompt** - No fluff, just what AI needs
✅ **Best practices** - AI knows your standards
✅ **Prioritized issues** - Critical first
✅ **Specific fixes** - Line numbers and suggestions
✅ **Universal** - Works with any AI

---

## Common Use Cases

### Quick File Fix
```bash
poetry run ultrathink handoff --path problem_file.py
```

### Full Project Review
```bash
poetry run ultrathink handoff --path ./src
```

### Before PR
```bash
poetry run ultrathink handoff --path ./my_feature
# Fix issues before submitting
```

---

## Tips

💡 **Iterate**: Fix critical issues, re-run handoff, repeat
💡 **Focus**: Analyze specific files for faster results
💡 **Learn**: Ask AI to explain why each issue matters
💡 **Share**: Send `ultrathink_handoff.md` to teammates

---

**That's it! Start using it now:**
```bash
poetry run ultrathink handoff --path ./your_code
```
