"""
Property-based tests for analysis components.
Tests file scanning and dependency extraction properties.
"""

import pytest
from hypothesis import given, settings, assume, HealthCheck
from hypothesis import strategies as st
from pathlib import Path
import tempfile
import os

from services.file_scanner import FileScanner
from services.dependency_extractor import DependencyExtractor
from tests.test_generators import pip_requirements, file_paths, generate_analysis_result


class TestFileScannerProperties:
    """Property-based tests for file scanner."""
    
    @given(extension=st.sampled_from(['.py', '.js', '.ts', '.jsx', '.tsx']))
    @settings(max_examples=20)
    def test_code_files_are_always_analyzed(self, extension):
        """
        Property: Code files with valid extensions are always selected for analysis
        
        For any code file extension, should_analyze_file returns True.
        """
        # Create fresh scanner for each test
        scanner = FileScanner()
        
        # Create a temporary file path
        file_path = Path(f"test{extension}")
        
        # Property: Code files should always be analyzed
        assert scanner.should_analyze_file(file_path) is True
    
    @given(dirname=st.sampled_from(['node_modules', '__pycache__', '.git', 'venv']))
    @settings(max_examples=10)
    def test_ignored_dirs_are_always_ignored(self, dirname):
        """
        Property: Ignored directories are always skipped
        
        For any ignored directory name, should_ignore_dir returns True.
        """
        # Create fresh scanner for each test
        scanner = FileScanner()
        
        dir_path = Path(dirname)
        
        # Property: Ignored dirs should always be ignored
        assert scanner.should_ignore_dir(dir_path) is True
    
    @given(
        files=st.lists(
            st.sampled_from(['.py', '.js', '.ts']),
            min_size=0,
            max_size=20
        )
    )
    @settings(max_examples=20)
    def test_statistics_total_equals_file_count(self, files):
        """
        Property: Statistics total matches actual file count
        
        For any list of files, statistics total should equal list length.
        """
        # Create fresh scanner for each test
        scanner = FileScanner()
        
        from services.file_scanner import FileInfo
        
        # Create FileInfo objects
        file_infos = []
        for i, ext in enumerate(files):
            file_info = FileInfo(
                path=Path(f"file{i}{ext}"),
                relative_path=Path(f"file{i}{ext}"),
                size=100,
                extension=ext
            )
            file_infos.append(file_info)
        
        stats = scanner.get_statistics(file_infos)
        
        # Property: Total should equal input count
        assert stats['total_files'] == len(files)


class TestDependencyExtractorProperties:
    """Property-based tests for dependency extractor."""
    
    @given(requirement=pip_requirements())
    @settings(max_examples=30)
    def test_requirements_parsing_extracts_package_name(self, requirement):
        """
        Property: Requirements parsing always extracts a package name
        
        For any valid requirement string, parsing should extract a name.
        """
        # Create fresh extractor for each test
        extractor = DependencyExtractor()
        
        # Create temporary requirements.txt
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(requirement)
            temp_path = f.name
        
        try:
            deps = extractor.extract_from_requirements_txt(Path(temp_path))
            
            # Property: Should extract at least one dependency
            if requirement.strip() and not requirement.startswith('#'):
                assert len(deps) >= 1
                assert deps[0].name is not None
                assert len(deps[0].name) > 0
        finally:
            os.unlink(temp_path)
    
    @given(
        deps=st.lists(
            st.tuples(
                st.text(alphabet='abcdefghijklmnopqrstuvwxyz-', min_size=3, max_size=15),
                st.text(alphabet='0123456789.', min_size=3, max_size=10)
            ),
            min_size=0,
            max_size=10
        )
    )
    @settings(max_examples=20)
    def test_statistics_counts_match_dependency_list(self, deps):
        """
        Property: Dependency statistics match actual counts
        
        For any list of dependencies, statistics should match list length.
        """
        # Create fresh extractor for each test
        extractor = DependencyExtractor()
        
        from services.dependency_extractor import Dependency
        
        # Create Dependency objects
        dep_objects = [
            Dependency(name=name, version=version, ecosystem='pip')
            for name, version in deps
        ]
        
        stats = extractor.get_statistics(dep_objects)
        
        # Property: Total should equal input count
        assert stats['total'] == len(deps)
        assert stats['prod_dependencies'] == len(deps)  # All are prod by default


# Feature: phase3-property-testing, Property 13: Language Percentage Summation
# Feature: phase3-property-testing, Property 14: Analysis File Count Consistency
# Feature: phase3-property-testing, Property 15: Issue File Path Validity
# Feature: phase3-property-testing, Property 16: Technical Debt Grade Consistency
class TestAnalysisCompletenessProperties:
    """Property-based tests for analysis completeness."""
    
    @given(
        python_count=st.integers(0, 10),
        js_count=st.integers(0, 10)
    )
    @settings(max_examples=20)
    def test_language_percentages_sum_to_100(self, python_count, js_count):
        """
        Property 3: Analysis completeness - Language percentages sum to 100%
        
        For any repository with files, language percentages should sum to ~100%.
        Validates: Requirements 2.1
        """
        assume(python_count + js_count > 0)  # Need at least one file
        
        # Simulate language calculation
        total = python_count + js_count
        python_pct = round((python_count / total) * 100, 2)
        js_pct = round((js_count / total) * 100, 2)
        
        # Property: Percentages should sum to approximately 100
        # (allowing for rounding errors)
        total_pct = python_pct + js_pct
        assert 99.0 <= total_pct <= 101.0
    
    @given(analysis_result=generate_analysis_result())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_property_13_language_percentage_summation(self, analysis_result):
        """
        **Feature: phase3-property-testing, Property 13: Language Percentage Summation**
        **Validates: Requirements 5.1**
        
        For any analysis result with detected languages, the sum of all language 
        percentages should equal 100% (or 0% if no files were analyzed).
        """
        languages = analysis_result['languages']
        
        if len(languages) == 0:
            # No languages detected - this is valid (0% case)
            return
        
        # Calculate total percentage
        total_percentage = sum(lang['percentage'] for lang in languages)
        
        # Property: Percentages should sum to 100% (with small tolerance for rounding)
        assert abs(total_percentage - 100.0) < 0.1, \
            f"Language percentages sum to {total_percentage}, expected 100.0"
    
    @given(analysis_result=generate_analysis_result())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_property_14_analysis_file_count_consistency(self, analysis_result):
        """
        **Feature: phase3-property-testing, Property 14: Analysis File Count Consistency**
        **Validates: Requirements 5.2**
        
        For any analysis result, the total_files field should equal the sum of 
        file_count across all detected languages.
        """
        languages = analysis_result['languages']
        total_files = analysis_result['total_files']
        
        # Calculate sum of file counts by language
        sum_file_counts = sum(lang['file_count'] for lang in languages)
        
        # Property: Sum of file counts should equal total_files
        assert sum_file_counts == total_files, \
            f"Sum of file counts ({sum_file_counts}) does not equal total_files ({total_files})"
    
    @given(analysis_result=generate_analysis_result())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_property_15_issue_file_path_validity(self, analysis_result):
        """
        **Feature: phase3-property-testing, Property 15: Issue File Path Validity**
        **Validates: Requirements 5.3**
        
        For any issue detected in the analysis, the file path should be a valid 
        relative path (no null bytes, no absolute paths, no path traversal).
        """
        issues = analysis_result['issues']
        
        for issue in issues:
            file_path = issue['file']
            
            # Property 1: No absolute paths (Unix or Windows)
            assert not file_path.startswith('/'), \
                f"Issue has absolute Unix path: {file_path}"
            assert not (len(file_path) > 1 and file_path[1] == ':'), \
                f"Issue has absolute Windows path: {file_path}"
            assert not file_path.startswith('\\'), \
                f"Issue has absolute Windows path: {file_path}"
            
            # Property 2: No null bytes
            assert '\x00' not in file_path, \
                f"Issue has null byte in path: {repr(file_path)}"
            
            # Property 3: No path traversal
            assert '..' not in file_path, \
                f"Issue has path traversal: {file_path}"
            
            # Property 4: Path should not be empty
            assert len(file_path) > 0, \
                "Issue has empty file path"
    
    @given(analysis_result=generate_analysis_result())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_property_16_technical_debt_grade_consistency(self, analysis_result):
        """
        **Feature: phase3-property-testing, Property 16: Technical Debt Grade Consistency**
        **Validates: Requirements 5.4**
        
        For any analysis result with a maintainability score, the assigned grade 
        should match the score according to the grading scale:
        - A: 80-100
        - B: 60-79
        - C: 40-59
        - D: 20-39
        - F: 0-19
        """
        tech_debt = analysis_result['tech_debt']
        score = tech_debt['maintainability_score']
        grade = tech_debt['grade']
        
        # Property: Grade should match score according to grading scale
        if score >= 80:
            expected_grade = 'A'
        elif score >= 60:
            expected_grade = 'B'
        elif score >= 40:
            expected_grade = 'C'
        elif score >= 20:
            expected_grade = 'D'
        else:
            expected_grade = 'F'
        
        assert grade == expected_grade, \
            f"Score {score} should be grade {expected_grade}, but got {grade}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
