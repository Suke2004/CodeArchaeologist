"""
Property-based tests for file scanning.
Tests correctness properties using Hypothesis.
"""

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st
from pathlib import Path
import tempfile
import shutil

from services.file_scanner import FileScanner, FileInfo
from tests.test_generators import generate_file_tree


class TestFileScanningProperties:
    """Property-based tests for file scanning."""
    
    # ========================================================================
    # Property 5: File Identification Completeness
    # Feature: phase3-property-testing, Property 5: File Identification Completeness
    # Validates: Requirements 3.1
    # ========================================================================
    
    @given(file_tree=generate_file_tree())
    @settings(max_examples=100, deadline=10000)
    def test_property_5_file_identification_completeness(self, file_tree):
        """
        **Feature: phase3-property-testing, Property 5: File Identification Completeness**
        **Validates: Requirements 3.1**
        
        For any directory structure, the file scanner should identify all files 
        with supported extensions (.py, .js, .ts, .jsx, .tsx) and no files 
        should be missed if they have these extensions.
        
        Property: All files with supported extensions are found
        """
        # Skip empty trees
        assume(len(file_tree) > 0)
        
        scanner = FileScanner()
        
        # Create temporary directory with the generated structure
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            
            # Create the file tree on disk
            expected_files = self._create_file_tree(repo_path, file_tree)
            
            # Scan the directory
            scanned_files = scanner.scan_directory(repo_path)
            
            # Get paths of scanned files (normalize to forward slashes for comparison)
            scanned_paths = {str(f.relative_path).replace('\\', '/') for f in scanned_files}
            
            # Property: All expected files with supported extensions should be found
            supported_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx'}
            
            for expected_path in expected_files:
                file_path = Path(expected_path)
                
                # Check if file has supported extension
                if file_path.suffix in supported_extensions:
                    # Check if file is in an ignored directory
                    if not self._is_in_ignored_dir(file_path):
                        # Normalize path for comparison (use forward slashes)
                        normalized_expected = expected_path.replace('\\', '/')
                        assert normalized_expected in scanned_paths, \
                            f"File with supported extension was missed: {expected_path}"
    
    # ========================================================================
    # Property 6: Ignored Directory Exclusion
    # Feature: phase3-property-testing, Property 6: Ignored Directory Exclusion
    # Validates: Requirements 3.2
    # ========================================================================
    
    @given(file_tree=generate_file_tree())
    @settings(max_examples=100, deadline=10000)
    def test_property_6_ignored_directory_exclusion(self, file_tree):
        """
        **Feature: phase3-property-testing, Property 6: Ignored Directory Exclusion**
        **Validates: Requirements 3.2**
        
        For any directory structure containing ignored directories (node_modules, 
        __pycache__, .git, .venv, dist, build), the scanner should skip these 
        directories and none of their contents should appear in the results.
        
        Property: No files from ignored directories appear in results
        """
        # Skip empty trees
        assume(len(file_tree) > 0)
        
        scanner = FileScanner()
        
        # Create temporary directory with the generated structure
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            
            # Create the file tree on disk
            self._create_file_tree(repo_path, file_tree)
            
            # Scan the directory
            scanned_files = scanner.scan_directory(repo_path)
            
            # Property: No scanned file should be in an ignored directory
            ignored_dirs = scanner.ignore_dirs
            
            for file_info in scanned_files:
                file_path = Path(file_info.relative_path)
                
                # Check all parent directories
                for parent in file_path.parents:
                    parent_name = parent.name
                    assert parent_name not in ignored_dirs, \
                        f"File from ignored directory was included: {file_info.relative_path} " \
                        f"(ignored dir: {parent_name})"
    
    # ========================================================================
    # Property 7: File Statistics Consistency
    # Feature: phase3-property-testing, Property 7: File Statistics Consistency
    # Validates: Requirements 3.3
    # ========================================================================
    
    @given(file_tree=generate_file_tree())
    @settings(max_examples=100, deadline=10000)
    def test_property_7_file_statistics_consistency(self, file_tree):
        """
        **Feature: phase3-property-testing, Property 7: File Statistics Consistency**
        **Validates: Requirements 3.3**
        
        For any scanned repository, the sum of file counts by language should 
        equal the total files count, and the sum of file counts by extension 
        should also equal the total files count.
        
        Property: Statistics are internally consistent
        """
        # Skip empty trees
        assume(len(file_tree) > 0)
        
        scanner = FileScanner()
        
        # Create temporary directory with the generated structure
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            
            # Create the file tree on disk
            self._create_file_tree(repo_path, file_tree)
            
            # Scan the directory
            scanned_files = scanner.scan_directory(repo_path)
            
            # Get statistics
            stats = scanner.get_statistics(scanned_files)
            
            # Property 1: Sum of counts by language equals total
            total_by_language = sum(stats['by_language'].values())
            assert total_by_language == stats['total_files'], \
                f"Sum of language counts ({total_by_language}) != total files ({stats['total_files']})"
            
            # Property 2: Sum of counts by extension equals total
            total_by_extension = sum(stats['by_extension'].values())
            assert total_by_extension == stats['total_files'], \
                f"Sum of extension counts ({total_by_extension}) != total files ({stats['total_files']})"
            
            # Property 3: Total files equals length of scanned files list
            assert stats['total_files'] == len(scanned_files), \
                f"Total files in stats ({stats['total_files']}) != scanned files count ({len(scanned_files)})"
    
    # ========================================================================
    # Property 8: Language Categorization Accuracy
    # Feature: phase3-property-testing, Property 8: Language Categorization Accuracy
    # Validates: Requirements 3.4
    # ========================================================================
    
    @given(
        extension=st.sampled_from(['.py', '.js', '.ts', '.jsx', '.tsx']),
        filename=st.text(
            alphabet='abcdefghijklmnopqrstuvwxyz_',
            min_size=3,
            max_size=15
        ).filter(lambda x: x[0] != '_' and x[-1] != '_')
    )
    @settings(max_examples=100)
    def test_property_8_language_categorization_accuracy(self, extension, filename):
        """
        **Feature: phase3-property-testing, Property 8: Language Categorization Accuracy**
        **Validates: Requirements 3.4**
        
        For any file path with a known extension, the file scanner should 
        categorize it to the correct language (.py → python, .js → javascript, 
        .ts → typescript).
        
        Property: File extensions are correctly mapped to languages
        """
        scanner = FileScanner()
        
        # Create temporary directory with a single file
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            
            # Create file with the given extension
            file_path = repo_path / f"{filename}{extension}"
            file_path.write_text("# Test content")
            
            # Scan the directory
            scanned_files = scanner.scan_directory(repo_path)
            
            # Should find exactly one file
            assert len(scanned_files) == 1, \
                f"Expected 1 file, found {len(scanned_files)}"
            
            file_info = scanned_files[0]
            
            # Property: Extension should match
            assert file_info.extension == extension, \
                f"Extension mismatch: expected {extension}, got {file_info.extension}"
            
            # Property: Language should be correctly categorized
            expected_language = {
                '.py': 'python',
                '.js': 'javascript',
                '.ts': 'typescript',
                '.jsx': 'javascript',
                '.tsx': 'typescript'
            }[extension]
            
            assert file_info.language == expected_language, \
                f"Language mismatch for {extension}: expected {expected_language}, got {file_info.language}"
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _create_file_tree(self, base_path: Path, tree: dict, current_path: str = "") -> list:
        """
        Recursively create file tree on disk.
        
        Args:
            base_path: Base directory path
            tree: Dictionary representing file tree
            current_path: Current relative path (for tracking)
        
        Returns:
            List of relative file paths created
        """
        created_files = []
        
        for name, content in tree.items():
            full_path = base_path / name if not current_path else base_path / current_path / name
            relative_path = name if not current_path else f"{current_path}/{name}"
            
            if isinstance(content, dict):
                # It's a directory
                full_path.mkdir(parents=True, exist_ok=True)
                # Recursively create subdirectory contents
                created_files.extend(
                    self._create_file_tree(base_path, content, relative_path)
                )
            else:
                # It's a file
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content)
                created_files.append(relative_path)
        
        return created_files
    
    def _is_in_ignored_dir(self, file_path: Path) -> bool:
        """
        Check if file path is in an ignored directory.
        
        Args:
            file_path: Path to check
        
        Returns:
            True if in ignored directory
        """
        # Match the IGNORE_DIRS from file_scanner.py
        ignored_dirs = {
            '.git', '.svn', '.hg',
            'node_modules', '__pycache__', '.pytest_cache',
            'venv', 'env', '.venv', '.env',
            'dist', 'build', '.next', '.nuxt',
            'coverage', '.coverage', 'htmlcov',
            '.idea', '.vscode', '.vs',
            'target', 'bin', 'obj'
        }
        
        for parent in file_path.parents:
            if parent.name in ignored_dirs:
                return True
        
        # Also check if the file itself is in an ignored directory
        if file_path.parts and any(part in ignored_dirs for part in file_path.parts[:-1]):
            return True
        
        return False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
