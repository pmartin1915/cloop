"""
Quick test script to verify MCP server works.
Run: poetry run python test_mcp.py
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ultrathink.framework import Ultrathink
from ultrathink.learning_engine import LearningEngine

async def test_mcp_functions():
    """Test the core functions that MCP server will use."""
    print("Testing Ultrathink MCP Integration...\n")
    
    # Initialize
    print("1. Initializing Ultrathink...")
    ultrathink = Ultrathink("ultrathink.yaml")
    ultrathink.initialize()
    print("   [OK] Initialized\n")
    
    # Test stats
    print("2. Getting stats...")
    stats = ultrathink.get_stats()
    print(f"   [OK] Findings: {stats.get('total_findings', 0)}")
    print(f"   [OK] Patterns: {stats.get('total_patterns', 0)}")
    print(f"   [OK] Improvements: {stats.get('total_improvements', 0)}\n")
    
    # Test getting patterns
    print("3. Getting patterns...")
    patterns = ultrathink.knowledge_base.get_all_patterns()
    print(f"   [OK] Found {len(patterns)} patterns\n")
    
    # Test getting improvements
    print("4. Getting improvements...")
    improvements = ultrathink.knowledge_base.get_all_improvements()
    print(f"   [OK] Found {len(improvements)} improvements\n")
    
    print("[SUCCESS] All MCP functions working!")
    print("\nNext step: Install MCP SDK")
    print("  poetry add mcp")
    print("\nThen configure Amazon Q (see QUICK_MCP_START.md)")

if __name__ == "__main__":
    asyncio.run(test_mcp_functions())
