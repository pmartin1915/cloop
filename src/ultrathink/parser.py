"""
Universal parser for multiple programming languages.

This module provides parsing capabilities for different code files and
extracts structural information using AST parsing.
"""
import ast
import logging
from typing import Any, Dict

from tree_sitter import Parser

logger = logging.getLogger(__name__)


class UniversalParser:
    """Parse code in multiple languages"""

    def __init__(self):
        """Initialize language parsers"""
        self.parsers = {}
        self._initialize_parsers()

    def _initialize_parsers(self):
        """Initialize language parsers"""
        # For now, we use Python's built-in ast module for Python
        # tree-sitter can be added later for other languages
        languages = {
            'python': 'tree-sitter-python',
            'javascript': 'tree-sitter-javascript',
            'typescript': 'tree-sitter-typescript',
            'rust': 'tree-sitter-rust',
            'go': 'tree-sitter-go'
        }

        for lang, lib_name in languages.items():
            parser = Parser()
            # Note: tree-sitter language libraries need to be built separately
            # For now, we'll use Python's ast for Python code
            self.parsers[lang] = parser

    def parse(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Parse code and return structured analysis.

        Args:
            code: Source code string
            language: Programming language (default: python)

        Returns:
            Dictionary with parsed information
        """
        if language == "python":
            return self._parse_python(code)
        elif language in self.parsers:
            # Placeholder for other languages via tree-sitter
            return {
                "language": language,
                "ast": "AST parsing not yet implemented for this language",
                "metrics": self._calculate_metrics(code, language),
                "functions": [],
                "classes": [],
                "imports": []
            }
        else:
            raise ValueError(f"Unsupported language: {language}")

    def _parse_python(self, code: str) -> Dict[str, Any]:
        """
        Parse Python code using built-in ast module.

        Args:
            code: Python source code

        Returns:
            Structured information about the code
        """
        try:
            tree = ast.parse(code)

            # Extract functions
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line_number": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "has_docstring": ast.get_docstring(node) is not None,
                        "has_return_annotation": node.returns is not None,
                        "decorators": [self._get_decorator_name(d) for d in node.decorator_list]
                    })

            # Extract classes
            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = [
                        n.name for n in node.body
                        if isinstance(n, ast.FunctionDef)
                    ]
                    classes.append({
                        "name": node.name,
                        "line_number": node.lineno,
                        "methods": methods,
                        "bases": [self._get_base_name(base) for base in node.bases],
                        "has_docstring": ast.get_docstring(node) is not None
                    })

            # Extract imports
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({
                            "type": "import",
                            "module": alias.name,
                            "alias": alias.asname,
                            "line_number": node.lineno
                        })
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imports.append({
                            "type": "from_import",
                            "module": node.module,
                            "name": alias.name,
                            "alias": alias.asname,
                            "line_number": node.lineno
                        })

            # Calculate complexity
            complexity = self._calculate_complexity(tree)

            return {
                "language": "python",
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "metrics": {
                    **self._calculate_metrics(code, "python"),
                    "complexity": complexity,
                    "function_count": len(functions),
                    "class_count": len(classes),
                    "import_count": len(imports)
                }
            }

        except SyntaxError as e:
            logger.error(f"Syntax error parsing Python code: {e}")
            return {
                "language": "python",
                "error": f"Syntax error: {str(e)}",
                "functions": [],
                "classes": [],
                "imports": [],
                "metrics": self._calculate_metrics(code, "python")
            }
        except Exception as e:
            logger.error(f"Error parsing Python code: {e}")
            return {
                "language": "python",
                "error": str(e),
                "functions": [],
                "classes": [],
                "imports": [],
                "metrics": self._calculate_metrics(code, "python")
            }

    def _get_decorator_name(self, decorator) -> str:
        """Extract decorator name from AST node"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{decorator.value.id if isinstance(decorator.value, ast.Name) else '?'}.{decorator.attr}"
        return "unknown"

    def _get_base_name(self, base) -> str:
        """Extract base class name from AST node"""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{base.value.id if isinstance(base.value, ast.Name) else '?'}.{base.attr}"
        return "unknown"

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, (ast.And, ast.Or)):
                complexity += 1
        return complexity

    def _calculate_metrics(self, code: str, language: str) -> Dict[str, Any]:
        """Calculate basic code metrics"""
        lines = code.split('\n')
        return {
            "lines_of_code": len(lines),
            "blank_lines": sum(1 for line in lines if not line.strip()),
            "comment_lines": sum(1 for line in lines if line.strip().startswith(('#', '//', '/*'))),
            "code_lines": len([line for line in lines if line.strip() and not line.strip().startswith(('#', '//', '/*'))])
        }
