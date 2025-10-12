"""
Tests for the KnowledgeBase module.
"""
import sqlite3
from pathlib import Path

import pytest

from ultrathink.knowledge_base import KnowledgeBase


@pytest.fixture
def temp_db(tmp_path):
    """Create a temporary database for testing"""
    db_path = tmp_path / "test_knowledge.db"
    return str(db_path)


@pytest.fixture
def knowledge_base(temp_db):
    """Create a KnowledgeBase instance for testing"""
    return KnowledgeBase(db_path=temp_db)


def test_knowledge_base_initialization(knowledge_base, temp_db):
    """Test knowledge base initializes and creates database"""
    assert knowledge_base.db_path == temp_db
    assert Path(temp_db).exists()

    # Verify tables were created
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    assert 'findings' in tables
    assert 'patterns' in tables
    assert 'improvements' in tables

    conn.close()


def test_store_analysis_findings(knowledge_base, temp_db):
    """Test storing analysis findings"""
    findings = [
        {
            "line_number": 10,
            "severity": "high",
            "category": "bug",
            "description": "Division by zero not handled",
            "suggestion": "Add zero check before division"
        },
        {
            "line_number": 15,
            "severity": "medium",
            "category": "quality",
            "description": "Missing type hints",
            "suggestion": "Add type annotations"
        }
    ]

    knowledge_base.store_analysis_findings(
        file_path="test_file.py",
        findings=findings
    )

    # Verify findings were stored
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM findings WHERE file_path = 'test_file.py'")
    count = cursor.fetchone()[0]
    assert count == 2

    cursor.execute("SELECT severity, category, description FROM findings WHERE file_path = 'test_file.py'")
    stored_findings = cursor.fetchall()

    assert ('high', 'bug', 'Division by zero not handled') in stored_findings
    assert ('medium', 'quality', 'Missing type hints') in stored_findings

    conn.close()


def test_store_duplicate_findings(knowledge_base, temp_db):
    """Test that duplicate findings are handled properly"""
    finding = {
        "line_number": 10,
        "severity": "high",
        "category": "bug",
        "description": "Division by zero not handled",
        "suggestion": "Add zero check"
    }

    # Store same finding twice
    knowledge_base.store_analysis_findings("test.py", [finding])
    knowledge_base.store_analysis_findings("test.py", [finding])

    # Should only have one entry (UNIQUE constraint)
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM findings WHERE file_path = 'test.py'")
    count = cursor.fetchone()[0]
    assert count == 1
    conn.close()


def test_get_recurring_issues(knowledge_base):
    """Test finding recurring issues across multiple files"""
    # Store same issue in multiple files
    issue = {
        "line_number": 10,
        "severity": "medium",
        "category": "quality",
        "description": "Missing docstring",
        "suggestion": "Add docstring"
    }

    knowledge_base.store_analysis_findings("file1.py", [issue])
    knowledge_base.store_analysis_findings("file2.py", [issue])
    knowledge_base.store_analysis_findings("file3.py", [issue])

    # Find recurring issues with threshold of 2
    recurring = knowledge_base.get_recurring_issues(threshold=2)

    assert len(recurring) == 1
    assert recurring[0]['description'] == "Missing docstring"
    assert recurring[0]['frequency'] == 3
    assert recurring[0]['category'] == "quality"
    assert len(recurring[0]['affected_files']) == 3


def test_get_recurring_issues_threshold(knowledge_base):
    """Test recurring issues respects threshold"""
    issue1 = {"line_number": 1, "severity": "low", "category": "style", "description": "Issue A"}
    issue2 = {"line_number": 2, "severity": "medium", "category": "quality", "description": "Issue B"}

    # Issue A appears 2 times
    knowledge_base.store_analysis_findings("file1.py", [issue1])
    knowledge_base.store_analysis_findings("file2.py", [issue1])

    # Issue B appears 4 times
    knowledge_base.store_analysis_findings("file3.py", [issue2])
    knowledge_base.store_analysis_findings("file4.py", [issue2])
    knowledge_base.store_analysis_findings("file5.py", [issue2])
    knowledge_base.store_analysis_findings("file6.py", [issue2])

    # With threshold=3, only Issue B should appear
    recurring = knowledge_base.get_recurring_issues(threshold=3)
    assert len(recurring) == 1
    assert recurring[0]['description'] == "Issue B"
    assert recurring[0]['frequency'] == 4


def test_store_pattern(knowledge_base, temp_db):
    """Test storing a pattern"""
    pattern = {
        "pattern_type": "code_smell",
        "description": "Long parameter list",
        "context": {"max_params": 5}
    }

    knowledge_base.store_pattern(pattern)

    # Verify pattern was stored in database
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT pattern_type, description FROM patterns")
    result = cursor.fetchone()

    assert result[0] == "code_smell"
    assert result[1] == "Long parameter list"
    conn.close()

    # Also check in-memory list
    assert len(knowledge_base.patterns) == 1


def test_store_pattern_duplicate_increments_frequency(knowledge_base, temp_db):
    """Test that storing same pattern increments frequency"""
    pattern = {
        "pattern_type": "code_smell",
        "description": "Long parameter list",
        "context": {}
    }

    knowledge_base.store_pattern(pattern)
    knowledge_base.store_pattern(pattern)
    knowledge_base.store_pattern(pattern)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT frequency FROM patterns WHERE description = 'Long parameter list'")
    frequency = cursor.fetchone()[0]
    assert frequency == 3
    conn.close()


def test_save_and_load(knowledge_base, temp_db):
    """Test save and load functionality"""
    # Store some data
    findings = [
        {"line_number": 5, "severity": "high", "category": "security", "description": "SQL injection risk"}
    ]
    knowledge_base.store_analysis_findings("app.py", findings)

    pattern = {"pattern_type": "security", "description": "Unsafe SQL query"}
    knowledge_base.store_pattern(pattern)

    improvement = {
        "pattern_id": "test123",
        "template_file": "main.py",
        "line_pattern": "db.execute(query)",
        "replacement": "db.execute(query, params)",
        "reason": "Prevent SQL injection"
    }
    knowledge_base.store_improvement(improvement)

    # Save and create new instance
    knowledge_base.save()
    new_kb = KnowledgeBase(db_path=temp_db)
    new_kb.load()

    # Verify loaded data
    assert len(new_kb.patterns) == 1
    assert new_kb.patterns[0]['description'] == "Unsafe SQL query"

    assert len(new_kb.improvements) == 1
    assert new_kb.improvements[0]['template_file'] == "main.py"


def test_store_improvement(knowledge_base, temp_db):
    """Test storing an improvement/patch"""
    improvement = {
        "pattern_id": "abc123",
        "template_file": "calculator.py",
        "line_pattern": "def divide(a, b):",
        "replacement": "def divide(a, b):\\n    if b == 0:\\n        raise ValueError('Cannot divide by zero')",
        "reason": "Add zero division check"
    }

    knowledge_base.store_improvement(improvement)

    # Verify in database
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT template_file, reason FROM improvements")
    result = cursor.fetchone()

    assert result[0] == "calculator.py"
    assert result[1] == "Add zero division check"
    conn.close()


def test_get_improvements_for_template(knowledge_base):
    """Test retrieving improvements for a specific template"""
    imp1 = {
        "template_file": "calculator.py",
        "line_pattern": "def divide",
        "replacement": "improved_code",
        "reason": "Fix division"
    }

    imp2 = {
        "template_file": "calculator.py",
        "line_pattern": "def multiply",
        "replacement": "improved_code2",
        "reason": "Fix multiplication"
    }

    imp3 = {
        "template_file": "other.py",
        "line_pattern": "def foo",
        "replacement": "improved_code3",
        "reason": "Fix foo"
    }

    knowledge_base.store_improvement(imp1)
    knowledge_base.store_improvement(imp2)
    knowledge_base.store_improvement(imp3)

    # Get improvements for calculator.py
    improvements = knowledge_base.get_improvements_for_template("calculator.py")

    assert len(improvements) == 2
    reasons = [imp['reason'] for imp in improvements]
    assert "Fix division" in reasons
    assert "Fix multiplication" in reasons
    assert "Fix foo" not in reasons


def test_increment_improvement_usage(knowledge_base, temp_db):
    """Test incrementing improvement usage count"""
    improvement = {
        "template_file": "test.py",
        "line_pattern": "pattern",
        "replacement": "replacement",
        "reason": "test"
    }

    knowledge_base.store_improvement(improvement)

    # Get the improvement ID
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM improvements WHERE template_file = 'test.py'")
    imp_id = cursor.fetchone()[0]
    conn.close()

    # Increment usage
    knowledge_base.increment_improvement_usage(imp_id)
    knowledge_base.increment_improvement_usage(imp_id)

    # Verify count
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT applied_count FROM improvements WHERE id = ?", (imp_id,))
    count = cursor.fetchone()[0]
    assert count == 2
    conn.close()


def test_get_stats(knowledge_base):
    """Test getting knowledge base statistics"""
    # Add some data
    findings = [
        {"line_number": 1, "severity": "critical", "category": "security", "description": "Issue 1"},
        {"line_number": 2, "severity": "high", "category": "bug", "description": "Issue 2"},
        {"line_number": 3, "severity": "high", "category": "bug", "description": "Issue 2"}  # duplicate
    ]
    knowledge_base.store_analysis_findings("file.py", findings)

    pattern = {"pattern_type": "test", "description": "Test pattern"}
    knowledge_base.store_pattern(pattern)

    improvement = {"template_file": "test.py", "reason": "test"}
    knowledge_base.store_improvement(improvement)

    # Get stats
    stats = knowledge_base.get_stats()

    assert stats['total_findings'] == 3
    assert stats['total_patterns'] == 1
    assert stats['total_improvements'] == 1
    assert 'critical' in stats['findings_by_severity']
    assert 'high' in stats['findings_by_severity']
    assert len(stats['top_issues']) > 0


def test_findings_with_raw_response(knowledge_base):
    """Test that findings with raw_response are stored properly"""
    finding = {
        "line_number": None,
        "severity": "info",
        "category": "unknown",
        "raw_response": "Some unstructured AI response"
    }

    knowledge_base.store_analysis_findings("test.py", [finding])

    recurring = knowledge_base.get_recurring_issues(threshold=1)
    assert len(recurring) == 1
    assert recurring[0]['description'] == "Some unstructured AI response"


def test_empty_knowledge_base(knowledge_base):
    """Test operations on empty knowledge base"""
    recurring = knowledge_base.get_recurring_issues()
    assert recurring == []

    improvements = knowledge_base.get_improvements_for_template("any.py")
    assert improvements == []

    stats = knowledge_base.get_stats()
    assert stats['total_findings'] == 0
    assert stats['total_patterns'] == 0
    assert stats['total_improvements'] == 0
