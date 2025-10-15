# 🚀 Quick Start: Ultrathink + Amazon Q

Get Ultrathink working with Amazon Q in 3 commands.

## Step 1: Install MCP

```bash
cd c:\Cloop\ultrathink
poetry add mcp
```

## Step 2: Configure Amazon Q

Copy this to Amazon Q's MCP config file:

**Location:** `%APPDATA%\Code\User\globalStorage\amazonwebservices.amazon-q-vscode\mcp_config.json`

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

## Step 3: Restart VS Code

Done! Now chat with Amazon Q:

```
"Analyze this file with Ultrathink"
"Learn patterns from my code"
"Create a new FastAPI project with improvements"
```

## Test It

1. Open any Python file
2. Ask Amazon Q: "Use Ultrathink to analyze this file"
3. Watch it find issues automatically!

See [MCP_SETUP.md](MCP_SETUP.md) for full details.
