# Test file for Ultrathink extension
# This file has intentional issues for testing

def calculate_total(items):
    # Missing type hints
    total = 0
    for item in items:
        total = total + item  # Could use +=
    return total

def divide(a, b):
    # No error handling for division by zero
    return a / b

class UserManager:
    def __init__(self):
        self.users = []
    
    def add_user(self, name, email):
        # No validation
        user = {"name": name, "email": email}
        self.users.append(user)
        return user
    
    def get_user(self, name):
        # Inefficient search
        for user in self.users:
            if user["name"] == name:
                return user
        return None

# Unused import (if we had one)
# Missing docstrings
# No error handling
