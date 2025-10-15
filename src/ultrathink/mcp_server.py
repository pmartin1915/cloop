"""
MCP Server for Ultrathink - Exposes Ultrathink capabilities to MCP clients like Amazon Q.
"""
import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource, ResourceTemplate

from .framework import Ultrathink
from .learning_engine import LearningEngine
from .scaffolding import PythonScaffolder

logger = logging.getLogger(__name__)

# Initialize Ultrathink framework
ultrathink = Ultrathink("ultrathink.yaml")
ultrathink.initialize()

app = Server("ultrathink")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Ultrathink tools."""
    return [
        Tool(
            name="analyze_code",
            description="Analyze Python code for bugs, security issues, and quality problems. Returns detailed findings with severity levels.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to file or directory to analyze"
                    },
                    "save_findings": {
                        "type": "boolean",
                        "description": "Save findings to knowledge base for learning (default: true)",
                        "default": True
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="learn_patterns",
            description="Learn patterns from accumulated code analysis findings. Identifies recurring issues and generates fixes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "threshold": {
                        "type": "integer",
                        "description": "Minimum occurrences for pattern detection (default: 2)",
                        "default": 2
                    }
                }
            }
        ),
        Tool(
            name="scaffold_project",
            description="Generate a new FastAPI project with learned improvements automatically applied.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Project name"},
                    "author": {"type": "string", "description": "Author name", "default": "Developer"},
                    "email": {"type": "string", "description": "Author email", "default": "dev@example.com"},
                    "description": {"type": "string", "description": "Project description", "default": "A FastAPI application"}
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="get_stats",
            description="Get statistics about the knowledge base: findings, patterns, improvements, and learning rate.",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_patterns",
            description="Browse learned patterns with details about frequency and affected files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Max patterns to return", "default": 10}
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "analyze_code":
            path = arguments["path"]
            save_findings = arguments.get("save_findings", True)
            
            result = await ultrathink.analyze_codebase(path, save_findings=save_findings)
            
            summary = result.get("summary", {})
            output = f"""Analysis Complete for {path}

Summary:
- Files analyzed: {summary.get('files_analyzed', 0)}
- Total issues: {summary.get('total_issues', 0)}
- Critical: {summary.get('critical_issues', 0)}
- High: {summary.get('high_priority_issues', 0)}

Severity Breakdown:
{json.dumps(summary.get('severity_breakdown', {}), indent=2)}

Category Breakdown:
{json.dumps(summary.get('category_breakdown', {}), indent=2)}

Detailed Findings:
{json.dumps(result.get('results', []), indent=2)}
"""
            return [TextContent(type="text", text=output)]
        
        elif name == "learn_patterns":
            threshold = arguments.get("threshold", 2)
            
            learning_engine = LearningEngine(
                knowledge_base=ultrathink.knowledge_base,
                similarity_threshold=0.8
            )
            
            result = learning_engine.learn_from_findings(occurrence_threshold=threshold)
            
            output = f"""Learning Complete

Patterns Identified: {result['patterns_identified']}
Patches Generated: {result['patches_generated']}

Patterns:
{json.dumps(result['patterns'], indent=2)}

Patches:
{json.dumps(result['patches'], indent=2)}
"""
            return [TextContent(type="text", text=output)]
        
        elif name == "scaffold_project":
            name = arguments["name"]
            author = arguments.get("author", "Developer")
            email = arguments.get("email", "dev@example.com")
            description = arguments.get("description", "A FastAPI application")
            
            scaffolder = PythonScaffolder(knowledge_base=ultrathink.knowledge_base)
            project_path = scaffolder.scaffold(
                project_name=name,
                output_dir=".",
                author_name=author,
                author_email=email,
                description=description
            )
            
            applied = scaffolder.get_applied_improvements()
            
            output = f"""Project Scaffolded Successfully!

Location: {project_path.absolute()}
Applied Improvements: {len(applied)}

Improvements Applied:
{json.dumps(applied, indent=2)}

Next Steps:
1. cd {name}
2. poetry install
3. poetry run {name}
"""
            return [TextContent(type="text", text=output)]
        
        elif name == "get_stats":
            stats = ultrathink.get_stats()
            output = f"""Ultrathink Statistics

{json.dumps(stats, indent=2)}
"""
            return [TextContent(type="text", text=output)]
        
        elif name == "get_patterns":
            limit = arguments.get("limit", 10)
            
            patterns = ultrathink.knowledge_base.get_all_patterns()[:limit]
            
            output = f"""Learned Patterns (showing {len(patterns)})

{json.dumps(patterns, indent=2)}
"""
            return [TextContent(type="text", text=output)]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        logger.exception(f"Tool execution failed: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available knowledge base resources."""
    return [
        Resource(
            uri="ultrathink://stats",
            name="Knowledge Base Statistics",
            mimeType="application/json",
            description="Overall statistics about findings, patterns, and improvements"
        ),
        Resource(
            uri="ultrathink://findings",
            name="All Findings",
            mimeType="application/json",
            description="All code analysis findings stored in the knowledge base"
        ),
        Resource(
            uri="ultrathink://patterns",
            name="Learned Patterns",
            mimeType="application/json",
            description="All learned patterns from recurring issues"
        ),
        Resource(
            uri="ultrathink://improvements",
            name="Available Improvements",
            mimeType="application/json",
            description="All generated improvements ready to apply"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read knowledge base resources."""
    if uri == "ultrathink://stats":
        stats = ultrathink.get_stats()
        return json.dumps(stats, indent=2)
    
    elif uri == "ultrathink://findings":
        findings = ultrathink.knowledge_base.get_all_findings()
        return json.dumps(findings, indent=2)
    
    elif uri == "ultrathink://patterns":
        patterns = ultrathink.knowledge_base.get_all_patterns()
        return json.dumps(patterns, indent=2)
    
    elif uri == "ultrathink://improvements":
        improvements = ultrathink.knowledge_base.get_all_improvements()
        return json.dumps(improvements, indent=2)
    
    else:
        raise ValueError(f"Unknown resource: {uri}")


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
