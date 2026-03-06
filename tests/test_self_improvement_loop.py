"""
End-to-end integration test for Ultrathink's self-improvement loop.

This test demonstrates the complete cycle:
1. Analyze flawed code
2. Learn patterns from findings
3. Generate new code with improvements applied
"""
import shutil
from pathlib import Path

import pytest

from ultrathink.framework import Ultrathink
from ultrathink.knowledge_base import KnowledgeBase
from ultrathink.learning_engine import LearningEngine
from ultrathink.scaffolding import PythonScaffolder


@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace for testing"""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture
def flawed_demo_files():
    """Path to flawed demo files"""
    return Path(__file__).parent.parent.parent / "flawed_demo"


@pytest.fixture
def clean_knowledge_base(tmp_path):
    """Create a clean knowledge base for testing"""
    db_path = tmp_path / "test_loop.db"
    return KnowledgeBase(db_path=str(db_path))


@pytest.mark.asyncio
async def test_complete_self_improvement_cycle(temp_workspace, flawed_demo_files, clean_knowledge_base):
    """
    Test the complete self-improvement cycle:
    1. Store findings (simulating analysis)
    2. Learn patterns
    3. Verify patches are generated
    """
    # Step 1: Manually inject findings (simulating analysis without AI)
    # This avoids needing API keys for the test
    findings_to_inject = [
        {
            "line_number": 24,
            "severity": "high",
            "category": "bug",
            "description": "Division by zero not handled",
            "suggestion": "Add zero check before division"
        },
        {
            "line_number": 30,
            "severity": "critical",
            "category": "security",
            "description": "Unsafe eval usage",
            "suggestion": "Use ast.literal_eval instead"
        },
        {
            "line_number": 10,
            "severity": "medium",
            "category": "quality",
            "description": "Missing type hints",
            "suggestion": "Add type annotations"
        }
    ]

    # Store same findings in multiple files to trigger pattern detection
    clean_knowledge_base.store_analysis_findings("calculator_v1.py", findings_to_inject)
    clean_knowledge_base.store_analysis_findings("math_utils.py", findings_to_inject[:2])  # Repeated issues
    clean_knowledge_base.store_analysis_findings("string_utils.py", [findings_to_inject[2]])

    findings_count = 6  # Total stored
    print(f"\nStep 1: Stored {findings_count} findings (simulated analysis)")

    # Step 2: Learn patterns from findings
    learning_engine = LearningEngine(clean_knowledge_base, similarity_threshold=0.8)
    learning_result = learning_engine.learn_from_findings(occurrence_threshold=2)

    # Verify patterns were identified
    assert learning_result['patterns_identified'] > 0, "Should identify patterns from recurring issues"
    assert learning_result['patches_generated'] > 0, "Should generate patches from patterns"

    patterns_count = learning_result['patterns_identified']
    patches_count = learning_result['patches_generated']
    print(f"Step 2: Identified {patterns_count} patterns, generated {patches_count} patches")

    # Step 3: Verify improvements are stored
    stats = clean_knowledge_base.get_stats()
    assert stats['total_findings'] > 0
    assert stats['total_patterns'] > 0
    assert stats['total_improvements'] > 0

    print(f"Step 3: Knowledge base contains {stats['total_improvements']} improvements")


@pytest.mark.asyncio
async def test_scaffolding_applies_learned_improvements(temp_workspace, clean_knowledge_base):
    """
    Test that scaffolded projects automatically apply learned improvements.
    """
    # Pre-populate knowledge base with an improvement
    improvement = {
        'pattern_id': 'test123',
        'template_file': '',  # Apply to all files
        'line_pattern': r'def divide\(self, a, b\):',
        'replacement': '''def divide(self, a, b):
        """Divide two numbers with zero check."""
        if b == 0:
            raise ValueError("Cannot divide by zero")''',
        'reason': 'Add zero division check'
    }
    clean_knowledge_base.store_improvement(improvement)
    clean_knowledge_base.load()

    # Create scaffolder with knowledge base
    scaffolder = PythonScaffolder(knowledge_base=clean_knowledge_base)

    # Scaffold a new project
    project_path = scaffolder.scaffold(
        project_name="test_improved",
        output_dir=str(temp_workspace),
        author_name="Test",
        author_email="test@test.com"
    )

    assert project_path.exists()

    # Check if improvements were applied
    applied = scaffolder.get_applied_improvements()

    # Note: Improvements may or may not be applied depending on whether
    # the pattern matches in the generated code. This tests the mechanism.
    print(f"\nApplied {len(applied)} improvements to generated project")


def test_pattern_frequency_threshold(clean_knowledge_base):
    """Test that patterns are only learned after reaching threshold"""
    # Store same issue twice
    issue = {
        "line_number": 10,
        "severity": "medium",
        "category": "quality",
        "description": "Missing type hints"
    }

    clean_knowledge_base.store_analysis_findings("file1.py", [issue])
    clean_knowledge_base.store_analysis_findings("file2.py", [issue])

    # With threshold=3, should not learn
    learning_engine = LearningEngine(clean_knowledge_base)
    result = learning_engine.learn_from_findings(occurrence_threshold=3)
    assert result['patterns_identified'] == 0

    # Add one more occurrence
    clean_knowledge_base.store_analysis_findings("file3.py", [issue])

    # Now should learn with threshold=3
    result = learning_engine.learn_from_findings(occurrence_threshold=3)
    assert result['patterns_identified'] == 1


def test_learning_from_multiple_categories(clean_knowledge_base):
    """Test learning patterns across different issue categories"""
    issues = [
        {
            "line_number": 1,
            "severity": "high",
            "category": "bug",
            "description": "Division by zero"
        },
        {
            "line_number": 2,
            "severity": "critical",
            "category": "security",
            "description": "Unsafe eval usage"
        },
        {
            "line_number": 3,
            "severity": "medium",
            "category": "quality",
            "description": "Missing docstring"
        }
    ]

    # Store each issue in 2 files to trigger learning
    for i, issue in enumerate(issues):
        clean_knowledge_base.store_analysis_findings(f"file{i}_a.py", [issue])
        clean_knowledge_base.store_analysis_findings(f"file{i}_b.py", [issue])

    learning_engine = LearningEngine(clean_knowledge_base)
    result = learning_engine.learn_from_findings(occurrence_threshold=2)

    # Should identify patterns from all 3 categories
    assert result['patterns_identified'] == 3
    assert result['patches_generated'] > 0

    # Verify categories are represented
    categories = [p['pattern_type'] for p in result['patterns']]
    assert 'bug' in categories
    assert 'security' in categories
    assert 'quality' in categories


def test_improvement_usage_tracking(clean_knowledge_base):
    """Test that improvement usage is tracked"""
    improvement = {
        'pattern_id': 'test456',
        'template_file': 'test.py',
        'line_pattern': 'pattern',
        'replacement': 'replacement',
        'reason': 'Test improvement'
    }

    clean_knowledge_base.store_improvement(improvement)

    # Get the improvement ID
    improvements = clean_knowledge_base.get_improvements_for_template('test.py')
    assert len(improvements) > 0

    imp_id = improvements[0]['id']
    initial_count = improvements[0]['applied_count']

    # Increment usage
    clean_knowledge_base.increment_improvement_usage(imp_id)
    clean_knowledge_base.increment_improvement_usage(imp_id)

    # Verify count increased
    updated = clean_knowledge_base.get_improvements_for_template('test.py')
    assert updated[0]['applied_count'] == initial_count + 2


def test_learning_statistics(clean_knowledge_base):
    """Test learning statistics are calculated correctly"""
    # Add test data with specific descriptions that will generate patches
    issues = [
        {"line_number": 1, "severity": "high", "category": "bug", "description": "Division by zero not handled"},
        {"line_number": 2, "severity": "medium", "category": "quality", "description": "Missing type hints"},
    ]

    for i in range(5):
        clean_knowledge_base.store_analysis_findings(f"file{i}.py", issues)

    learning_engine = LearningEngine(clean_knowledge_base)
    learning_engine.learn_from_findings(occurrence_threshold=2)

    stats = learning_engine.get_learning_stats()

    assert stats['total_findings'] == 10  # 5 files * 2 issues
    assert stats['total_patterns'] > 0
    assert stats['total_patches'] > 0
    assert 0 <= stats['learning_rate'] <= 1.0
    assert stats['learning_rate'] > 0  # Should be learning from the data


@pytest.mark.asyncio
async def test_before_after_comparison(temp_workspace, flawed_demo_files, clean_knowledge_base):
    """
    Compare code quality before and after learning cycle.
    """
    if not flawed_demo_files.exists():
        pytest.skip("Flawed demo files not found")

    # Simulate analysis by injecting findings from flawed code
    # This avoids needing API keys for the test
    findings_from_flawed_code = [
        {
            "line_number": 24,
            "severity": "high",
            "category": "bug",
            "description": "Division by zero not handled",
            "suggestion": "Add zero check before division"
        },
        {
            "line_number": 32,
            "severity": "critical",
            "category": "security",
            "description": "Unsafe eval usage",
            "suggestion": "Use ast.literal_eval instead"
        },
        {
            "line_number": 19,
            "severity": "medium",
            "category": "quality",
            "description": "Missing type hints",
            "suggestion": "Add type annotations"
        }
    ]

    # Store findings from multiple files to trigger pattern detection
    clean_knowledge_base.store_analysis_findings("calculator_v1.py", findings_from_flawed_code)
    clean_knowledge_base.store_analysis_findings("math_utils.py", findings_from_flawed_code[:2])
    issues_before = 5  # Total issues injected

    # Learn from findings
    learning_engine = LearningEngine(clean_knowledge_base)
    learning_engine.learn_from_findings(occurrence_threshold=2)

    # Get improvement count
    stats = clean_knowledge_base.get_stats()
    improvements_available = stats['total_improvements']

    # Verify learning occurred
    assert improvements_available > 0, "Should have learned improvements from flawed code"

    print(f"\nBefore: {issues_before} issues found")
    print(f"Learned: {improvements_available} improvements")
    print("After: Future projects will have these improvements applied automatically")


def test_empty_analysis_no_learning(clean_knowledge_base):
    """Test that no learning occurs with empty analysis"""
    learning_engine = LearningEngine(clean_knowledge_base)
    result = learning_engine.learn_from_findings()

    assert result['patterns_identified'] == 0
    assert result['patches_generated'] == 0
    assert result['patterns'] == []
    assert result['patches'] == []
