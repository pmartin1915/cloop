# 🤖 Ultrathink + Amazon Q via MCP

**Transform Ultrathink into a conversational AI assistant through Amazon Q.**

## What Changed?

**Before (CLI):**
```bash
poetry run ultrathink analyze --path ./my_code
poetry run ultrathink learn --threshold 2
poetry run ultrathink scaffold --name new_project
```

**After (MCP + Amazon Q):**
```
You: "Analyze this file for issues"
You: "Learn patterns from my code"  
You: "Create a new project with improvements"
```

Just chat naturally with Amazon Q - it handles Ultrathink for you.

## Why MCP?

✅ **Zero context switching** - Everything in your IDE  
✅ **Natural language** - No commands to remember  
✅ **Context aware** - Amazon Q knows your current file  
✅ **Discoverable** - Amazon Q suggests when to use Ultrathink  
✅ **Composable** - Works with other MCP tools  

## Setup (3 Steps)

### 1. Install MCP SDK
```bash
cd c:\Cloop\ultrathink
poetry add mcp
```

### 2. Test It Works
```bash
poetry run python test_mcp.py
```

Should show:
```
✅ All MCP functions working!
```

### 3. Configure Amazon Q

Add to: `%APPDATA%\Code\User\globalStorage\amazonwebservices.amazon-q-vscode\mcp_config.json`

```json
{
  "mcpServers": {
    "ultrathink": {
      "command": "poetry",
      "args": ["run", "python", "-m", "ultrathink.mcp_server"],
      "cwd": "c:\\Cloop\\ultrathink"
    }
  }
}
```

Restart VS Code. Done!

## What You Can Do

### Analyze Code
```
"Use Ultrathink to analyze this file"
"Check src/ultrathink/framework.py for issues"
"Analyze my current file"
```

### Learn Patterns
```
"Learn patterns from my analyses"
"What patterns has Ultrathink found?"
"Learn with threshold 3"
```

### Generate Projects
```
"Create a FastAPI project called 'my-api'"
"Scaffold a new project with learned improvements"
"Generate a project named 'improved-service'"
```

### Check Progress
```
"Show Ultrathink statistics"
"What has Ultrathink learned?"
"How many patterns do we have?"
```

## Available Tools

Amazon Q can use these Ultrathink tools:

- **analyze_code** - Analyze files/folders for issues
- **learn_patterns** - Learn from accumulated findings
- **scaffold_project** - Generate projects with improvements
- **get_stats** - View knowledge base statistics
- **get_patterns** - Browse learned patterns

## Available Resources

Amazon Q can read from:

- `ultrathink://stats` - Overall statistics
- `ultrathink://findings` - All findings
- `ultrathink://patterns` - All patterns
- `ultrathink://improvements` - All improvements

## Example Workflow

```
You: "Analyze src/ultrathink/framework.py"
Q: [Uses analyze_code]
   Found 3 issues: 1 high, 2 medium...

You: "Learn patterns from that"
Q: [Uses learn_patterns]
   Learned 2 new patterns...

You: "Create a project called 'better-api' with those improvements"
Q: [Uses scaffold_project]
   Created project with 2 improvements applied!
   Location: c:\Cloop\ultrathink\better-api
```

## Troubleshooting

**MCP server not connecting?**
1. Run `poetry run python test_mcp.py` - should pass
2. Check VS Code Output → Amazon Q Language Server
3. Verify path in mcp_config.json uses `\\` on Windows

**Tool execution fails?**
1. Ensure `.env` has API credentials
2. Run `poetry run ultrathink init`
3. Check `ultrathink.yaml` exists

**Need help?**
See [MCP_SETUP.md](MCP_SETUP.md) for detailed troubleshooting.

## Files Added

- `src/ultrathink/mcp_server.py` - MCP server implementation
- `mcp_config.json` - Example configuration
- `test_mcp.py` - Test script
- `MCP_SETUP.md` - Detailed setup guide
- `QUICK_MCP_START.md` - Quick reference

## Next Steps

1. Install: `poetry add mcp`
2. Test: `poetry run python test_mcp.py`
3. Configure Amazon Q (see above)
4. Restart VS Code
5. Chat with Amazon Q: "Use Ultrathink to analyze this file"

The more you use it, the smarter it gets! 🚀
