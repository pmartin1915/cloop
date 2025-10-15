# Ultrathink MCP Integration

Connect Ultrathink to Amazon Q using Model Context Protocol (MCP).

## What This Gives You

Instead of running CLI commands, just chat with Amazon Q:

```
You: "Analyze this file for issues"
Q: [Uses Ultrathink] Found 5 issues: 2 security, 3 quality...

You: "Learn patterns from my analyses"
Q: [Uses Ultrathink] Learned 3 new patterns...

You: "Create a FastAPI project with those improvements"
Q: [Uses Ultrathink] Created project with 8 improvements applied...
```

## Setup (2 minutes)

### 1. Install MCP SDK

```bash
cd c:\Cloop\ultrathink
poetry add mcp
```

### 2. Configure Amazon Q

Add to your Amazon Q MCP settings file:

**Windows:** `%APPDATA%\Code\User\globalStorage\amazonwebservices.amazon-q-vscode\mcp_config.json`

**Mac/Linux:** `~/.config/Code/User/globalStorage/amazonwebservices.amazon-q-vscode/mcp_config.json`

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

### 3. Restart VS Code

Amazon Q will automatically connect to Ultrathink on startup.

## Available Tools

Amazon Q can now use these Ultrathink tools:

### `analyze_code`
Analyze Python code for bugs, security issues, and quality problems.

**Example:** "Analyze the framework.py file"

### `learn_patterns`
Learn patterns from accumulated findings and generate fixes.

**Example:** "Learn patterns from my recent analyses"

### `scaffold_project`
Generate a new FastAPI project with learned improvements.

**Example:** "Create a new FastAPI project called 'my-api'"

### `get_stats`
View knowledge base statistics.

**Example:** "Show me Ultrathink statistics"

### `get_patterns`
Browse learned patterns.

**Example:** "What patterns has Ultrathink learned?"

## Available Resources

Amazon Q can also read from Ultrathink's knowledge base:

- `ultrathink://stats` - Overall statistics
- `ultrathink://findings` - All code analysis findings
- `ultrathink://patterns` - All learned patterns
- `ultrathink://improvements` - All available improvements

## Usage Examples

### Analyze Code
```
You: "Use Ultrathink to analyze src/ultrathink/framework.py"
Q: [Calls analyze_code tool]
   Analysis Complete for src/ultrathink/framework.py
   
   Summary:
   - Files analyzed: 1
   - Total issues: 3
   - Critical: 0
   - High: 1
   ...
```

### Learn and Apply
```
You: "Learn patterns from my analyses with threshold 2"
Q: [Calls learn_patterns tool]
   Learning Complete
   
   Patterns Identified: 2
   Patches Generated: 2
   ...

You: "Now create a new project called 'improved-api' with those improvements"
Q: [Calls scaffold_project tool]
   Project Scaffolded Successfully!
   
   Location: c:\Cloop\ultrathink\improved-api
   Applied Improvements: 2
   ...
```

### Check Progress
```
You: "What has Ultrathink learned so far?"
Q: [Calls get_stats tool]
   Ultrathink Statistics
   
   - Total findings: 42
   - Total patterns: 5
   - Total improvements: 5
   - Learning rate: 11.9%
   ...
```

## Troubleshooting

### MCP server not connecting

1. Check Poetry is in PATH: `poetry --version`
2. Check Ultrathink is installed: `poetry run python -c "import ultrathink"`
3. Test MCP server manually: `poetry run python -m ultrathink.mcp_server`
4. Check VS Code Output panel → Amazon Q Language Server

### Tool execution fails

1. Ensure `.env` file has API credentials (Claude/Gemini/Bedrock)
2. Check `ultrathink.yaml` exists
3. Run `poetry run ultrathink init` to initialize

### Path issues on Windows

Use double backslashes in `cwd`: `"cwd": "c:\\Cloop\\ultrathink"`

## Benefits Over CLI

✅ **Natural conversation** - No need to remember commands  
✅ **Context aware** - Amazon Q knows your current file/project  
✅ **Integrated** - Everything in your IDE, no terminal switching  
✅ **Discoverable** - Amazon Q suggests when to use Ultrathink  
✅ **Composable** - Combine with other MCP tools and Amazon Q features

## Next Steps

1. Try analyzing a file: "Analyze this file with Ultrathink"
2. Learn patterns: "Learn patterns from my analyses"
3. Generate a project: "Create a FastAPI project with improvements"
4. Check progress: "Show Ultrathink stats"

The more you use it, the smarter it gets! 🚀
