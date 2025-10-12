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

    # Analysis-specific arguments
    parser.add_argument(
        "--save-findings",
        action="store_true",
        default=True,
        help="Save analysis findings to knowledge base (default: True)"
    )

    parser.add_argument(
        "--no-save-findings",
        dest="save_findings",
        action="store_false",
        help="Don't save analysis findings to knowledge base"
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

            print("\n[SUCCESS] Project scaffolded successfully!")
            print(f"Location: {project_path.absolute()}")
            print("\nNext steps:")
            print(f"   cd {args.name}")
            print("   poetry install")
            print(f"   poetry run {args.name}")
            print("\nDocumentation: http://localhost:8000/docs")

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
        result = await ultrathink.analyze_codebase(args.path, save_findings=args.save_findings)

        # Notify user if findings were saved
        if args.save_findings:
            total_issues = result.get("summary", {}).get("total_issues", 0)
            if total_issues > 0:
                print(f"\n[Saved {total_issues} findings to knowledge base]")

        # Display results in a user-friendly format
        print("\n" + "="*70)
        print("ANALYSIS RESULTS")
        print("="*70)

        summary = result.get("summary", {})
        print("\nSummary:")
        print(f"  Files analyzed: {summary.get('files_analyzed', 0)}")
        print(f"  Total issues found: {summary.get('total_issues', 0)}")
        print(f"  Critical issues: {summary.get('critical_issues', 0)}")
        print(f"  High priority: {summary.get('high_priority_issues', 0)}")

        # Show severity breakdown
        severity_breakdown = summary.get('severity_breakdown', {})
        if any(severity_breakdown.values()):
            print("\n  Severity breakdown:")
            for severity, count in severity_breakdown.items():
                if count > 0:
                    print(f"    {severity}: {count}")

        # Show category breakdown
        category_breakdown = summary.get('category_breakdown', {})
        if category_breakdown:
            print("\n  Category breakdown:")
            for category, count in category_breakdown.items():
                print(f"    {category}: {count}")

        # Show detailed findings for each file
        print("\n" + "-"*70)
        print("DETAILED FINDINGS")
        print("-"*70)

        for file_result in result.get("results", []):
            file_path = file_result.get("file", "Unknown")
            print(f"\n{file_path}")

            if 'error' in file_result:
                print(f"  [ERROR] {file_result['error']}")
                continue

            analysis = file_result.get("analysis", {})
            findings = analysis.get("findings", [])

            if not findings:
                print("  No issues found")
                continue

            for i, finding in enumerate(findings, 1):
                line = finding.get("line_number", "?")
                severity = finding.get("severity", "info").upper()
                category = finding.get("category", "unknown")
                description = finding.get("description", finding.get("raw_response", "No description"))
                suggestion = finding.get("suggestion", "")

                print(f"  [{i}] Line {line} - {severity} ({category})")
                print(f"      Issue: {description}")
                if suggestion:
                    print(f"      Fix: {suggestion}")

        print("\n" + "="*70)

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
