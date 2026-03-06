# Code Review - Fix Request

## Context
I analyzed `c:\Cloop\flawed_demo\calculator_v1.py` and found **8 issues** that need fixing.

## Best Practices to Follow
- **Type Safety**: Add type hints to all functions
- **Error Handling**: Use specific exceptions, validate inputs
- **Security**: Avoid eval(), use parameterized queries
- **Code Quality**: Add docstrings, remove unused code
- **Performance**: Optimize loops, avoid redundant operations

## Issues Found (8 total)

**Priority**: 1 critical, 2 high-severity issues

### `calculator_v1.py`

[!] **Line 32** [CRITICAL] - security
- Issue: Use of eval() allows arbitrary code execution
- Fix: Replace eval() with ast.literal_eval() or a safe expression parser

[!!] **Line 26** [HIGH] - bug
- Issue: Division by zero not handled
- Fix: Add zero check before division operation

[!!] **Line 15** [HIGH] - quality
- Issue: Missing type hints on function parameters
- Fix: Add type annotations: def add(self, a: float, b: float) -> float

[*] **Line 18** [MEDIUM] - quality
- Issue: Missing type hints on function parameters
- Fix: Add type annotations: def subtract(self, a: float, b: float) -> float

[*] **Line 21** [MEDIUM] - quality
- Issue: Missing type hints on function parameters
- Fix: Add type annotations: def multiply(self, a: float, b: float) -> float

[*] **Line 28** [MEDIUM] - quality
- Issue: Missing type hints on function parameters
- Fix: Add type annotations: def power(self, a: float, b: float) -> float

[*] **Line 35** [MEDIUM] - quality
- Issue: Missing type hints on function parameters
- Fix: Add type annotations: def square_root(self, a: float) -> float

[-] **Line 35** [LOW] - quality
- Issue: No validation for negative numbers in square_root
- Fix: Add check for negative input and raise ValueError

## Your Task
Fix these issues following the best practices above. For each fix:
1. Show the corrected code
2. Explain what changed and why
3. Start with critical/high-severity issues

---

## Example Fixed Code

Here's how the critical security issue should be fixed:

```python
import ast

# BEFORE (INSECURE):
def evaluate_expression(self, expr):
    return eval(expr)  # Dangerous!

# AFTER (SECURE):
def evaluate_expression(self, expr: str) -> float:
    """Safely evaluate a mathematical expression.
    
    Args:
        expr: Mathematical expression as string
        
    Returns:
        Result of evaluation
        
    Raises:
        ValueError: If expression is invalid or unsafe
    """
    try:
        # Only allows literals, not arbitrary code
        return ast.literal_eval(expr)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid expression: {expr}") from e
```

And the division by zero bug:

```python
# BEFORE (BUGGY):
def divide(self, a, b):
    return a / b  # Crashes on b=0!

# AFTER (SAFE):
def divide(self, a: float, b: float) -> float:
    """Divide two numbers with zero check.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Result of division
        
    Raises:
        ValueError: If denominator is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```
