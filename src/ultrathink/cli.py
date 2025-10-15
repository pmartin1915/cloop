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

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .framework import Ultrathink
from .learning_engine import LearningEngine
from .scaffolding import PythonScaffolder
from .profiles import ProfileManager

# Initialize rich console for colored output
# Force UTF-8 to avoid Windows cp1252 encoding issues with Unicode symbols
console = Console(force_terminal=True, legacy_windows=False)

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
        choices=["init", "analyze", "improve", "evolve", "test", "stats", "scaffold", "learn", "ui", "handoff"],
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

    parser.add_argument(
        "--profile",
        type=str,
        choices=["auto", "medical", "game", "general"],
        default="auto",
        help="Project profile for context-aware analysis (default: auto-detect)"
    )

    args = parser.parse_args()

    # Handle scaffold command with optional knowledge base integration
    if args.command == "scaffold":
        if not args.name:
            parser.error("--name is required for scaffold command")

        console.print(f"\n[cyan]Scaffolding new FastAPI project:[/cyan] [bold]{args.name}[/bold]")

        # Initialize framework to get knowledge base for applying improvements
        try:
            ultrathink = Ultrathink(args.config)
            ultrathink.knowledge_base.load()  # Load existing improvements
            scaffolder = PythonScaffolder(knowledge_base=ultrathink.knowledge_base)

            # Check if there are improvements available
            kb_stats = ultrathink.knowledge_base.get_stats()
            if kb_stats.get('total_improvements', 0) > 0:
                console.print(f"[yellow]Found {kb_stats['total_improvements']} learned improvements in knowledge base[/yellow]")
                console.print("[dim]These will be applied automatically to the generated code[/dim]\n")
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

            console.print(Panel.fit(
                f"[green]SUCCESS: Project scaffolded successfully![/green]\n"
                f"[cyan]Location:[/cyan] {project_path.absolute()}",
                border_style="green"
            ))

            # Show applied improvements
            applied = scaffolder.get_applied_improvements()
            if applied:
                console.print(f"\n[green]Applied {len(applied)} learned improvements:[/green]")
                for imp in applied[:5]:  # Show first 5
                    console.print(f"  [green]+[/green] {imp['file']}: [dim]{imp['reason']}[/dim]")
                if len(applied) > 5:
                    console.print(f"  [dim]... and {len(applied) - 5} more[/dim]")

            console.print("\n[cyan]Next steps:[/cyan]")
            console.print(f"   [bold]cd {args.name}[/bold]")
            console.print("   [bold]poetry install[/bold]")
            console.print(f"   [bold]poetry run {args.name}[/bold]")
            console.print("\n[cyan]Documentation:[/cyan] http://localhost:8000/docs")

        except ValueError as e:
            console.print(f"[red]ERROR:[/red] {e}")
            return
        except FileExistsError as e:
            console.print(f"[red]ERROR:[/red] {e}")
            return
        except Exception as e:
            console.print(f"[red]ERROR:[/red] Unexpected error: {e}")
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

    elif args.command == "ui":
        console.print("\n[cyan]Launching Ultrathink Dashboard...[/cyan]")
        
        import subprocess
        import sys
        import socket
        
        # Get path to streamlit app
        ui_path = Path(__file__).parent.parent.parent / "ui" / "app.py"
        
        # Find available port with retry logic
        def is_port_available(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('localhost', port))
                    return True
                except OSError:
                    return False
        
        # Try ports 8501-8510 with retries
        port = None
        for p in range(8501, 8511):
            if is_port_available(p):
                # Double-check after a brief moment
                import time
                time.sleep(0.1)
                if is_port_available(p):
                    port = p
                    break
        
        if not port:
            console.print("[red]No available ports found (tried 8501-8510)[/red]")
            console.print("[yellow]Please close other Streamlit instances or specify a port:[/yellow]")
            console.print("[dim]streamlit run ui/app.py --server.port 8520[/dim]")
            return
        
        console.print(f"[dim]Opening browser at http://localhost:{port}[/dim]\n")
        
        try:
            # Launch streamlit with available port
            result = subprocess.run([
                sys.executable, "-m", "streamlit", "run", str(ui_path),
                "--server.port", str(port)
            ], check=True, capture_output=False)
        except subprocess.CalledProcessError as e:
            # Port conflict - try next port
            console.print(f"[yellow]Port {port} became unavailable, trying next port...[/yellow]")
            for p in range(port + 1, 8511):
                if is_port_available(p):
                    console.print(f"[dim]Retrying with port {p}[/dim]\n")
                    try:
                        subprocess.run([
                            sys.executable, "-m", "streamlit", "run", str(ui_path),
                            "--server.port", str(p)
                        ], check=True)
                        return
                    except:
                        continue
            console.print(f"[red]Failed to launch dashboard[/red]")
            console.print(f"[dim]Try manually: streamlit run ui/app.py --server.port 8520[/dim]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Dashboard closed[/yellow]")
        except Exception as e:
            console.print(f"[red]Failed to launch dashboard: {e}[/red]")
            console.print(f"[dim]Try manually: streamlit run ui/app.py --server.port 8520[/dim]")
        
        return

    elif args.command == "learn":
        console.print("\n[cyan]Learning from stored analysis findings...[/cyan]")
        console.print(f"[dim]Pattern detection threshold: {args.threshold} occurrences[/dim]\n")

        # Create learning engine
        learning_engine = LearningEngine(
            knowledge_base=ultrathink.knowledge_base,
            similarity_threshold=ultrathink.config.get('learning', {}).get('pattern_similarity_threshold', 0.8)
        )

        # Learn from findings
        result = learning_engine.learn_from_findings(occurrence_threshold=args.threshold)

        # Display learning summary with table
        summary_table = Table(title="Learning Results", show_header=False, border_style="cyan")
        summary_table.add_row("[cyan]Patterns Identified:[/cyan]", f"[bold]{result['patterns_identified']}[/bold]")
        summary_table.add_row("[cyan]Patches Generated:[/cyan]", f"[bold]{result['patches_generated']}[/bold]")
        console.print(summary_table)

        # Show identified patterns
        if result['patterns']:
            console.print("\n[bold cyan]=== PATTERNS IDENTIFIED ===[/bold cyan]")

            for i, pattern in enumerate(result['patterns'], 1):
                severity_color = {
                    "critical": "red",
                    "high": "orange",
                    "medium": "yellow",
                    "low": "blue"
                }.get(pattern['severity'].lower(), "white")

                console.print(f"\n[bold][{i}][/bold] {pattern['description']}")
                console.print(f"    [dim]Category:[/dim] {pattern['pattern_type']}")
                console.print(f"    [dim]Severity:[/dim] [{severity_color}]{pattern['severity']}[/{severity_color}]")
                console.print(f"    [dim]Frequency:[/dim] {pattern['frequency']} occurrences")
                console.print(f"    [dim]Affected files:[/dim] {len(pattern['affected_files'])}")
                if pattern['affected_files'][:3]:
                    console.print("    [dim]Examples:[/dim]")
                    for file in pattern['affected_files'][:3]:
                        console.print(f"      [dim]- {file}[/dim]")

        # Show generated patches
        if result['patches']:
            console.print("\n[bold cyan]=== PATCHES GENERATED ===[/bold cyan]")

            for i, patch in enumerate(result['patches'], 1):
                console.print(f"\n[bold green][{i}][/bold green] {patch['reason']}")
                if patch.get('template_file'):
                    console.print(f"    [dim]Target template:[/dim] {patch['template_file']}")
                if patch.get('line_pattern'):
                    pattern_preview = patch['line_pattern'][:60]
                    if len(patch['line_pattern']) > 60:
                        pattern_preview += "..."
                    console.print(f"    [dim]Pattern to match:[/dim] [yellow]{pattern_preview}[/yellow]")

        # Show learning statistics
        stats = learning_engine.get_learning_stats()

        stats_table = Table(title="Learning Statistics", show_header=False, border_style="cyan")
        stats_table.add_row("[cyan]Total findings analyzed:[/cyan]", str(stats['total_findings']))
        stats_table.add_row("[cyan]Total patterns identified:[/cyan]", str(stats['total_patterns']))
        stats_table.add_row("[cyan]Total patches available:[/cyan]", str(stats['total_patches']))
        stats_table.add_row("[cyan]Learning rate:[/cyan]", f"[bold]{stats['learning_rate']:.2%}[/bold]")

        console.print()
        console.print(stats_table)

        if stats['top_issues']:
            console.print("\n[cyan]Most common issues:[/cyan]")
            for issue in stats['top_issues'][:5]:
                console.print(f"  [yellow]-[/yellow] {issue['description']}: [bold]{issue['count']}[/bold] occurrences")

        if result['patches_generated'] > 0:
            console.print(Panel.fit(
                f"[green]SUCCESS: Learned {result['patches_generated']} improvements from code analysis[/green]\n"
                "[dim]These patches will be applied automatically in future scaffolding operations[/dim]",
                border_style="green"
            ))
        else:
            console.print(Panel.fit(
                "[yellow]INFO: No new patterns found[/yellow]\n"
                "[dim]Analyze more code to enable learning[/dim]",
                border_style="yellow"
            ))

    elif args.command == "handoff":
        console.print("\n[cyan]Generating AI handoff prompt...[/cyan]\n")
        
        # Detect or use specified project profile
        profile_mgr = ProfileManager()
        if args.profile == "auto":
            profile_name = profile_mgr.detect_profile(args.path)
        else:
            profile_name = args.profile
        profile = profile_mgr.load_profile(profile_name)
        
        console.print(f"[dim]Detected profile: {profile['name']}[/dim]\n")
        
        # Analyze the codebase
        result = await ultrathink.analyze_codebase(args.path, save_findings=False)
        
        # Generate handoff prompt with profile template
        analysis_text = generate_handoff_prompt(result, args.path)
        prompt = profile_mgr.get_handoff_template(profile_name, analysis_text)
        
        # Display the prompt
        console.print(Panel(prompt, title=f"[bold cyan]{profile['name']} - AI Handoff[/bold cyan]", border_style="cyan"))
        
        # Save to file
        output_file = Path("ultrathink_handoff.md")
        output_file.write_text(prompt, encoding='utf-8')
        console.print(f"\n[green]SUCCESS:[/green] Saved to [bold]{output_file}[/bold]")
        console.print("[dim]Copy and paste this prompt to your AI assistant[/dim]\n")


def generate_handoff_prompt(analysis_result: dict, path: str) -> str:
    """Generate a concise AI handoff prompt with best practices and errors."""
    summary = analysis_result.get("summary", {})
    results = analysis_result.get("results", [])
    
    # Count issues by severity
    critical = summary.get("critical_issues", 0)
    high = summary.get("high_priority_issues", 0)
    total = summary.get("total_issues", 0)
    
    # Build prompt
    prompt = f"""# Code Review - Fix Request

## Context
I analyzed `{path}` and found **{total} issues** that need fixing.

## Best Practices to Follow
- **Type Safety**: Add type hints to all functions
- **Error Handling**: Use specific exceptions, validate inputs
- **Security**: Avoid eval(), use parameterized queries
- **Code Quality**: Add docstrings, remove unused code
- **Performance**: Optimize loops, avoid redundant operations

## Issues Found ({total} total)
"""
    
    if critical > 0 or high > 0:
        prompt += f"\n**Priority**: {critical} critical, {high} high-severity issues\n"
    
    # Group findings by file
    for file_result in results:
        file_path = file_result.get("file", "Unknown")
        
        if 'error' in file_result:
            continue
            
        analysis = file_result.get("analysis", {})
        findings = analysis.get("findings", [])
        
        if not findings:
            continue
        
        # Show relative path
        try:
            rel_path = Path(file_path).relative_to(Path(path).parent)
        except:
            rel_path = Path(file_path).name
            
        prompt += f"\n### `{rel_path}`\n"
        
        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        sorted_findings = sorted(findings, key=lambda f: severity_order.get(f.get("severity", "info"), 5))
        
        for finding in sorted_findings[:10]:  # Limit to top 10 per file
            line = finding.get("line_number", "?")
            severity = finding.get("severity", "info").upper()
            category = finding.get("category", "unknown")
            description = finding.get("description", "No description")
            suggestion = finding.get("suggestion", "")
            
            # Emoji for severity (use text for Windows compatibility)
            emoji = {"CRITICAL": "[!]", "HIGH": "[!!]", "MEDIUM": "[*]", "LOW": "[-]", "INFO": "[i]"}.get(severity, "[i]")
            
            prompt += f"\n{emoji} **Line {line}** [{severity}] - {category}\n"
            prompt += f"- Issue: {description}\n"
            if suggestion:
                prompt += f"- Fix: {suggestion}\n"
    
    prompt += """\n## Your Task
Fix these issues following the best practices above. For each fix:
1. Show the corrected code
2. Explain what changed and why
3. Start with critical/high-severity issues
"""
    
    return prompt


def run() -> None:
    """Wrapper to run the async main function."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
