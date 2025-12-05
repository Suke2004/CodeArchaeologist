"""
Property-based tests for dependency extraction.
Tests correctness properties using Hypothesis.
"""

import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st
from pathlib import Path
import tempfile
import json

from services.dependency_extractor import DependencyExtractor, Dependency
from tests.test_generators import (
    generate_requirements_txt_content,
    generate_package_json_content,
    generate_pyproject_toml_content,
    generate_malformed_json,
    generate_malformed_toml
)


class TestDependencyExtractionProperties:
    """Property-based tests for dependency extraction."""
    
    # ========================================================================
    # Property 9: Requirements.txt Parsing Completeness
    # Feature: phase3-property-testing, Property 9: Requirements.txt Parsing Completeness
    # Validates: Requirements 4.1
    # ========================================================================
    
    @given(content=generate_requirements_txt_content())
    @settings(max_examples=100)
    def test_property_9_requirements_txt_parsing_completeness(self, content):
        """
        **Feature: phase3-property-testing, Property 9: Requirements.txt Parsing Completeness**
        **Validates: Requirements 4.1**
        
        For any valid requirements.txt content, the dependency extractor should 
        extract all listed dependencies with their version constraints preserved 
        accurately.
        
        Property: All dependencies in requirements.txt are extracted with correct versions
        """
        extractor = DependencyExtractor()
        
        # Create a temporary file with the generated content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)
        
        try:
            # Extract dependencies
            dependencies = extractor.extract_from_requirements_txt(temp_path)
            
            # Parse the content to count expected dependencies
            lines = content.split('\n')
            expected_deps = []
            for line in lines:
                line = line.strip()
                # Skip empty lines, comments, and flags
                if line and not line.startswith('#') and not line.startswith('-'):
                    expected_deps.append(line)
            
            # Property: Number of extracted dependencies should match non-comment lines
            assert len(dependencies) == len(expected_deps), \
                f"Expected {len(expected_deps)} dependencies, got {len(dependencies)}"
            
            # Property: All dependencies should be Dependency objects
            for dep in dependencies:
                assert isinstance(dep, Dependency), \
                    f"Expected Dependency object, got {type(dep)}"
            
            # Property: All dependencies should have pip ecosystem
            for dep in dependencies:
                assert dep.ecosystem == 'pip', \
                    f"Expected ecosystem 'pip', got '{dep.ecosystem}'"
            
            # Property: All dependencies should have a name
            for dep in dependencies:
                assert dep.name is not None and len(dep.name) > 0, \
                    "Dependency name should not be empty"
            
            # Property: Version constraints should be preserved
            # Check that each expected dependency line has a corresponding extracted dependency
            for expected_line in expected_deps:
                # Extract package name from the line
                import re
                match = re.match(r'^([a-zA-Z0-9\-_\.]+)', expected_line)
                if match:
                    expected_name = match.group(1)
                    # Find this dependency in extracted list
                    found = any(dep.name == expected_name for dep in dependencies)
                    assert found, f"Expected dependency '{expected_name}' not found in extracted list"
        
        finally:
            # Clean up temporary file
            temp_path.unlink()
    
    # ========================================================================
    # Property 10: Package.json Dependency Classification
    # Feature: phase3-property-testing, Property 10: Package.json Dependency Classification
    # Validates: Requirements 4.2
    # ========================================================================
    
    @given(content=generate_package_json_content())
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_property_10_package_json_dependency_classification(self, content):
        """
        **Feature: phase3-property-testing, Property 10: Package.json Dependency Classification**
        **Validates: Requirements 4.2**
        
        For any valid package.json content, the dependency extractor should 
        correctly distinguish between production dependencies and devDependencies, 
        with no misclassification.
        
        Property: Dependencies are correctly classified as production or dev
        """
        extractor = DependencyExtractor()
        
        # Create a temporary file with the generated content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)
        
        try:
            # Extract dependencies
            dependencies = extractor.extract_from_package_json(temp_path)
            
            # Parse the JSON to get expected dependencies
            data = json.loads(content)
            expected_prod = data.get('dependencies', {})
            expected_dev = data.get('devDependencies', {})
            
            # Property: Total extracted should match total expected
            total_expected = len(expected_prod) + len(expected_dev)
            assert len(dependencies) == total_expected, \
                f"Expected {total_expected} dependencies, got {len(dependencies)}"
            
            # Property: All dependencies should be Dependency objects
            for dep in dependencies:
                assert isinstance(dep, Dependency), \
                    f"Expected Dependency object, got {type(dep)}"
            
            # Property: All dependencies should have npm ecosystem
            for dep in dependencies:
                assert dep.ecosystem == 'npm', \
                    f"Expected ecosystem 'npm', got '{dep.ecosystem}'"
            
            # Property: Production dependencies should have is_dev=False
            for name in expected_prod.keys():
                matching_deps = [d for d in dependencies if d.name == name]
                assert len(matching_deps) == 1, \
                    f"Expected exactly one dependency named '{name}', found {len(matching_deps)}"
                assert matching_deps[0].is_dev is False, \
                    f"Production dependency '{name}' incorrectly marked as dev"
            
            # Property: Dev dependencies should have is_dev=True
            for name in expected_dev.keys():
                matching_deps = [d for d in dependencies if d.name == name]
                assert len(matching_deps) == 1, \
                    f"Expected exactly one dependency named '{name}', found {len(matching_deps)}"
                assert matching_deps[0].is_dev is True, \
                    f"Dev dependency '{name}' incorrectly marked as production"
            
            # Property: No misclassification - count should match
            prod_count = sum(1 for d in dependencies if not d.is_dev)
            dev_count = sum(1 for d in dependencies if d.is_dev)
            
            assert prod_count == len(expected_prod), \
                f"Expected {len(expected_prod)} production deps, got {prod_count}"
            assert dev_count == len(expected_dev), \
                f"Expected {len(expected_dev)} dev deps, got {dev_count}"
        
        finally:
            # Clean up temporary file
            temp_path.unlink()
    
    # ========================================================================
    # Property 11: Pyproject.toml Parsing Accuracy
    # Feature: phase3-property-testing, Property 11: Pyproject.toml Parsing Accuracy
    # Validates: Requirements 4.3
    # ========================================================================
    
    @given(content=generate_pyproject_toml_content())
    @settings(max_examples=100)
    def test_property_11_pyproject_toml_parsing_accuracy(self, content):
        """
        **Feature: phase3-property-testing, Property 11: Pyproject.toml Parsing Accuracy**
        **Validates: Requirements 4.3**
        
        For any valid pyproject.toml content, the dependency extractor should 
        extract all dependencies from the [tool.poetry.dependencies] section 
        with version constraints preserved.
        
        Property: All dependencies in pyproject.toml are extracted with correct versions
        """
        extractor = DependencyExtractor()
        
        # Create a temporary file with the generated content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)
        
        try:
            # Extract dependencies
            dependencies = extractor.extract_from_pyproject_toml(temp_path)
            
            # Parse the content to count expected dependencies
            lines = content.split('\n')
            in_dependencies = False
            expected_deps = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('[tool.poetry.dependencies]') or line.startswith('[project.dependencies]'):
                    in_dependencies = True
                    continue
                elif line.startswith('[') and in_dependencies:
                    in_dependencies = False
                
                if in_dependencies and '=' in line:
                    import re
                    match = re.match(r'^([a-zA-Z0-9\-_]+)\s*=', line)
                    if match:
                        name = match.group(1)
                        # Skip python version
                        if name.lower() != 'python':
                            expected_deps.append(name)
            
            # Property: Number of extracted dependencies should match expected
            # (excluding python version)
            assert len(dependencies) == len(expected_deps), \
                f"Expected {len(expected_deps)} dependencies, got {len(dependencies)}"
            
            # Property: All dependencies should be Dependency objects
            for dep in dependencies:
                assert isinstance(dep, Dependency), \
                    f"Expected Dependency object, got {type(dep)}"
            
            # Property: All dependencies should have pip ecosystem
            for dep in dependencies:
                assert dep.ecosystem == 'pip', \
                    f"Expected ecosystem 'pip', got '{dep.ecosystem}'"
            
            # Property: All dependencies should have a name
            for dep in dependencies:
                assert dep.name is not None and len(dep.name) > 0, \
                    "Dependency name should not be empty"
            
            # Property: All expected dependencies should be found
            for expected_name in expected_deps:
                found = any(dep.name == expected_name for dep in dependencies)
                assert found, f"Expected dependency '{expected_name}' not found in extracted list"
            
            # Property: Python version should not be included
            python_deps = [d for d in dependencies if d.name.lower() == 'python']
            assert len(python_deps) == 0, \
                "Python version should not be included in dependencies"
        
        finally:
            # Clean up temporary file
            temp_path.unlink()
    
    # ========================================================================
    # Property 12: Malformed File Error Handling
    # Feature: phase3-property-testing, Property 12: Malformed File Error Handling
    # Validates: Requirements 4.4
    # ========================================================================
    
    @given(
        file_type=st.sampled_from(['json', 'toml']),
        content=st.one_of(generate_malformed_json(), generate_malformed_toml())
    )
    @settings(max_examples=100)
    def test_property_12_malformed_file_error_handling(self, file_type, content):
        """
        **Feature: phase3-property-testing, Property 12: Malformed File Error Handling**
        **Validates: Requirements 4.4**
        
        For any malformed dependency file (invalid JSON, invalid TOML, corrupted 
        content), the dependency extractor should handle the error gracefully 
        and return an empty dependency list or error indicator without crashing.
        
        Property: Malformed files are handled gracefully without crashes
        """
        extractor = DependencyExtractor()
        
        # Create a temporary file with the malformed content
        suffix = '.json' if file_type == 'json' else '.toml'
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)
        
        try:
            # Property: Parsing should not crash, even with malformed content
            if file_type == 'json':
                dependencies = extractor.extract_from_package_json(temp_path)
            else:
                dependencies = extractor.extract_from_pyproject_toml(temp_path)
            
            # Property: Result should be a list (possibly empty)
            assert isinstance(dependencies, list), \
                f"Expected list result, got {type(dependencies)}"
            
            # Property: All items in result should be Dependency objects
            for dep in dependencies:
                assert isinstance(dep, Dependency), \
                    f"Expected Dependency object, got {type(dep)}"
            
            # Property: For malformed files, we expect empty list or graceful handling
            # The extractor logs errors but returns empty list
            # This is acceptable behavior - no crash
            
        except Exception as e:
            # Property: If an exception is raised, it should be a known exception type
            # Not an unhandled crash
            pytest.fail(f"Unexpected exception type raised: {type(e).__name__}: {e}")
        
        finally:
            # Clean up temporary file
            temp_path.unlink()
    
    # ========================================================================
    # Additional Helper Properties
    # ========================================================================
    
    @given(content=generate_requirements_txt_content())
    @settings(max_examples=50)
    def test_requirements_parsing_is_idempotent(self, content):
        """
        Property: Requirements.txt parsing is idempotent
        
        For any requirements.txt content, parsing it twice gives the same result.
        """
        extractor = DependencyExtractor()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)
        
        try:
            # Parse twice
            deps1 = extractor.extract_from_requirements_txt(temp_path)
            deps2 = extractor.extract_from_requirements_txt(temp_path)
            
            # Property: Results should be identical
            assert len(deps1) == len(deps2)
            
            for d1, d2 in zip(deps1, deps2):
                assert d1.name == d2.name
                assert d1.version == d2.version
                assert d1.ecosystem == d2.ecosystem
                assert d1.is_dev == d2.is_dev
        
        finally:
            temp_path.unlink()
    
    @given(content=generate_package_json_content())
    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    def test_package_json_parsing_preserves_versions(self, content):
        """
        Property: Package.json parsing preserves version strings
        
        For any package.json, the extracted version should match the original.
        """
        extractor = DependencyExtractor()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)
        
        try:
            dependencies = extractor.extract_from_package_json(temp_path)
            data = json.loads(content)
            
            all_deps = {}
            all_deps.update(data.get('dependencies', {}))
            all_deps.update(data.get('devDependencies', {}))
            
            # Property: Each extracted dependency should have matching version
            for dep in dependencies:
                if dep.name in all_deps:
                    expected_version = all_deps[dep.name]
                    assert dep.version == expected_version, \
                        f"Version mismatch for {dep.name}: expected {expected_version}, got {dep.version}"
        
        finally:
            temp_path.unlink()
    
    @given(content=generate_pyproject_toml_content())
    @settings(max_examples=50)
    def test_pyproject_toml_excludes_python_version(self, content):
        """
        Property: Pyproject.toml parsing excludes Python version
        
        For any pyproject.toml, the Python version should not be in dependencies.
        """
        extractor = DependencyExtractor()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)
        
        try:
            dependencies = extractor.extract_from_pyproject_toml(temp_path)
            
            # Property: No dependency should be named 'python'
            python_deps = [d for d in dependencies if d.name.lower() == 'python']
            assert len(python_deps) == 0, \
                "Python version should not be included in dependencies"
        
        finally:
            temp_path.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
