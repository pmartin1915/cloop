"""
Command-line interface for Ultrathink.

This module provides the CLI entry point and user interaction for the
Ultrathink framework.
"""
import argparse
import asyncio
import json
from pathlib import Path

from .framework import Ultrathink


async def main() -> None:
    """Main entry point for the Ultrathink CLI."""
    parser = argparse.ArgumentParser(
        description="Ultrathink - Self-Improving Development Framework"
    )

    parser.add_argument(
        "command",
        choices=["init", "analyze", "improve", "evolve", "test", "stats"],
        help="Command to execute"
    )

    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Path to code/project (default: current directory)"
    )

    parser.add_argument(
        "--config",
        type=str,
        default="ultrathink.yaml",
        help="Config file path (default: ultrathink.yaml)"
    )

    args = parser.parse_args()

    # Initialize framework
    ultrathink = Ultrathink(args.config)

    # Execute command
    if args.command == "init":
        ultrathink.initialize()
        print("Ultrathink framework initialized successfully!")

    elif args.command == "analyze":
        print(f"Analyzing codebase at {args.path}...")
        result = await ultrathink.analyze_codebase(args.path)
        print(json.dumps(result, indent=2))

    elif args.command == "evolve":
        print(f"Evolving architecture for {args.path}...")
        result = await ultrathink.evolve_architecture(args.path)
        print("Architecture Evolution Results:")
        print(json.dumps(result, indent=2))

    elif args.command == "test":
        print(f"Generating tests for {args.path}...")
        code = Path(args.path).read_text()
        tests = await ultrathink.generate_tests(code)
        print(f"Generated Tests:\n{tests}")

    elif args.command == "improve":
        print(f"Running self-improvement for {args.path}...")
        improved = await ultrathink.self_improve(args.path)
        print(f"Self-improvement complete for {args.path}")
        if improved.metadata:
            print(f"Improvements: {json.dumps(improved.metadata.get('improvements', []), indent=2)}")

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
