"""
Command-line interface for Ultrathink.

This module provides the CLI entry point and user interaction for the
Ultrathink framework.
"""
import argparse
import asyncio
import json
import logging
from pathlib import Path

from .framework import Ultrathink
from .scaffolding import PythonScaffolder

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main() -> None:
    """Main entry point for the Ultrathink CLI."""
    parser = argparse.ArgumentParser(
        description="Ultrathink - Self-Improving Development Framework"
    )

    parser.add_argument(
        "command",
        choices=["init", "analyze", "improve", "evolve", "test", "stats", "scaffold"],
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

    # Scaffold-specific arguments
    parser.add_argument(
        "--name",
        type=str,
        help="Project name for scaffolding (required for scaffold command)"
    )

    parser.add_argument(
        "--author",
        type=str,
        default="Your Name",
        help="Author name for scaffolded project"
    )

    parser.add_argument(
        "--email",
        type=str,
        default="you@example.com",
        help="Author email for scaffolded project"
    )

    parser.add_argument(
        "--description",
        type=str,
        default="A FastAPI application",
        help="Project description for scaffolded project"
    )

    args = parser.parse_args()

    # Handle scaffold command separately (doesn't need framework init)
    if args.command == "scaffold":
        if not args.name:
            parser.error("--name is required for scaffold command")

        print(f"Scaffolding new FastAPI project: {args.name}")
        scaffolder = PythonScaffolder()

        try:
            project_path = scaffolder.scaffold(
                project_name=args.name,
                output_dir=args.path,
                author_name=args.author,
                author_email=args.email,
                description=args.description
            )

            print(f"\n[SUCCESS] Project scaffolded successfully!")
            print(f"Location: {project_path.absolute()}")
            print(f"\nNext steps:")
            print(f"   cd {args.name}")
            print(f"   poetry install")
            print(f"   poetry run {args.name}")
            print(f"\nDocumentation: http://localhost:8000/docs")

        except ValueError as e:
            print(f"[ERROR] {e}")
            return
        except FileExistsError as e:
            print(f"[ERROR] {e}")
            return
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            logging.exception("Scaffolding failed")
            return

        return

    # Initialize framework for other commands
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
