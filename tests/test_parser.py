"""
Tests for the UniversalParser module.
"""
import pytest

from ultrathink.parser import UniversalParser


@pytest.fixture
def parser():
    """Create a UniversalParser instance for testing"""
    return UniversalParser()


def test_parser_initialization(parser):
    """Test parser initializes correctly"""
    assert parser is not None
    assert hasattr(parser, 'parse')


def test_parse_simple_function(parser):
    """Test parsing a simple function"""
    code = """
def hello_world():
    print("Hello, World!")
"""
    result = parser.parse(code, language="python")

    assert result['language'] == 'python'
    assert len(result['functions']) == 1
    assert result['functions'][0]['name'] == 'hello_world'
    assert result['functions'][0]['args'] == []


def test_parse_function_with_arguments(parser):
    """Test parsing function with arguments"""
    code = """
def add(a, b, c=0):
    return a + b + c
"""
    result = parser.parse(code, language="python")

    assert len(result['functions']) == 1
    func = result['functions'][0]
    assert func['name'] == 'add'
    assert func['args'] == ['a', 'b', 'c']
    assert func['line_number'] == 2


def test_parse_function_with_docstring(parser):
    """Test parsing function with docstring"""
    code = '''
def greet(name):
    """Greet someone by name"""
    return f"Hello, {name}"
'''
    result = parser.parse(code, language="python")

    func = result['functions'][0]
    assert func['has_docstring'] is True


def test_parse_function_without_docstring(parser):
    """Test parsing function without docstring"""
    code = """
def greet(name):
    return f"Hello, {name}"
"""
    result = parser.parse(code, language="python")

    func = result['functions'][0]
    assert func['has_docstring'] is False


def test_parse_function_with_type_annotations(parser):
    """Test parsing function with return annotation"""
    code = """
def add(a: int, b: int) -> int:
    return a + b
"""
    result = parser.parse(code, language="python")

    func = result['functions'][0]
    assert func['has_return_annotation'] is True


def test_parse_function_with_decorator(parser):
    """Test parsing function with decorator"""
    code = """
@staticmethod
@property
def my_func():
    pass
"""
    result = parser.parse(code, language="python")

    func = result['functions'][0]
    assert len(func['decorators']) == 2
    assert 'staticmethod' in func['decorators']
    assert 'property' in func['decorators']


def test_parse_simple_class(parser):
    """Test parsing a simple class"""
    code = """
class MyClass:
    def method1(self):
        pass

    def method2(self):
        pass
"""
    result = parser.parse(code, language="python")

    assert len(result['classes']) == 1
    cls = result['classes'][0]
    assert cls['name'] == 'MyClass'
    assert len(cls['methods']) == 2
    assert 'method1' in cls['methods']
    assert 'method2' in cls['methods']


def test_parse_class_with_inheritance(parser):
    """Test parsing class with base classes"""
    code = """
class Child(Parent, Mixin):
    pass
"""
    result = parser.parse(code, language="python")

    cls = result['classes'][0]
    assert cls['name'] == 'Child'
    assert 'Parent' in cls['bases']
    assert 'Mixin' in cls['bases']


def test_parse_class_with_docstring(parser):
    """Test parsing class with docstring"""
    code = '''
class MyClass:
    """This is my class"""
    pass
'''
    result = parser.parse(code, language="python")

    cls = result['classes'][0]
    assert cls['has_docstring'] is True


def test_parse_imports(parser):
    """Test parsing import statements"""
    code = """
import os
import sys
from pathlib import Path
from typing import Dict, List
"""
    result = parser.parse(code, language="python")

    # Note: 'from typing import Dict, List' creates 2 separate import entries
    assert len(result['imports']) == 5
    imports = [imp['module'] for imp in result['imports']]
    assert 'os' in imports
    assert 'sys' in imports
    assert 'pathlib' in imports
    assert 'typing' in imports


def test_parse_metrics(parser):
    """Test code metrics calculation"""
    code = """
def simple():
    return 42

def complex(x):
    if x > 0:
        if x > 10:
            return "large"
        return "small"
    return "negative"
"""
    result = parser.parse(code, language="python")

    metrics = result['metrics']
    assert 'complexity' in metrics
    assert 'function_count' in metrics
    assert 'class_count' in metrics
    assert metrics['function_count'] == 2
    assert metrics['class_count'] == 0


def test_parse_calculator_sample(parser):
    """Test parsing the sample calculator file"""
    code = """
import os

class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, a, b, c=None):
        if c is not None:
            return a + b + c
        else:
            return a + b

    def divide(self, a, b):
        return a / b

    def evaluate_expression(self, expr):
        return eval(expr)
"""
    result = parser.parse(code, language="python")

    # Should find Calculator class
    assert len(result['classes']) == 1
    assert result['classes'][0]['name'] == 'Calculator'

    # Should find methods
    methods = result['classes'][0]['methods']
    assert '__init__' in methods
    assert 'add' in methods
    assert 'divide' in methods
    assert 'evaluate_expression' in methods

    # Should find import
    assert len(result['imports']) == 1
    assert result['imports'][0]['module'] == 'os'

    # Should have metrics
    assert result['metrics']['class_count'] == 1
    assert result['metrics']['complexity'] > 0


def test_parse_empty_code(parser):
    """Test parsing empty code"""
    result = parser.parse("", language="python")

    assert result['language'] == 'python'
    assert result['functions'] == []
    assert result['classes'] == []
    assert result['imports'] == []


def test_parse_syntax_error(parser):
    """Test parsing code with syntax errors"""
    code = """
def broken(
    # Missing closing parenthesis and body
"""
    result = parser.parse(code, language="python")

    # Should return error information
    assert 'error' in result
    assert 'Syntax error' in result['error']


def test_parse_unsupported_language(parser):
    """Test parsing with unsupported language"""
    code = "fn main() {}"
    result = parser.parse(code, language="rust")

    # Should indicate unsupported language
    assert 'error' in result or result['language'] == 'rust'


def test_cyclomatic_complexity_simple(parser):
    """Test complexity calculation for simple function"""
    code = """
def simple():
    return 42
"""
    result = parser.parse(code, language="python")

    # Simple function with no branches has 0 decision points
    assert result['metrics']['complexity'] == 0


def test_cyclomatic_complexity_branches(parser):
    """Test complexity calculation with branches"""
    code = """
def complex(x, y):
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"

    while y > 0:
        y -= 1
"""
    result = parser.parse(code, language="python")

    # Function with branches should have higher complexity
    assert result['metrics']['complexity'] > 1
