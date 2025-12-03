# Design Document - Phase 3: Property-Based Testing

## Overview

This design document outlines the implementation of property-based testing for CodeArchaeologist using the Hypothesis library. Property-based testing will validate that core system behaviors hold true across a wide range of inputs, providing stronger correctness guarantees than traditional example-based unit tests.

The implementation will focus on testing the critical components already built in Phases 1 and 2:
- Repository ingestion and URL validation
- File scanning across diverse directory structures
- Dependency extraction from multiple file formats
- Analysis completeness and consistency
- Data persistence round-trips

## Architecture

### Testing Framework: Hypothesis

We will use Hypothesis 6.92.0+ as our property-based testing framework. Hypothesis provides:
- Automatic test case generation
- Intelligent shrinking to minimal failing examples
- Stateful testing capabilities
- Integration with pytest

### Test Organization

```
backend/tests/
├── generators.py              # Test data generators
├── test_properties_ingestion.py   # Repository ingestion properties
├── test_properties_scanning.py    # File scanning properties
├── test_properties_extraction.py  # Dependency extraction properties
├── test_properties_analysis.py    # Analysis completeness properties
└── test_properties_persistence.py # Data persistence properties
```

### Integration with Existing Tests

Property-based tests will complement existing unit tests:
- **Unit tests**: Verify specific examples and edge cases
- **Property tests**: Verify universal properties across all inputs
- Both run together in the pytest suite

## Components and Interfaces

### 1. Test Data Generators (`generators.py`)

**Purpose:** Generate realistic test data for property tests

**Key Generators:**

```python
@composite
def generate_git_url(draw) -> str:
    """Generate valid Git repository URLs"""
    
@composite
def generate_invalid_url(draw) -> str:
    """Generate invalid URLs for rejection testing"""
    
@composite
def generate_python_code(draw) -> str:
    """Generate syntactically valid Python code"""
    
@composite
def generate_dependency_spec(draw, format: str) -> str:
    """Generate dependency specifications (pip, npm, poetry)"""
    
@composite
def generate_file_tree(draw) -> Dict[str, Any]:
    """Generate directory structures with files"""
    
@composite
def generate_repository_metadata(draw) -> Dict[str, Any]:
    """Generate repository metadata"""
    
@composite
def generate_analysis_result(draw) -> Dict[str, Any]:
    """Generate complete analysis results"""
```

**Constraints:**
- Git URLs must follow valid patterns (https, git, ssh)
- Python code must be parseable (use ast.parse for validation)
- Dependency specs must match format requirements
- File trees must have valid paths (no invalid characters)

### 2. Repository Ingestion Property Tests

**File:** `test_properties_ingestion.py`

**Properties to Test:**
- Invalid URL rejection
- Valid URL acceptance
- Metadata extraction completeness
- Error handling consistency

**Test Fixtures:**
- Mock Git operations for speed
- Temporary directories for cloning
- Database session for persistence tests

### 3. File Scanning Property Tests

**File:** `test_properties_scanning.py`

**Properties to Test:**
- File identification completeness
- Ignored directory exclusion
- Statistics consistency
- Language categorization accuracy

**Test Approach:**
- Generate diverse directory structures
- Create temporary file systems
- Verify scanner behavior across all structures

### 4. Dependency Extraction Property Tests

**File:** `test_properties_extraction.py`

**Properties to Test:**
- Parsing correctness for all formats
- Version constraint preservation
- Dev vs production classification
- Error handling for malformed files

**Test Approach:**
- Generate valid dependency files
- Generate malformed files for error testing
- Verify extraction accuracy

### 5. Analysis Completeness Property Tests

**File:** `test_properties_analysis.py`

**Properties to Test:**
- Language percentage summation
- File count consistency
- Issue file path validity
- Technical debt grade consistency

**Test Approach:**
- Generate complete analysis results
- Verify internal consistency
- Check mathematical invariants

### 6. Data Persistence Property Tests

**File:** `test_properties_persistence.py`

**Properties to Test:**
- Round-trip data preservation
- JSON serialization correctness
- Timestamp preservation
- Field completeness

**Test Approach:**
- Generate random data
- Store in database
- Retrieve and compare
- Verify no data loss

## Data Models

### Generator Output Types

```python
# Git URL formats
GitUrl = str  # "https://github.com/user/repo.git"

# File tree structure
FileTree = Dict[str, Union[str, Dict]]
# Example: {"src": {"main.py": "content", "utils.py": "content"}}

# Dependency specification
DependencySpec = Dict[str, str]
# Example: {"name": "flask", "version": ">=2.0.0", "type": "production"}

# Analysis result structure (matches AnalysisResult model)
AnalysisData = Dict[str, Any]
```

### Test Configuration

```python
# pytest.ini additions
[tool.pytest.ini_options]
hypothesis_max_examples = 100
hypothesis_deadline = 5000  # 5 seconds per test
hypothesis_verbosity = "normal"
hypothesis_show_statistics = true
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Invalid URL Rejection

*For any* invalid URL format, the repository ingester should reject it with an appropriate error message and not attempt to clone.

**Validates: Requirements 2.1**

### Property 2: Valid URL Acceptance

*For any* valid Git URL (https, git, or ssh format), the repository ingester should successfully validate it without errors.

**Validates: Requirements 2.2**

### Property 3: Metadata Extraction Completeness

*For any* successfully cloned repository, the extracted metadata should include all required fields: default branch, last commit hash, last commit date, and repository size.

**Validates: Requirements 2.3**

### Property 4: Network Error Handling

*For any* repository URL that triggers a network error (timeout, connection refused, DNS failure), the system should handle it gracefully by returning an error without crashing.

**Validates: Requirements 2.4**

### Property 5: File Identification Completeness

*For any* directory structure, the file scanner should identify all files with supported extensions (.py, .js, .ts, .jsx, .tsx) and no files should be missed if they have these extensions.

**Validates: Requirements 3.1**

### Property 6: Ignored Directory Exclusion

*For any* directory structure containing ignored directories (node_modules, __pycache__, .git, .venv, dist, build), the scanner should skip these directories and none of their contents should appear in the results.

**Validates: Requirements 3.2**

### Property 7: File Statistics Consistency

*For any* scanned repository, the sum of file counts by language should equal the total files count, and the sum of file counts by extension should also equal the total files count.

**Validates: Requirements 3.3**

### Property 8: Language Categorization Accuracy

*For any* file path with a known extension, the file scanner should categorize it to the correct language (.py → python, .js → javascript, .ts → typescript).

**Validates: Requirements 3.4**

### Property 9: Requirements.txt Parsing Completeness

*For any* valid requirements.txt content, the dependency extractor should extract all listed dependencies with their version constraints preserved accurately.

**Validates: Requirements 4.1**

### Property 10: Package.json Dependency Classification

*For any* valid package.json content, the dependency extractor should correctly distinguish between production dependencies and devDependencies, with no misclassification.

**Validates: Requirements 4.2**

### Property 11: Pyproject.toml Parsing Accuracy

*For any* valid pyproject.toml content, the dependency extractor should extract all dependencies from the [tool.poetry.dependencies] section with version constraints preserved.

**Validates: Requirements 4.3**

### Property 12: Malformed File Error Handling

*For any* malformed dependency file (invalid JSON, invalid TOML, corrupted content), the dependency extractor should handle the error gracefully and return an empty dependency list or error indicator without crashing.

**Validates: Requirements 4.4**

### Property 13: Language Percentage Summation

*For any* analysis result with detected languages, the sum of all language percentages should equal 100% (or 0% if no files were analyzed).

**Validates: Requirements 5.1**

### Property 14: Analysis File Count Consistency

*For any* analysis result, the total_files field should equal the sum of file_count across all detected languages.

**Validates: Requirements 5.2**

### Property 15: Issue File Path Validity

*For any* issue detected in the analysis, the file path should be a valid relative path that could exist in a repository (no null bytes, no absolute paths, no path traversal).

**Validates: Requirements 5.3**

### Property 16: Technical Debt Grade Consistency

*For any* analysis result with a maintainability score, the assigned grade should match the score according to the grading scale (A: 80-100, B: 60-79, C: 40-59, D: 20-39, F: 0-19).

**Validates: Requirements 5.4**

### Property 17: Data Persistence Round-Trip

*For any* analysis result, storing it in the database and then retrieving it should return data that is equivalent to the original (all fields preserved, JSON structures intact).

**Validates: Requirements 6.1, 6.2, 6.3**

### Property 18: Timestamp Preservation

*For any* timestamp stored in the database, retrieving it should return the same moment in time with correct timezone information (UTC).

**Validates: Requirements 6.4**

### Property 19: Generator URL Validity

*For any* URL generated by the test data generator, it should pass the repository ingester's URL validation function.

**Validates: Requirements 7.1**

### Property 20: Generator Python Syntax Validity

*For any* Python code generated by the test data generator, it should be parseable by Python's ast.parse() without syntax errors.

**Validates: Requirements 7.2**

### Property 21: Generator Dependency Format Validity

*For any* dependency specification generated by the test data generator, it should match the expected format for its type (pip, npm, or poetry).

**Validates: Requirements 7.3**

### Property 22: Generator Directory Tree Validity

*For any* directory structure generated by the test data generator, all paths should be valid (no invalid characters, no path traversal, proper nesting).

**Validates: Requirements 7.4**

## Error Handling

### Property Test Failures

When a property test fails, Hypothesis will:
1. Report the failing example
2. Shrink it to the minimal failing case
3. Save it for regression testing

**Handling Strategy:**
- Investigate the minimal failing example
- Determine if it's a bug in the system or the test
- Fix the bug or adjust the generator constraints
- Re-run to verify the fix

### Test Timeouts

Some properties may take longer to test (e.g., actual repository cloning):
- Use mocking for slow operations
- Set appropriate deadlines in pytest.ini
- Use `@settings(deadline=None)` for integration-style properties

### Database State Management

For persistence properties:
- Use pytest fixtures with database rollback
- Create isolated test databases
- Clean up after each test run

## Testing Strategy

### Unit Tests vs Property Tests

**Unit Tests (Existing):**
- Test specific examples
- Test known edge cases
- Test error messages
- Fast execution

**Property Tests (New):**
- Test universal behaviors
- Generate diverse inputs
- Find unknown edge cases
- Slower but more thorough

### Test Execution

```bash
# Run all tests including properties
pytest

# Run only property tests
pytest -m property

# Run with verbose Hypothesis output
pytest --hypothesis-show-statistics

# Run with specific seed for reproducibility
pytest --hypothesis-seed=12345
```

### Coverage Goals

- Property tests should cover all critical paths
- Aim for 100 examples per property (configurable)
- Each property should complete in < 5 seconds
- Total property test suite should run in < 2 minutes

### Continuous Integration

Property tests will run in CI:
- On every pull request
- On main branch commits
- Nightly with increased example counts (1000 examples)

## Implementation Notes

### Mocking Strategy

For expensive operations:
- Mock Git operations (use temporary directories instead)
- Mock network calls (use responses library)
- Mock AI calls (not needed for property tests)

### Test Data Realism

Generators should produce realistic data:
- Use actual Git URL patterns from real repositories
- Generate Python code that resembles real code
- Create directory structures similar to real projects
- Use realistic dependency versions

### Performance Considerations

- Keep property tests fast (< 5s each)
- Use smaller example counts during development
- Increase counts in CI for thorough testing
- Profile slow properties and optimize

### Debugging Failed Properties

When a property fails:
1. Hypothesis shows the minimal failing example
2. Add that example as a unit test
3. Debug with the specific example
4. Fix the bug
5. Verify the property passes
6. Keep the unit test as regression protection
