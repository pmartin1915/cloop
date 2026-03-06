"""
Tests for the PatchEngine module.
"""
import pytest

from ultrathink.patch_engine import PatchEngine, SmartPatcher


@pytest.fixture
def patch_engine():
    """Create a PatchEngine instance for testing"""
    return PatchEngine()


@pytest.fixture
def smart_patcher():
    """Create a SmartPatcher instance for testing"""
    return SmartPatcher()


def test_patch_engine_initialization(patch_engine):
    """Test patch engine initializes correctly"""
    assert patch_engine is not None
    assert patch_engine.applied_patches == []
    assert patch_engine.failed_patches == []


def test_apply_simple_regex_patch(patch_engine):
    """Test applying a simple regex patch"""
    code = """def divide(a, b):
    return a / b
"""

    patch = {
        'line_pattern': r'def divide\(a, b\):',
        'replacement': '''def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")'''
    }

    result = patch_engine.apply_patch(code, patch)

    assert result['applied'] is True
    assert 'Cannot divide by zero' in result['code']
    assert 'raise ValueError' in result['code']


def test_apply_patch_pattern_not_found(patch_engine):
    """Test patch when pattern is not found"""
    code = "def multiply(a, b):\n    return a * b"

    patch = {
        'line_pattern': r'def divide\(.*\):',
        'replacement': 'replacement code'
    }

    result = patch_engine.apply_patch(code, patch)

    assert result['applied'] is False
    assert result['code'] == code
    assert 'not found' in result['message'].lower()


def test_apply_patch_with_invalid_syntax(patch_engine):
    """Test that patch producing invalid syntax is rejected"""
    code = """def foo():
    return 42
"""

    patch = {
        'line_pattern': r'return 42',
        'replacement': 'return invalid syntax here )'  # Invalid Python
    }

    result = patch_engine.apply_patch(code, patch)

    # Should detect invalid syntax and reject
    assert result['applied'] is False or 'invalid syntax' in result['message'].lower()


def test_apply_multiple_patches(patch_engine):
    """Test applying multiple patches to code"""
    code = """def divide(a, b):
    return a / b

def multiply(a, b):
    return a * b
"""

    patches = [
        {
            'line_pattern': r'def divide\(a, b\):',
            'replacement': '''def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")'''
        },
        {
            'line_pattern': r'def multiply\(a, b\):',
            'replacement': '''def multiply(a: int, b: int) -> int:  # Added type hints'''
        }
    ]

    patched_code, report = patch_engine.apply_patches(code, patches)

    assert len(report) == 2
    assert 'Division by zero' in patched_code
    assert 'type hints' in patched_code


def test_apply_patches_with_some_failures(patch_engine):
    """Test applying patches where some succeed and some fail"""
    code = "def foo():\n    pass"

    patches = [
        {
            'line_pattern': r'def foo\(\):',
            'replacement': 'def foo():  # Updated'
        },
        {
            'line_pattern': r'def bar\(\):',  # This won't match
            'replacement': 'def bar():  # This'
        }
    ]

    patched_code, report = patch_engine.apply_patches(code, patches)

    assert len(report) == 2
    assert report[0]['status'] == 'applied'
    assert report[1]['status'] in ['skipped', 'error']
    assert '# Updated' in patched_code


def test_validate_python_syntax(patch_engine):
    """Test Python syntax validation"""
    valid_code = "def foo():\n    return 42"
    invalid_code = "def foo(\n    invalid"

    assert patch_engine._validate_python_syntax(valid_code) is True
    assert patch_engine._validate_python_syntax(invalid_code) is False


def test_patch_with_no_pattern(patch_engine):
    """Test patch with empty pattern"""
    code = "def foo(): pass"

    patch = {
        'line_pattern': '',
        'replacement': 'something'
    }

    result = patch_engine.apply_patch(code, patch)

    assert result['applied'] is False
    assert 'No line pattern' in result['message']


def test_patch_stats(patch_engine):
    """Test getting patch statistics"""
    code = "def foo():\n    pass\n\ndef bar():\n    pass"

    patches = [
        {'line_pattern': r'def foo\(\):', 'replacement': 'def foo():  # patched'},
        {'line_pattern': r'def bar\(\):', 'replacement': 'def bar():  # patched'},
        {'line_pattern': r'def baz\(\):', 'replacement': 'def baz():  # not found'},
    ]

    patch_engine.apply_patches(code, patches)
    stats = patch_engine.get_stats()

    assert stats['total_applied'] == 2
    assert stats['total_failed'] == 1
    assert stats['success_rate'] == 2/3


def test_reset_patch_engine(patch_engine):
    """Test resetting patch engine state"""
    code = "def foo():\n    pass"
    patch = {'line_pattern': r'def foo\(\):', 'replacement': 'def foo():  # x'}

    patch_engine.apply_patches(code, [patch])
    assert len(patch_engine.applied_patches) == 1

    patch_engine.reset()
    assert len(patch_engine.applied_patches) == 0
    assert len(patch_engine.failed_patches) == 0


def test_regex_patch_with_multiline(patch_engine):
    """Test regex patch with multiline matching"""
    code = """def foo():
    x = 1
    y = 2
    return x + y
"""

    patch = {
        'line_pattern': r'x = 1\n    y = 2',
        'replacement': 'result = 3  # Optimized'
    }

    result = patch_engine.apply_patch(code, patch)

    assert result['applied'] is True
    assert 'Optimized' in result['code']


def test_patch_with_regex_groups(patch_engine):
    """Test patch using regex capture groups"""
    code = "def foo(a, b):\n    pass"

    patch = {
        'line_pattern': r'def (foo)\((.*)\):',
        'replacement': r'def \1(\2) -> int:'  # Add return type
    }

    result = patch_engine.apply_patch(code, patch)

    assert result['applied'] is True
    assert '-> int:' in result['code']


def test_smart_patcher_with_conflict_detection(smart_patcher):
    """Test smart patcher detects conflicts"""
    patches = [
        {'line_pattern': r'def foo\(\):', 'replacement': 'def foo():  # a'},
        {'line_pattern': r'def foo\(\):', 'replacement': 'def foo():  # b'},
    ]

    conflicts = smart_patcher.detect_conflicts("def foo(): pass", patches)

    assert len(conflicts) > 0
    assert conflicts[0]['type'] == 'overlapping_patterns'


def test_smart_patcher_applies_by_priority(smart_patcher):
    """Test smart patcher applies patches in severity order"""
    code = "def foo():\n    pass\n\ndef bar():\n    pass"

    patches = [
        {
            'line_pattern': r'def bar\(\):',
            'replacement': 'def bar():  # low',
            'severity': 'low'
        },
        {
            'line_pattern': r'def foo\(\):',
            'replacement': 'def foo():  # critical',
            'severity': 'critical'
        }
    ]

    patched_code, report = smart_patcher.apply_patches_with_conflict_detection(
        code, patches
    )

    # Critical should be applied first
    assert report[0]['status'] == 'applied'
    assert 'critical' in patched_code


def test_apply_patches_empty_list(patch_engine):
    """Test applying empty patch list"""
    code = "def foo(): pass"
    patched_code, report = patch_engine.apply_patches(code, [])

    assert patched_code == code
    assert report == []


def test_apply_patch_with_exception(patch_engine):
    """Test handling of exception during patch application"""
    code = "def foo():\n    pass"

    # Invalid regex pattern will cause exception
    patch = {
        'line_pattern': r'[invalid(regex',  # Invalid regex
        'replacement': 'something'
    }

    result = patch_engine.apply_patch(code, patch)

    assert result['applied'] is False
    # Error message should indicate invalid pattern
    assert result['message'] != ''


def test_patch_preserves_indentation(patch_engine):
    """Test that patches preserve code indentation"""
    code = """class MyClass:
    def method(self):
        return 42
"""

    patch = {
        'line_pattern': r'return 42',
        'replacement': 'return self.calculate()  # Refactored'
    }

    result = patch_engine.apply_patch(code, patch)

    assert result['applied'] is True
    # Check that indentation is preserved
    assert '        return self.calculate()' in result['code']


def test_multiple_patches_sequential_application(patch_engine):
    """Test that patches are applied sequentially"""
    code = "x = 1"

    patches = [
        {'line_pattern': r'x = 1', 'replacement': 'x = 2'},
        {'line_pattern': r'x = 2', 'replacement': 'x = 3'},
    ]

    patched_code, report = patch_engine.apply_patches(code, patches)

    # Both should apply because they're applied sequentially
    assert 'x = 3' in patched_code
    assert report[0]['status'] == 'applied'
    assert report[1]['status'] == 'applied'


def test_patch_report_contains_details(patch_engine):
    """Test that patch report contains detailed information"""
    code = "def foo():\n    pass"

    patch = {
        'id': 123,
        'line_pattern': r'def foo\(\):',
        'replacement': 'def foo():  # improved',
        'reason': 'Add comment for clarity'
    }

    _, report = patch_engine.apply_patches(code, [patch])

    assert len(report) == 1
    assert report[0]['patch_id'] == 123
    assert report[0]['reason'] == 'Add comment for clarity'
    assert report[0]['status'] == 'applied'
    assert 'message' in report[0]
