# Self-Improvement Loop

Ultrathink's self-improvement loop enables the framework to learn from code analysis and automatically apply improvements to future projects.

## Overview

The self-improvement cycle consists of four phases:

1. **Analyze**: Examine code and identify issues
2. **Learn**: Detect patterns in recurring issues
3. **Improve**: Generate code patches from patterns
4. **Apply**: Automatically apply learned improvements to new projects

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Self-Improvement Loop                     │
└─────────────────────────────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
   ┌──────────┐        ┌──────────┐       ┌──────────┐
   │ Analyze  │───────▶│  Learn   │──────▶│  Apply   │
   │ Codebase │        │ Patterns │       │ Patches  │
   └──────────┘        └──────────┘       └──────────┘
         │                   │                   │
         │                   │                   │
         ▼                   ▼                   ▼
   ┌─────────────────────────────────────────────────┐
   │            Knowledge Base (SQLite)              │
   ├─────────────┬───────────────┬──────────────────┤
   │  Findings   │   Patterns    │   Improvements   │
   └─────────────┴───────────────┴──────────────────┘
```

## Components

### 1. Knowledge Base (`knowledge_base.py`)

Persistent SQLite storage for analysis findings, identified patterns, and improvements.

**Schema:**
- `findings`: Stores individual code issues (line number, severity, category, description)
- `patterns`: Groups recurring issues by category and similarity
- `improvements`: Code patches generated from patterns

**Key Methods:**
```python
# Store analysis results
knowledge_base.store_analysis_findings(file_path, findings)

# Retrieve recurring issues
recurring = knowledge_base.get_recurring_issues(threshold=2)

# Store learned improvement
knowledge_base.store_improvement(patch)

# Get statistics
stats = knowledge_base.get_stats()
```

### 2. Learning Engine (`learning_engine.py`)

Identifies patterns in recurring issues and generates code patches.

**Pattern Detection:**
- Groups findings by category (bug, security, quality, style, performance)
- Uses fuzzy string matching (difflib) to cluster similar descriptions
- Configurable similarity threshold (default: 0.8)
- Configurable occurrence threshold (default: 2)

**Patch Generation:**
Category-specific patch generators:
- **Bug**: Division by zero checks, null pointer guards, boundary checks
- **Security**: Replace eval() with ast.literal_eval, SQL injection protection
- **Quality**: Add type hints, docstrings, logging
- **Style**: Format strings, naming conventions
- **Performance**: List comprehensions, caching, algorithm optimization

**Key Methods:**
```python
# Learn from stored findings
learning_engine = LearningEngine(knowledge_base, similarity_threshold=0.8)
result = learning_engine.learn_from_findings(occurrence_threshold=2)

# Get learning statistics
stats = learning_engine.get_learning_stats()
# Returns: total_findings, total_patterns, total_patches, learning_rate
```

### 3. Patch Engine (`patch_engine.py`)

Applies code patches with validation.

**Features:**
- Regex-based pattern matching and replacement
- Multiline pattern support
- Syntax validation after each patch (AST parsing)
- Conflict detection between overlapping patches
- Detailed application reporting

**Key Methods:**
```python
patch_engine = PatchEngine()

# Apply single patch
result = patch_engine.apply_patch(code, patch, language="python")

# Apply multiple patches
patched_code, report = patch_engine.apply_patches(code, patches, language="python")

# Get statistics
stats = patch_engine.get_stats()
```

### 4. Python Scaffolder (`scaffolding/python_scaffolder.py`)

Generates new projects with learned improvements applied.

**Integration:**
```python
scaffolder = PythonScaffolder(knowledge_base=knowledge_base)
project_path = scaffolder.scaffold(
    project_name="my_project",
    output_dir="./output",
    author_name="John Doe",
    author_email="john@example.com"
)

# Check which improvements were applied
applied = scaffolder.get_applied_improvements()
```

## Usage Examples

### End-to-End Workflow

```bash
# Step 1: Analyze flawed codebase
ultrathink analyze /path/to/flawed_code --save-findings

# Step 2: Learn patterns from findings
ultrathink learn --threshold 2

# Step 3: Generate new project (improvements applied automatically)
ultrathink scaffold my_improved_project \
    --author-name "John Doe" \
    --author-email "john@example.com" \
    --output-dir ./output

# View statistics
ultrathink stats
```

### Programmatic Usage

```python
from ultrathink import Ultrathink
from ultrathink.learning_engine import LearningEngine

# Initialize framework
ultrathink = Ultrathink()

# Analyze codebase
result = await ultrathink.analyze_codebase(
    "/path/to/code",
    save_findings=True
)

# Learn from findings
learning_engine = LearningEngine(
    ultrathink.knowledge_base,
    similarity_threshold=0.8
)
learning_result = learning_engine.learn_from_findings(
    occurrence_threshold=2
)

print(f"Patterns identified: {learning_result['patterns_identified']}")
print(f"Patches generated: {learning_result['patches_generated']}")

# Future scaffolding will automatically apply these improvements
```

### Configuration

Control learning behavior in `ultrathink.yaml`:

```yaml
learning:
  learning_rate: 0.1
  pattern_similarity_threshold: 0.7
  knowledge_base_path: "ultrathink.db"

quality_thresholds:
  complexity: 0.7
  readability: 0.8
  performance: 0.7
  security: 0.9
  test_coverage: 0.8
```

## Metrics and Statistics

### Learning Statistics

```python
stats = learning_engine.get_learning_stats()
```

Returns:
- `total_findings`: Number of issues found
- `total_patterns`: Number of patterns identified
- `total_patches`: Number of patches generated
- `learning_rate`: (patterns + patches) / findings (0-1)
- `findings_by_severity`: Breakdown by severity level
- `top_issues`: Most common issue types

### Knowledge Base Statistics

```python
stats = knowledge_base.get_stats()
```

Returns:
- `total_findings`: All stored findings
- `total_patterns`: Identified patterns
- `total_improvements`: Stored patches
- `findings_by_category`: Breakdown by category
- `most_improved_files`: Files with most applied patches

### Patch Application Statistics

```python
stats = patch_engine.get_stats()
```

Returns:
- `total_applied`: Successfully applied patches
- `total_failed`: Failed patch attempts
- `success_rate`: Applied / (Applied + Failed)
- `applied_by_category`: Breakdown by issue category

## Testing

Comprehensive test coverage across all loop components:

```bash
# Run all integration tests
poetry run pytest tests/test_self_improvement_loop.py -v

# Run specific test
poetry run pytest tests/test_self_improvement_loop.py::test_complete_self_improvement_cycle -v
```

**Integration Tests:**
1. `test_complete_self_improvement_cycle`: Full analyze → learn → improve cycle
2. `test_scaffolding_applies_learned_improvements`: Verify patches applied during scaffolding
3. `test_pattern_frequency_threshold`: Pattern detection only above threshold
4. `test_learning_from_multiple_categories`: Cross-category learning
5. `test_improvement_usage_tracking`: Track patch application counts
6. `test_learning_statistics`: Verify metrics calculation
7. `test_before_after_comparison`: Compare quality before/after learning
8. `test_empty_analysis_no_learning`: Handle empty state gracefully

## Demonstration

The `flawed_demo/` directory contains intentionally flawed code to demonstrate the loop:

**calculator_v1.py** - Common code issues:
- Division by zero bug
- Security: eval() usage
- Missing type hints
- Missing docstrings
- Unused variables

**Expected Learning:**
After analyzing flawed_demo, Ultrathink should learn patterns like:
- "Division by zero not handled" → Add zero check
- "Unsafe eval usage" → Use ast.literal_eval
- "Missing type hints" → Add type annotations

These improvements are then automatically applied to future projects.

## Future Enhancements

1. **Multi-language Support**: Extend beyond Python to JavaScript, TypeScript, Rust, Go
2. **AI-Enhanced Patch Generation**: Use LLMs to generate more sophisticated patches
3. **Confidence Scoring**: Rank patches by likelihood of success
4. **A/B Testing**: Compare code quality before/after patches
5. **Collaborative Learning**: Share knowledge bases across teams
6. **Real-time Learning**: Update knowledge base during development
7. **Automated Refactoring**: Suggest large-scale refactorings based on patterns

## References

- **SQLite Schema**: [src/ultrathink/knowledge_base.py](../src/ultrathink/knowledge_base.py)
- **Learning Algorithm**: [src/ultrathink/learning_engine.py](../src/ultrathink/learning_engine.py)
- **Patch Application**: [src/ultrathink/patch_engine.py](../src/ultrathink/patch_engine.py)
- **Integration Tests**: [tests/test_self_improvement_loop.py](../tests/test_self_improvement_loop.py)
- **Configuration**: [ultrathink.yaml](../ultrathink.yaml)
