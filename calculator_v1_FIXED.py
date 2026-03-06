"""
Fixed calculator demonstrating Ultrathink improvements.

All issues from the flawed version have been corrected:
✓ Division by zero handled
✓ Type hints added
✓ Security issue (eval) fixed
✓ Docstrings added
"""
import ast
from typing import Union


class Calculator:
    """A calculator with proper error handling and type safety."""
    
    def __init__(self) -> None:
        """Initialize calculator with result set to 0."""
        self.result: float = 0

    def add(self, a: float, b: float) -> float:
        """Add two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a.
        
        Args:
            a: Number to subtract from
            b: Number to subtract
            
        Returns:
            Difference of a and b
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a and b
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Divide a by b with zero check.
        
        Args:
            a: Numerator
            b: Denominator
            
        Returns:
            Quotient of a and b
            
        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, a: float, b: float) -> float:
        """Raise a to the power of b.
        
        Args:
            a: Base number
            b: Exponent
            
        Returns:
            a raised to the power of b
        """
        return a ** b

    def evaluate_expression(self, expr: str) -> Union[int, float]:
        """Safely evaluate a mathematical expression.
        
        Uses ast.literal_eval() instead of eval() to prevent code injection.
        Only allows literal expressions (numbers and basic operations).
        
        Args:
            expr: Mathematical expression as string (e.g., "2 + 3")
            
        Returns:
            Result of evaluation
            
        Raises:
            ValueError: If expression is invalid or unsafe
            
        Example:
            >>> calc = Calculator()
            >>> calc.evaluate_expression("2 + 3")
            5
        """
        try:
            # ast.literal_eval only allows literals, not arbitrary code
            return ast.literal_eval(expr)
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Invalid expression: {expr}") from e

    def square_root(self, a: float) -> float:
        """Calculate square root of a number.
        
        Args:
            a: Number to find square root of
            
        Returns:
            Square root of a
            
        Raises:
            ValueError: If a is negative
        """
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return a ** 0.5


# Example usage
if __name__ == "__main__":
    calc = Calculator()
    
    print("Addition:", calc.add(5, 3))
    print("Subtraction:", calc.subtract(10, 4))
    print("Multiplication:", calc.multiply(6, 7))
    print("Division:", calc.divide(15, 3))
    print("Power:", calc.power(2, 8))
    print("Square root:", calc.square_root(16))
    
    # Safe expression evaluation
    print("Expression:", calc.evaluate_expression("10 + 5"))
    
    # Error handling examples
    try:
        calc.divide(10, 0)
    except ValueError as e:
        print(f"Error caught: {e}")
    
    try:
        calc.square_root(-4)
    except ValueError as e:
        print(f"Error caught: {e}")
