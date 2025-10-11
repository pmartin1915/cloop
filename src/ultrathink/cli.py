"""
Command-line interface for Ultrathink.

This module provides the CLI entry point and user interaction for the
Ultrathink framework.
"""
import asyncio
import argparse
from pathlib import Path
from typing import Optional
from .framework import Ultrathink


async def main() -> None:
    """Main entry point for the Ultrathink CLI."""
    parser = argparse.ArgumentParser(
        description="Ultrathink - Self-Improving Development Framework"
    )

    parser.add_argument(
        "command",
        choices=["init", "analyze", "improve", "stats"],
        help="Command to execute"
    )

    parser.add_argument(
        "--project-path",
        type=str,
        default=".",
        help="Path to the project (default: current directory)"
    )

    parser.add_argument(
        "--paths",
        type=str,
        nargs="+",
        help="Specific paths to analyze or improve"
    )

    parser.add_argument(
        "--knowledge-base",
        type=str,
        help="Path to knowledge base storage"
    )

    args = parser.parse_args()

    # Initialize Ultrathink framework
    ultrathink = Ultrathink(
        project_path=args.project_path,
        knowledge_base_path=args.knowledge_base
    )

    # Execute command
    if args.command == "init":
        ultrathink.initialize()
        print("Ultrathink framework initialized successfully!")

    elif args.command == "analyze":
        print("Analyzing codebase...")
        ultrathink.initialize()
        results = ultrathink.analyze(args.paths)
        print(f"Analysis complete:")
        print(f"  - Findings: {results['findings_count']}")
        print(f"  - Suggestions: {results['suggestions_count']}")
        print(f"  - Confidence: {results['confidence']:.2%}")

    elif args.command == "improve":
        print("Running self-improvement cycle...")
        ultrathink.initialize()
        results = ultrathink.improve(args.paths)
        print(f"Improvement cycle complete:")
        print(f"  - Cycle number: {results['cycle_number']}")
        print(f"  - Hypotheses generated: {results['hypotheses_generated']}")
        print(f"  - Hypotheses validated: {results['hypotheses_validated']}")
        print(f"  - Improvements applied: {results['improvements_applied']}")
        ultrathink.save_knowledge()

    elif args.command == "stats":
        ultrathink.initialize()
        stats = ultrathink.get_stats()
        print("Ultrathink Statistics:")
        for key, value in stats.items():
            print(f"  - {key}: {value}")


def run() -> None:
    """Wrapper to run the async main function."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
