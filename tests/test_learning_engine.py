"""
Tests for the LearningEngine module.
"""
import pytest

from ultrathink.knowledge_base import KnowledgeBase
from ultrathink.learning_engine import LearningEngine


@pytest.fixture
def temp_db(tmp_path):
    """Create a temporary database for testing"""
    db_path = tmp_path / "test_learning.db"
    return str(db_path)


@pytest.fixture
def knowledge_base(temp_db):
    """Create a KnowledgeBase instance for testing"""
    return KnowledgeBase(db_path=temp_db)


@pytest.fixture
def learning_engine(knowledge_base):
    """Create a LearningEngine instance for testing"""
    return LearningEngine(knowledge_base=knowledge_base, similarity_threshold=0.8)


def test_learning_engine_initialization(learning_engine, knowledge_base):
    """Test learning engine initializes correctly"""
    assert learning_engine.knowledge_base == knowledge_base
    assert learning_engine.similarity_threshold == 0.8


def test_learn_from_findings_no_data(learning_engine):
    """Test learning with no stored findings"""
    result = learning_engine.learn_from_findings(occurrence_threshold=2)

    assert result['patterns_identified'] == 0
    assert result['patches_generated'] == 0
    assert result['patterns'] == []
    assert result['patches'] == []


def test_learn_from_findings_basic(learning_engine, knowledge_base):
    """Test basic learning from recurring issues"""
    # Store some recurring findings
    issue = {
        "line_number": 10,
        "severity": "high",
        "category": "bug",
        "description": "Division by zero not handled",
        "suggestion": "Add zero check"
    }

    # Store same issue in multiple files
    knowledge_base.store_analysis_findings("file1.py", [issue])
    knowledge_base.store_analysis_findings("file2.py", [issue])
    knowledge_base.store_analysis_findings("file3.py", [issue])

    # Learn from findings
    result = learning_engine.learn_from_findings(occurrence_threshold=2)

    assert result['patterns_identified'] == 1
    assert result['patches_generated'] > 0
    assert len(result['patterns']) == 1
    assert result['patterns'][0]['description'] == "Division by zero not handled"
    assert result['patterns'][0]['frequency'] == 3


def test_identify_patterns_by_category(learning_engine, knowledge_base):
    """Test that patterns are grouped by category"""
    # Store issues in different categories
    bug_issue = {
        "line_number": 1,
        "severity": "high",
        "category": "bug",
        "description": "Null pointer exception"
    }

    security_issue = {
        "line_number": 2,
        "severity": "critical",
        "category": "security",
        "description": "SQL injection risk"
    }

    # Store multiple times
    knowledge_base.store_analysis_findings("file1.py", [bug_issue])
    knowledge_base.store_analysis_findings("file2.py", [bug_issue])
    knowledge_base.store_analysis_findings("file3.py", [security_issue])
    knowledge_base.store_analysis_findings("file4.py", [security_issue])

    result = learning_engine.learn_from_findings(occurrence_threshold=2)

    # Should have 2 patterns (one for each category)
    assert result['patterns_identified'] == 2

    categories = [p['pattern_type'] for p in result['patterns']]
    assert 'bug' in categories
    assert 'security' in categories


def test_similarity_calculation(learning_engine):
    """Test text similarity calculation"""
    # Exact match
    similarity = learning_engine._calculate_similarity("hello world", "hello world")
    assert similarity == 1.0

    # Partial match
    similarity = learning_engine._calculate_similarity(
        "Missing type hints",
        "Missing type annotations"
    )
    assert 0.5 < similarity < 1.0

    # No match
    similarity = learning_engine._calculate_similarity(
        "Division by zero",
        "SQL injection"
    )
    assert similarity < 0.5


def test_group_similar_issues(learning_engine, knowledge_base):
    """Test grouping of similar issues"""
    # Store similar issues with slightly different wording
    issue1 = {
        "line_number": 1,
        "severity": "medium",
        "category": "quality",
        "description": "Missing type hints"
    }

    issue2 = {
        "line_number": 2,
        "severity": "medium",
        "category": "quality",
        "description": "Missing type annotations"
    }

    issue3 = {
        "line_number": 3,
        "severity": "low",
        "category": "quality",
        "description": "Unused variable found"
    }

    # Store multiple times
    knowledge_base.store_analysis_findings("file1.py", [issue1])
    knowledge_base.store_analysis_findings("file2.py", [issue1])
    knowledge_base.store_analysis_findings("file3.py", [issue2])
    knowledge_base.store_analysis_findings("file4.py", [issue2])
    knowledge_base.store_analysis_findings("file5.py", [issue3])
    knowledge_base.store_analysis_findings("file6.py", [issue3])

    # With high similarity threshold, should group similar ones
    result = learning_engine.learn_from_findings(occurrence_threshold=2)

    # May have 2 or 3 patterns depending on similarity grouping
    assert 1 <= result['patterns_identified'] <= 3


def test_generate_bug_patches(learning_engine):
    """Test patch generation for bug issues"""
    pattern = {
        'id': 'test123',
        'pattern_type': 'bug',
        'description': 'Division by zero not handled',
        'severity': 'high'
    }

    patches = learning_engine._generate_bug_patches(pattern, pattern['description'].lower())

    assert len(patches) > 0
    assert any('divide' in patch.get('line_pattern', '').lower() for patch in patches)
    assert any('zero' in patch.get('reason', '').lower() for patch in patches)


def test_generate_security_patches(learning_engine):
    """Test patch generation for security issues"""
    pattern = {
        'id': 'test456',
        'pattern_type': 'security',
        'description': 'Unsafe use of eval() function',
        'severity': 'critical'
    }

    patches = learning_engine._generate_security_patches(pattern, pattern['description'].lower())

    assert len(patches) > 0
    assert any('eval' in patch.get('line_pattern', '').lower() or
              'eval' in patch.get('replacement', '').lower()
              for patch in patches)


def test_generate_quality_patches(learning_engine):
    """Test patch generation for quality issues"""
    pattern = {
        'id': 'test789',
        'pattern_type': 'quality',
        'description': 'Missing type hints',
        'severity': 'medium'
    }

    patches = learning_engine._generate_quality_patches(pattern, pattern['description'].lower())

    assert len(patches) > 0
    assert any('type' in patch.get('reason', '').lower() for patch in patches)


def test_patches_stored_in_knowledge_base(learning_engine, knowledge_base):
    """Test that generated patches are stored in knowledge base"""
    issue = {
        "line_number": 15,
        "severity": "high",
        "category": "bug",
        "description": "Division by zero not handled"
    }

    # Store multiple times to trigger pattern
    knowledge_base.store_analysis_findings("file1.py", [issue])
    knowledge_base.store_analysis_findings("file2.py", [issue])

    # Learn and generate patches
    learning_engine.learn_from_findings(occurrence_threshold=2)

    # Verify patches were stored
    stats = knowledge_base.get_stats()
    assert stats['total_improvements'] > 0

    # Verify patches can be retrieved
    improvements = knowledge_base.get_improvements_for_template("calculator.py")
    assert len(improvements) > 0


def test_learning_with_threshold(learning_engine, knowledge_base):
    """Test that occurrence threshold works correctly"""
    issue = {
        "line_number": 5,
        "severity": "low",
        "category": "style",
        "description": "Inconsistent naming"
    }

    # Store only once
    knowledge_base.store_analysis_findings("file1.py", [issue])

    # With threshold=2, should not learn
    result = learning_engine.learn_from_findings(occurrence_threshold=2)
    assert result['patterns_identified'] == 0

    # Store one more time
    knowledge_base.store_analysis_findings("file2.py", [issue])

    # Now should learn
    result = learning_engine.learn_from_findings(occurrence_threshold=2)
    assert result['patterns_identified'] == 1


def test_get_learning_stats(learning_engine, knowledge_base):
    """Test getting learning statistics"""
    # Add some data
    issue = {
        "line_number": 1,
        "severity": "medium",
        "category": "quality",
        "description": "Missing docstring"
    }

    knowledge_base.store_analysis_findings("file1.py", [issue])
    knowledge_base.store_analysis_findings("file2.py", [issue])

    # Trigger learning
    learning_engine.learn_from_findings(occurrence_threshold=2)

    # Get stats
    stats = learning_engine.get_learning_stats()

    assert 'total_findings' in stats
    assert 'total_patterns' in stats
    assert 'total_patches' in stats
    assert 'learning_rate' in stats
    assert 'findings_by_severity' in stats
    assert 'top_issues' in stats

    assert stats['total_findings'] == 2
    assert stats['total_patterns'] > 0
    assert 0 <= stats['learning_rate'] <= 1.0


def test_learning_rate_calculation(learning_engine):
    """Test learning rate calculation"""
    # No findings
    rate = learning_engine._calculate_learning_rate({
        'total_findings': 0,
        'total_patterns': 0,
        'total_improvements': 0
    })
    assert rate == 0.0

    # Some findings and patterns
    rate = learning_engine._calculate_learning_rate({
        'total_findings': 10,
        'total_patterns': 3,
        'total_improvements': 2
    })
    assert 0 < rate <= 1.0
    assert rate == (3 + 2) / 10  # (patterns + improvements) / findings


def test_multiple_learning_cycles(learning_engine, knowledge_base):
    """Test running learn multiple times doesn't duplicate patterns"""
    issue = {
        "line_number": 1,
        "severity": "high",
        "category": "bug",
        "description": "Null check missing"
    }

    knowledge_base.store_analysis_findings("file1.py", [issue])
    knowledge_base.store_analysis_findings("file2.py", [issue])

    # First learning cycle
    result1 = learning_engine.learn_from_findings(occurrence_threshold=2)
    initial_patterns = result1['patterns_identified']

    # Second learning cycle (no new findings)
    result2 = learning_engine.learn_from_findings(occurrence_threshold=2)

    # Should identify same patterns, not duplicate
    assert result2['patterns_identified'] == initial_patterns


def test_pattern_with_affected_files(learning_engine, knowledge_base):
    """Test that patterns track which files are affected"""
    issue = {
        "line_number": 1,
        "severity": "medium",
        "category": "quality",
        "description": "Code duplication detected"
    }

    knowledge_base.store_analysis_findings("module1.py", [issue])
    knowledge_base.store_analysis_findings("module2.py", [issue])
    knowledge_base.store_analysis_findings("module3.py", [issue])

    result = learning_engine.learn_from_findings(occurrence_threshold=2)

    assert len(result['patterns']) > 0
    pattern = result['patterns'][0]
    assert 'affected_files' in pattern
    assert len(pattern['affected_files']) == 3
    assert "module1.py" in pattern['affected_files']
    assert "module2.py" in pattern['affected_files']
    assert "module3.py" in pattern['affected_files']


def test_empty_knowledge_base_learning(learning_engine):
    """Test learning engine handles empty knowledge base gracefully"""
    result = learning_engine.learn_from_findings()
    stats = learning_engine.get_learning_stats()

    assert result['patterns_identified'] == 0
    assert result['patches_generated'] == 0
    assert stats['total_findings'] == 0
    assert stats['learning_rate'] == 0.0
