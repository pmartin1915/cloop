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
from .learning_engine import LearningEngine
from .scaffolding import PythonScaffolder

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point for the Ultrathink CLI."""
    parser = argparse.ArgumentParser(
        description="Ultrathink - Self-Improving Development Framework"
    )

    parser.add_argument(
        "command",
        choices=["init", "analyze", "improve", "evolve", "test", "stats", "scaffold", "learn"],
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

    # Learn command arguments
    parser.add_argument(
        "--threshold",
        type=int,
        default=2,
        help="Minimum occurrences for pattern detection (default: 2)"
    )

    args = parser.parse_args()

    # Handle scaffold command with optional knowledge base integration
    if args.command == "scaffold":
        if not args.name:
            parser.error("--name is required for scaffold command")

        print(f"Scaffolding new FastAPI project: {args.name}")

        # Initialize framework to get knowledge base for applying improvements
        try:
            ultrathink = Ultrathink(args.config)
            ultrathink.knowledge_base.load()  # Load existing improvements
            scaffolder = PythonScaffolder(knowledge_base=ultrathink.knowledge_base)

            # Check if there are improvements available
            kb_stats = ultrathink.knowledge_base.get_stats()
            if kb_stats.get('total_improvements', 0) > 0:
                print(f"Found {kb_stats['total_improvements']} learned improvements in knowledge base")
                print("These will be applied automatically to the generated code\n")
        except Exception as e:
            # Fall back to basic scaffolder if framework init fails
            logger.warning(f"Could not load knowledge base: {e}")
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

            # Show applied improvements
            applied = scaffolder.get_applied_improvements()
            if applied:
                print(f"\n[IMPROVEMENTS] Applied {len(applied)} learned improvements:")
                for imp in applied[:5]:  # Show first 5
                    print(f"  - {imp['file']}: {imp['reason']}")
                if len(applied) > 5:
                    print(f"  ... and {len(applied) - 5} more")

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

    elif args.command == "learn":
        print("Learning from stored analysis findings...")
        print(f"Pattern detection threshold: {args.threshold} occurrences\n")

        # Create learning engine
        learning_engine = LearningEngine(
            knowledge_base=ultrathink.knowledge_base,
            similarity_threshold=ultrathink.config.get('learning', {}).get('pattern_similarity_threshold', 0.8)
        )

        # Learn from findings
        result = learning_engine.learn_from_findings(occurrence_threshold=args.threshold)

        # Display learning summary
        print("="*70)
        print("LEARNING RESULTS")
        print("="*70)

        print(f"\nPatterns Identified: {result['patterns_identified']}")
        print(f"Patches Generated: {result['patches_generated']}")

        # Show identified patterns
        if result['patterns']:
            print("\n" + "-"*70)
            print("PATTERNS IDENTIFIED")
            print("-"*70)

            for i, pattern in enumerate(result['patterns'], 1):
                print(f"\n[{i}] {pattern['description']}")
                print(f"    Category: {pattern['pattern_type']}")
                print(f"    Severity: {pattern['severity']}")
                print(f"    Frequency: {pattern['frequency']} occurrences")
                print(f"    Affected files: {len(pattern['affected_files'])}")
                if pattern['affected_files'][:3]:
                    print("    Examples:")
                    for file in pattern['affected_files'][:3]:
                        print(f"      - {file}")

        # Show generated patches
        if result['patches']:
            print("\n" + "-"*70)
            print("PATCHES GENERATED")
            print("-"*70)

            for i, patch in enumerate(result['patches'], 1):
                print(f"\n[{i}] {patch['reason']}")
                if patch['template_file']:
                    print(f"    Target template: {patch['template_file']}")
                if patch['line_pattern']:
                    print(f"    Pattern to match: {patch['line_pattern'][:60]}...")

        # Show learning statistics
        stats = learning_engine.get_learning_stats()
        print("\n" + "-"*70)
        print("LEARNING STATISTICS")
        print("-"*70)

        print(f"\n  Total findings analyzed: {stats['total_findings']}")
        print(f"  Total patterns identified: {stats['total_patterns']}")
        print(f"  Total patches available: {stats['total_patches']}")
        print(f"  Learning rate: {stats['learning_rate']:.2%}")

        if stats['top_issues']:
            print("\n  Most common issues:")
            for issue in stats['top_issues'][:5]:
                print(f"    - {issue['description']}: {issue['count']} occurrences")

        print("\n" + "="*70)

        if result['patches_generated'] > 0:
            print(f"\n[SUCCESS] Learned {result['patches_generated']} improvements from code analysis")
            print("These patches will be applied automatically in future scaffolding operations")
        else:
            print("\n[INFO] No new patterns found. Analyze more code to enable learning.")


def run() -> None:
    """Wrapper to run the async main function."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
