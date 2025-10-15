"""Example file with intentional issues for handoff demo."""

def calculate(a, b, operation):
    """Calculate result without type hints or validation."""
    if operation == "add":
        return a + b
    elif operation == "divide":
        return a / b  # No zero check!
    elif operation == "eval":
        return eval(f"{a} {operation} {b}")  # Security issue!
    
def process_data(data):
    # Missing docstring
    result = []
    for item in data:
        result.append(item * 2)
    return result

class Calculator:
    def __init__(self, name):
        self.name = name
        self.unused_var = "never used"  # Unused variable
    
    def divide(self, x, y):
        return x / y  # No error handling
