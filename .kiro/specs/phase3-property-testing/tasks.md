# Implementation Plan - Phase 3: Property-Based Testing

- [x] 1. Set up Hypothesis and test infrastructure
  - Install Hypothesis 6.92.0+ in requirements-dev.txt
  - Configure pytest.ini with Hypothesis settings (max_examples=100, deadline=5000ms)
  - Add property test marker to pytest configuration
  - Verify Hypothesis runs with a simple test
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 2. Create test data generators
  - [x] 2.1 Implement Git URL generators
    - Create `generate_git_url()` for valid URLs (https, git, ssh formats)
    - Create `generate_invalid_url()` for invalid URLs
    - Test that generated URLs match expected patterns
    - _Requirements: 7.1_

  - [x] 2.2 Implement Python code generator
    - Create `generate_python_code()` that produces parseable code
    - Use simple templates (function defs, imports, assignments)
    - Validate with ast.parse()
    - _Requirements: 7.2_

  - [x] 2.3 Implement dependency specification generators
    - Create `generate_dependency_spec()` for pip format (package==1.0.0)
    - Create generator for npm format ("package": "^1.0.0")
    - Create generator for poetry format (package = "^1.0.0")
    - _Requirements: 7.3_

  - [x] 2.4 Implement file tree generator
    - Create `generate_file_tree()` that produces valid directory structures
    - Include files with various extensions (.py, .js, .ts)
    - Include ignored directories (node_modules, __pycache__)
    - Ensure no invalid path characters
    - _Requirements: 7.4_

  - [x] 2.5 Implement repository metadata generator
    - Create `generate_repository_metadata()` with all required fields
    - Include default_branch, last_commit, size, etc.
    - _Requirements: 2.3_

  - [x] 2.6 Implement analysis result generator
    - Create `generate_analysis_result()` with complete structure
    - Include languages, frameworks, issues, tech_debt
    - Ensure internal consistency (percentages sum to 100%)
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [x] 3. Implement repository ingestion property tests
  - [x] 3.1 Write property test for invalid URL rejection
    - **Property 1: Invalid URL Rejection**
    - **Validates: Requirements 2.1**
    - Use `generate_invalid_url()` to create test cases
    - Verify all invalid URLs are rejected
    - Check error messages are appropriate

  - [x] 3.2 Write property test for valid URL acceptance
    - **Property 2: Valid URL Acceptance**
    - **Validates: Requirements 2.2**
    - Use `generate_git_url()` to create test cases
    - Verify all valid URLs pass validation
    - No exceptions should be raised

  - [x] 3.3 Write property test for metadata extraction
    - **Property 3: Metadata Extraction Completeness**
    - **Validates: Requirements 2.3**
    - Mock repository cloning to avoid network calls
    - Verify all required fields are present
    - Check field types are correct

  - [x] 3.4 Write property test for network error handling
    - **Property 4: Network Error Handling**
    - **Validates: Requirements 2.4**
    - Mock network errors (timeout, connection refused)
    - Verify graceful error handling
    - Ensure no crashes or unhandled exceptions

- [ ] 4. Implement file scanning property tests
  - [ ] 4.1 Write property test for file identification
    - **Property 5: File Identification Completeness**
    - **Validates: Requirements 3.1**
    - Use `generate_file_tree()` to create test directories
    - Create temporary file system with generated structure
    - Verify all files with supported extensions are found
    - Check no files are missed

  - [ ] 4.2 Write property test for ignored directory exclusion
    - **Property 6: Ignored Directory Exclusion**
    - **Validates: Requirements 3.2**
    - Generate file trees with ignored directories
    - Verify ignored directories don't appear in results
    - Check their contents are also excluded

  - [ ] 4.3 Write property test for statistics consistency
    - **Property 7: File Statistics Consistency**
    - **Validates: Requirements 3.3**
    - Generate diverse file trees
    - Scan and get statistics
    - Verify sum of counts by language equals total
    - Verify sum of counts by extension equals total

  - [ ] 4.4 Write property test for language categorization
    - **Property 8: Language Categorization Accuracy**
    - **Validates: Requirements 3.4**
    - Generate files with known extensions
    - Verify correct language assignment
    - Test all supported extensions (.py, .js, .ts, .jsx, .tsx)

- [ ] 5. Implement dependency extraction property tests
  - [ ] 5.1 Write property test for requirements.txt parsing
    - **Property 9: Requirements.txt Parsing Completeness**
    - **Validates: Requirements 4.1**
    - Generate valid requirements.txt content
    - Parse with dependency extractor
    - Verify all dependencies extracted
    - Check version constraints preserved

  - [ ] 5.2 Write property test for package.json parsing
    - **Property 10: Package.json Dependency Classification**
    - **Validates: Requirements 4.2**
    - Generate valid package.json with dependencies and devDependencies
    - Parse with dependency extractor
    - Verify correct classification
    - Check no misclassification between types

  - [ ] 5.3 Write property test for pyproject.toml parsing
    - **Property 11: Pyproject.toml Parsing Accuracy**
    - **Validates: Requirements 4.3**
    - Generate valid pyproject.toml content
    - Parse with dependency extractor
    - Verify all dependencies extracted
    - Check version constraints preserved

  - [ ] 5.4 Write property test for malformed file handling
    - **Property 12: Malformed File Error Handling**
    - **Validates: Requirements 4.4**
    - Generate malformed files (invalid JSON, invalid TOML)
    - Attempt to parse with dependency extractor
    - Verify graceful error handling
    - Ensure no crashes

- [ ] 6. Implement analysis completeness property tests
  - [ ] 6.1 Write property test for language percentage summation
    - **Property 13: Language Percentage Summation**
    - **Validates: Requirements 5.1**
    - Generate analysis results with languages
    - Verify percentages sum to 100% (or 0% if no files)
    - Test with various language combinations

  - [ ] 6.2 Write property test for file count consistency
    - **Property 14: Analysis File Count Consistency**
    - **Validates: Requirements 5.2**
    - Generate analysis results
    - Verify total_files equals sum of file_count by language
    - Test with various file distributions

  - [ ] 6.3 Write property test for issue file path validity
    - **Property 15: Issue File Path Validity**
    - **Validates: Requirements 5.3**
    - Generate analysis results with issues
    - Verify all file paths are valid relative paths
    - Check no absolute paths, no null bytes, no path traversal

  - [ ] 6.4 Write property test for technical debt grade consistency
    - **Property 16: Technical Debt Grade Consistency**
    - **Validates: Requirements 5.4**
    - Generate analysis results with maintainability scores
    - Verify grade matches score (A: 80-100, B: 60-79, C: 40-59, D: 20-39, F: 0-19)
    - Test all grade boundaries

- [ ] 7. Implement data persistence property tests
  - [ ] 7.1 Write property test for data persistence round-trip
    - **Property 17: Data Persistence Round-Trip**
    - **Validates: Requirements 6.1, 6.2, 6.3**
    - Generate random analysis results
    - Store in database
    - Retrieve from database
    - Verify all fields preserved
    - Check JSON structures intact
    - Use database rollback fixtures for cleanup

  - [ ] 7.2 Write property test for timestamp preservation
    - **Property 18: Timestamp Preservation**
    - **Validates: Requirements 6.4**
    - Generate random timestamps
    - Store in database
    - Retrieve from database
    - Verify same moment in time
    - Check timezone is UTC

- [ ] 8. Implement generator validation property tests
  - [ ] 8.1 Write property test for URL generator validity
    - **Property 19: Generator URL Validity**
    - **Validates: Requirements 7.1**
    - Generate many URLs with `generate_git_url()`
    - Verify all pass URL validation
    - This is a meta-test for the generator itself

  - [ ] 8.2 Write property test for Python code generator validity
    - **Property 20: Generator Python Syntax Validity**
    - **Validates: Requirements 7.2**
    - Generate many Python code samples
    - Verify all parse with ast.parse()
    - This is a meta-test for the generator itself

  - [ ] 8.3 Write property test for dependency generator validity
    - **Property 21: Generator Dependency Format Validity**
    - **Validates: Requirements 7.3**
    - Generate many dependency specs
    - Verify all match expected format
    - Test for pip, npm, and poetry formats

  - [ ] 8.4 Write property test for directory tree generator validity
    - **Property 22: Generator Directory Tree Validity**
    - **Validates: Requirements 7.4**
    - Generate many directory structures
    - Verify all paths are valid
    - Check no invalid characters, no path traversal

- [ ] 9. Configure CI and documentation
  - [ ] 9.1 Update CI configuration
    - Add property test execution to GitHub Actions
    - Configure to run with 100 examples
    - Add nightly run with 1000 examples
    - Set up test result reporting

  - [ ] 9.2 Document property testing approach
    - Add section to README about property tests
    - Document how to run property tests
    - Explain how to debug failing properties
    - Add examples of property test output

  - [ ] 9.3 Create troubleshooting guide
    - Document common property test failures
    - Explain Hypothesis shrinking
    - Provide debugging strategies
    - Add FAQ section

- [ ] 10. Final checkpoint - Ensure all tests pass
  - Run complete test suite including all property tests
  - Verify all 22 properties pass with 100 examples each
  - Check test execution time is reasonable (< 2 minutes)
  - Ensure all tests pass, ask the user if questions arise.
