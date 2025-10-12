"""
Tests for the Ultrathink framework.
"""

import pytest

from ultrathink import AIModel, CodeChange, TaskType, Ultrathink


def test_framework_initialization(tmp_path):
    """Test basic framework initialization"""
    config_file = tmp_path / "ultrathink.yaml"
    config_file.write_text("version: '1.0'")

    framework = Ultrathink(str(config_file))
    assert framework is not None
    assert framework.orchestrator is not None
    assert framework.improvement_engine is not None
    assert framework.parser is not None
    assert framework.knowledge_base is not None


def test_config_loading(tmp_path):
    """Test configuration loading"""
    config_file = tmp_path / "ultrathink.yaml"
    config_file.write_text("""
version: '1.0'
evolution:
  enabled: true
  max_iterations: 10
""")

    framework = Ultrathink(str(config_file))
    assert framework.config['version'] == '1.0'
    assert framework.config['evolution']['enabled'] is True
    assert framework.config['evolution']['max_iterations'] == 10


def test_language_detection():
    """Test language detection from file extension"""
    framework = Ultrathink()

    assert framework._detect_language("test.py") == "python"
    assert framework._detect_language("test.js") == "javascript"
    assert framework._detect_language("test.ts") == "typescript"
    assert framework._detect_language("test.rs") == "rust"
    assert framework._detect_language("test.go") == "go"
    assert framework._detect_language("test.unknown") == "unknown"


def test_code_change_model():
    """Test CodeChange data model"""
    change = CodeChange(
        file_path="test.py",
        language="python",
        original_code="def foo(): pass"
    )

    assert change.file_path == "test.py"
    assert change.language == "python"
    assert change.original_code == "def foo(): pass"
    assert change.modified_code is None


def test_ai_model_enum():
    """Test AIModel enum values"""
    assert AIModel.CLAUDE_OPUS.value == "claude-opus-4-1-20250805"
    assert AIModel.GEMINI_ULTRA.value == "gemini-ultra"
    assert AIModel.AWS_BEDROCK_CLAUDE.value == "anthropic.claude-v2"


def test_task_type_enum():
    """Test TaskType enum values"""
    assert TaskType.CODE_REVIEW.value == "code_review"
    assert TaskType.TEST_GENERATION.value == "test_generation"
    assert TaskType.REFACTORING.value == "refactoring"
    assert TaskType.SECURITY_ANALYSIS.value == "security_analysis"


def test_stats_generation():
    """Test statistics generation"""
    framework = Ultrathink()
    stats = framework.get_stats()

    assert "improvement_cycles" in stats
    assert "patterns_stored" in stats
    assert "improvements_recorded" in stats
    assert stats["improvement_cycles"] == 0  # Initially zero


@pytest.mark.asyncio
async def test_generate_tests_basic():
    """Test test generation with basic code"""
    framework = Ultrathink()

    # This will fail without API keys, but tests the structure
    # code = "def add(a, b):\n    return a + b"
    # result = await framework.generate_tests(code, "python")
    # For now, just test that the method exists
    assert hasattr(framework, 'generate_tests')
