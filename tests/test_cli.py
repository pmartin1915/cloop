"""
Integration tests for the Ultrathink CLI.
"""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from ultrathink.cli import main
from ultrathink.models import AIModel, AnalysisResult, TaskType


@pytest.fixture
def sample_code_file(tmp_path):
    """Create a sample Python file for testing"""
    code_file = tmp_path / "test_code.py"
    code_file.write_text("""
def add(a, b):
    return a + b

def divide(a, b):
    return a / b
""")
    return tmp_path


@pytest.fixture
def mock_analysis_result():
    """Create a mock analysis result with structured findings"""
    return AnalysisResult(
        task_type=TaskType.CODE_REVIEW,
        findings=[
            {
                "line_number": 5,
                "severity": "high",
                "category": "bug",
                "description": "Division by zero not handled",
                "suggestion": "Add check for b != 0 before division"
            },
            {
                "line_number": 2,
                "severity": "low",
                "category": "quality",
                "description": "Missing type hints",
                "suggestion": "Add type annotations: def add(a: int, b: int) -> int"
            }
        ],
        suggestions=[
            "Add check for b != 0 before division",
            "Add type annotations: def add(a: int, b: int) -> int"
        ],
        confidence=0.9,
        model_used=AIModel.CLAUDE_OPUS.value,
        timestamp="2025-01-15T10:00:00"
    )


@pytest.mark.asyncio
async def test_cli_analyze_basic(sample_code_file, mock_analysis_result, capsys):
    """Test basic analyze command"""
    with patch('ultrathink.cli.Ultrathink') as mock_ultrathink:
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.analyze_codebase = AsyncMock(return_value={
            "results": [
                {
                    "file": str(sample_code_file / "test_code.py"),
                    "parse_info": {
                        "language": "python",
                        "functions": [{"name": "add"}, {"name": "divide"}]
                    },
                    "analysis": {
                        "task_type": "code_review",
                        "findings": mock_analysis_result.findings,
                        "suggestions": mock_analysis_result.suggestions,
                        "confidence": 0.9,
                        "model_used": "claude-opus-4-1-20250805",
                        "timestamp": "2025-01-15T10:00:00"
                    }
                }
            ],
            "summary": {
                "files_analyzed": 1,
                "files_with_errors": 0,
                "total_issues": 2,
                "critical_issues": 0,
                "high_priority_issues": 1,
                "severity_breakdown": {
                    "critical": 0,
                    "high": 1,
                    "medium": 0,
                    "low": 1,
                    "info": 0
                },
                "category_breakdown": {
                    "bug": 1,
                    "quality": 1
                }
            }
        })
        mock_ultrathink.return_value = mock_instance

        # Run CLI
        with patch('sys.argv', ['ultrathink', 'analyze', '--path', str(sample_code_file)]):
            await main()

        # Verify output
        captured = capsys.readouterr()
        assert "ANALYSIS RESULTS" in captured.out
        assert "Files analyzed: 1" in captured.out
        assert "Total issues found: 2" in captured.out
        assert "HIGH (bug)" in captured.out
        assert "Division by zero not handled" in captured.out


@pytest.mark.asyncio
async def test_cli_analyze_no_issues(sample_code_file, capsys):
    """Test analyze command with no issues found"""
    with patch('ultrathink.cli.Ultrathink') as mock_ultrathink:
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.analyze_codebase = AsyncMock(return_value={
            "results": [
                {
                    "file": str(sample_code_file / "test_code.py"),
                    "parse_info": {"language": "python"},
                    "analysis": {
                        "findings": [],
                        "suggestions": [],
                        "confidence": 1.0
                    }
                }
            ],
            "summary": {
                "files_analyzed": 1,
                "files_with_errors": 0,
                "total_issues": 0,
                "critical_issues": 0,
                "high_priority_issues": 0,
                "severity_breakdown": {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                    "info": 0
                },
                "category_breakdown": {}
            }
        })
        mock_ultrathink.return_value = mock_instance

        # Run CLI
        with patch('sys.argv', ['ultrathink', 'analyze', '--path', str(sample_code_file)]):
            await main()

        # Verify output
        captured = capsys.readouterr()
        assert "Total issues found: 0" in captured.out
        assert "No issues found" in captured.out


@pytest.mark.asyncio
async def test_cli_analyze_with_errors(sample_code_file, capsys):
    """Test analyze command when file processing has errors"""
    with patch('ultrathink.cli.Ultrathink') as mock_ultrathink:
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.analyze_codebase = AsyncMock(return_value={
            "results": [
                {
                    "file": str(sample_code_file / "broken.py"),
                    "error": "Syntax error: unexpected EOF"
                }
            ],
            "summary": {
                "files_analyzed": 1,
                "files_with_errors": 1,
                "total_issues": 0,
                "critical_issues": 0,
                "high_priority_issues": 0,
                "severity_breakdown": {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                    "info": 0
                },
                "category_breakdown": {}
            }
        })
        mock_ultrathink.return_value = mock_instance

        # Run CLI
        with patch('sys.argv', ['ultrathink', 'analyze', '--path', str(sample_code_file)]):
            await main()

        # Verify output
        captured = capsys.readouterr()
        assert "Files analyzed: 1" in captured.out
        assert "[ERROR]" in captured.out
        assert "Syntax error" in captured.out


@pytest.mark.asyncio
async def test_cli_analyze_multiple_files(tmp_path, capsys):
    """Test analyze command with multiple files"""
    # Create multiple test files
    (tmp_path / "file1.py").write_text("def func1(): pass")
    (tmp_path / "file2.py").write_text("def func2(): pass")

    with patch('ultrathink.cli.Ultrathink') as mock_ultrathink:
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.analyze_codebase = AsyncMock(return_value={
            "results": [
                {
                    "file": str(tmp_path / "file1.py"),
                    "parse_info": {"language": "python"},
                    "analysis": {
                        "findings": [{"line_number": 1, "severity": "info", "category": "style", "description": "Test"}],
                        "suggestions": []
                    }
                },
                {
                    "file": str(tmp_path / "file2.py"),
                    "parse_info": {"language": "python"},
                    "analysis": {
                        "findings": [{"line_number": 1, "severity": "medium", "category": "quality", "description": "Test2"}],
                        "suggestions": []
                    }
                }
            ],
            "summary": {
                "files_analyzed": 2,
                "files_with_errors": 0,
                "total_issues": 2,
                "critical_issues": 0,
                "high_priority_issues": 0,
                "severity_breakdown": {
                    "critical": 0,
                    "high": 0,
                    "medium": 1,
                    "low": 0,
                    "info": 1
                },
                "category_breakdown": {
                    "style": 1,
                    "quality": 1
                }
            }
        })
        mock_ultrathink.return_value = mock_instance

        # Run CLI
        with patch('sys.argv', ['ultrathink', 'analyze', '--path', str(tmp_path)]):
            await main()

        # Verify output
        captured = capsys.readouterr()
        assert "Files analyzed: 2" in captured.out
        assert "file1.py" in captured.out
        assert "file2.py" in captured.out


@pytest.mark.asyncio
async def test_cli_init_command(capsys):
    """Test init command"""
    with patch('ultrathink.cli.Ultrathink') as mock_ultrathink:
        mock_instance = MagicMock()
        mock_instance.initialize = MagicMock()
        mock_ultrathink.return_value = mock_instance

        # Run CLI
        with patch('sys.argv', ['ultrathink', 'init']):
            await main()

        # Verify
        mock_instance.initialize.assert_called_once()
        captured = capsys.readouterr()
        assert "initialized successfully" in captured.out


@pytest.mark.asyncio
async def test_cli_stats_command(capsys):
    """Test stats command"""
    with patch('ultrathink.cli.Ultrathink') as mock_ultrathink:
        mock_instance = MagicMock()
        mock_instance.initialize = MagicMock()
        mock_instance.get_stats = MagicMock(return_value={
            "improvement_cycles": 5,
            "patterns_stored": 10,
            "improvements_recorded": 15
        })
        mock_ultrathink.return_value = mock_instance

        # Run CLI
        with patch('sys.argv', ['ultrathink', 'stats']):
            await main()

        # Verify
        captured = capsys.readouterr()
        assert "improvement_cycles: 5" in captured.out
        assert "patterns_stored: 10" in captured.out
        assert "improvements_recorded: 15" in captured.out


def test_cli_scaffold_command(tmp_path, capsys):
    """Test scaffold command (synchronous, doesn't need Ultrathink init)"""
    from ultrathink.cli import run

    with patch('ultrathink.cli.PythonScaffolder') as mock_scaffolder:
        mock_instance = MagicMock()
        mock_instance.scaffold = MagicMock(return_value=tmp_path / "myapi")
        mock_scaffolder.return_value = mock_instance

        # Run CLI
        with patch('sys.argv', ['ultrathink', 'scaffold', '--name', 'myapi', '--path', str(tmp_path)]):
            try:
                run()
            except SystemExit:
                pass  # argparse may call sys.exit

        # Verify scaffolder was called
        mock_instance.scaffold.assert_called_once()


@pytest.mark.asyncio
async def test_cli_analyze_severity_display(sample_code_file, capsys):
    """Test that severity breakdown is displayed correctly"""
    with patch('ultrathink.cli.Ultrathink') as mock_ultrathink:
        # Setup mock with various severities
        mock_instance = MagicMock()
        mock_instance.analyze_codebase = AsyncMock(return_value={
            "results": [{
                "file": str(sample_code_file / "test.py"),
                "analysis": {
                    "findings": [
                        {"line_number": 1, "severity": "critical", "category": "security", "description": "SQL injection risk"},
                        {"line_number": 2, "severity": "high", "category": "bug", "description": "Null pointer"},
                        {"line_number": 3, "severity": "medium", "category": "performance", "description": "Inefficient loop"},
                        {"line_number": 4, "severity": "low", "category": "style", "description": "Naming convention"},
                        {"line_number": 5, "severity": "info", "category": "info", "description": "Consider refactoring"}
                    ]
                }
            }],
            "summary": {
                "files_analyzed": 1,
                "total_issues": 5,
                "critical_issues": 1,
                "high_priority_issues": 1,
                "severity_breakdown": {
                    "critical": 1,
                    "high": 1,
                    "medium": 1,
                    "low": 1,
                    "info": 1
                },
                "category_breakdown": {
                    "security": 1,
                    "bug": 1,
                    "performance": 1,
                    "style": 1,
                    "info": 1
                }
            }
        })
        mock_ultrathink.return_value = mock_instance

        # Run CLI
        with patch('sys.argv', ['ultrathink', 'analyze', '--path', str(sample_code_file)]):
            await main()

        # Verify all severities displayed
        captured = capsys.readouterr()
        assert "critical: 1" in captured.out
        assert "high: 1" in captured.out
        assert "medium: 1" in captured.out
        assert "low: 1" in captured.out
        assert "info: 1" in captured.out
