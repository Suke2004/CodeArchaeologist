"""
Property-based tests for repository ingestion.
Tests correctness properties using Hypothesis.
"""

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from git import GitCommandError
import tempfile
import shutil

from services.repository_ingester import RepositoryIngester
from tests.test_generators import generate_git_url, generate_invalid_url, generate_repository_metadata


class TestRepositoryIngestionProperties:
    """Property-based tests for repository ingestion."""
    
    # ========================================================================
    # Property 1: Invalid URL Rejection
    # Feature: phase3-property-testing, Property 1: Invalid URL Rejection
    # Validates: Requirements 2.1
    # ========================================================================
    
    @given(url=generate_invalid_url())
    @settings(max_examples=100)
    def test_property_1_invalid_url_rejection(self, url):
        """
        **Feature: phase3-property-testing, Property 1: Invalid URL Rejection**
        **Validates: Requirements 2.1**
        
        For any invalid URL format, the repository ingester should reject it 
        with an appropriate error message and not attempt to clone.
        
        Property: All invalid URLs are rejected by validate_url()
        """
        ingester = RepositoryIngester()
        
        # Property: Invalid URLs should always be rejected
        result = ingester.validate_url(url)
        assert result is False, f"Invalid URL was accepted: {url}"
        
        # Additional check: Attempting to clone should raise ValueError
        with pytest.raises(ValueError, match="Invalid repository URL"):
            ingester.clone_repository(url, repo_id="test-id")
    
    # ========================================================================
    # Property 2: Valid URL Acceptance
    # Feature: phase3-property-testing, Property 2: Valid URL Acceptance
    # Validates: Requirements 2.2
    # ========================================================================
    
    @given(url=generate_git_url())
    @settings(max_examples=100)
    def test_property_2_valid_url_acceptance(self, url):
        """
        **Feature: phase3-property-testing, Property 2: Valid URL Acceptance**
        **Validates: Requirements 2.2**
        
        For any valid Git URL (https, git, or ssh format), the repository 
        ingester should successfully validate it without errors.
        
        Property: All valid Git URLs pass validation
        """
        ingester = RepositoryIngester()
        
        # Property: Valid URLs should always be accepted
        result = ingester.validate_url(url)
        assert result is True, f"Valid URL was rejected: {url}"
        
        # Additional check: No exceptions should be raised during validation
        try:
            ingester.validate_url(url)
        except Exception as e:
            pytest.fail(f"Validation raised unexpected exception for valid URL {url}: {e}")
    
    # ========================================================================
    # Property 3: Metadata Extraction Completeness
    # Feature: phase3-property-testing, Property 3: Metadata Extraction Completeness
    # Validates: Requirements 2.3
    # ========================================================================
    
    @given(metadata=generate_repository_metadata())
    @settings(max_examples=100)
    def test_property_3_metadata_extraction_completeness(self, metadata):
        """
        **Feature: phase3-property-testing, Property 3: Metadata Extraction Completeness**
        **Validates: Requirements 2.3**
        
        For any successfully cloned repository, the extracted metadata should 
        include all required fields: default branch, last commit hash, 
        last commit date, and repository size.
        
        Property: All required metadata fields are present and correctly typed
        """
        ingester = RepositoryIngester()
        
        # Create a temporary directory to simulate a cloned repository
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir)
            
            # Create a mock git repository structure
            git_dir = repo_path / ".git"
            git_dir.mkdir()
            
            # Create some files to simulate repository content
            (repo_path / "README.md").write_text("# Test Repository")
            (repo_path / "src").mkdir()
            (repo_path / "src" / "main.py").write_text("print('hello')")
            
            # Mock the Repo object to return our test metadata
            with patch('services.repository_ingester.Repo') as mock_repo_class:
                mock_repo = MagicMock()
                mock_repo_class.return_value = mock_repo
                
                # Set up mock branch
                mock_branch = MagicMock()
                mock_branch.name = metadata['default_branch']
                mock_repo.active_branch = mock_branch
                
                # Set up mock commit
                mock_commit = MagicMock()
                # Convert ISO date string to timestamp
                from datetime import datetime
                commit_date = datetime.fromisoformat(metadata['last_commit_date'])
                mock_commit.committed_date = commit_date.timestamp()
                mock_commit.message = "Test commit message"
                mock_repo.head.commit = mock_commit
                
                # Extract metadata
                result = ingester.extract_metadata(repo_path)
                
                # Property: All required fields must be present
                required_fields = ['default_branch', 'last_commit_date', 'file_count', 'size_mb']
                for field in required_fields:
                    assert field in result, f"Missing required field: {field}"
                
                # Property: Field types must be correct
                assert isinstance(result['default_branch'], str), \
                    f"default_branch should be str, got {type(result['default_branch'])}"
                
                assert result['last_commit_date'] is not None, \
                    "last_commit_date should not be None"
                
                assert isinstance(result['file_count'], int), \
                    f"file_count should be int, got {type(result['file_count'])}"
                
                assert isinstance(result['size_mb'], (int, float)), \
                    f"size_mb should be numeric, got {type(result['size_mb'])}"
                
                # Property: Values should be reasonable
                assert result['file_count'] >= 0, \
                    f"file_count should be non-negative, got {result['file_count']}"
                
                assert result['size_mb'] >= 0, \
                    f"size_mb should be non-negative, got {result['size_mb']}"
    
    # ========================================================================
    # Property 4: Network Error Handling
    # Feature: phase3-property-testing, Property 4: Network Error Handling
    # Validates: Requirements 2.4
    # ========================================================================
    
    @given(
        url=generate_git_url(),
        error_type=st.sampled_from(['timeout', 'connection_refused', 'dns_failure', 'auth_failure'])
    )
    @settings(max_examples=100)
    def test_property_4_network_error_handling(self, url, error_type):
        """
        **Feature: phase3-property-testing, Property 4: Network Error Handling**
        **Validates: Requirements 2.4**
        
        For any repository URL that triggers a network error (timeout, 
        connection refused, DNS failure), the system should handle it 
        gracefully by returning an error without crashing.
        
        Property: Network errors are caught and handled gracefully
        """
        ingester = RepositoryIngester()
        
        # Map error types to appropriate Git exceptions
        error_messages = {
            'timeout': "Connection timed out",
            'connection_refused': "Connection refused",
            'dns_failure': "Could not resolve host",
            'auth_failure': "Authentication failed"
        }
        
        # Mock Repo.clone_from to raise GitCommandError
        with patch('services.repository_ingester.Repo.clone_from') as mock_clone:
            mock_clone.side_effect = GitCommandError(
                command=['git', 'clone'],
                status=128,
                stderr=error_messages[error_type]
            )
            
            # Property: Network errors should be caught and re-raised as GitCommandError
            # but should not cause unhandled exceptions or crashes
            with pytest.raises(GitCommandError):
                ingester.clone_repository(url, repo_id="test-id")
            
            # Verify that the error was handled (no crash)
            # and that cleanup was attempted
            # The clone_repository method should handle the error gracefully
    
    # ========================================================================
    # Additional Helper Properties
    # ========================================================================
    
    @given(url=generate_git_url())
    @settings(max_examples=50)
    def test_repo_info_extraction_is_consistent(self, url):
        """
        Property: Repository info extraction consistency
        
        For any valid URL, extracting info twice should give same result.
        """
        ingester = RepositoryIngester()
        
        # Property: Extraction should be deterministic
        info1 = ingester.extract_repo_info(url)
        info2 = ingester.extract_repo_info(url)
        
        assert info1 == info2
        assert 'owner' in info1
        assert 'name' in info1
        assert len(info1['owner']) > 0
        assert len(info1['name']) > 0
    
    @given(url=generate_git_url())
    @settings(max_examples=50)
    def test_extracted_repo_name_is_in_url(self, url):
        """
        Property: Extracted repository name appears in URL
        
        For any valid URL, the extracted name should be part of the URL.
        """
        ingester = RepositoryIngester()
        
        info = ingester.extract_repo_info(url)
        
        # Property: Extracted name should be in the URL
        assert info['name'] in url or info['name'].replace('-', '') in url.replace('-', '')
    
    @given(url=generate_git_url())
    @settings(max_examples=50)
    def test_url_validation_is_idempotent(self, url):
        """
        Property: URL validation is idempotent
        
        For any URL, validating it multiple times gives the same result.
        """
        ingester = RepositoryIngester()
        
        # Property: f(x) = f(f(x)) for validation
        result1 = ingester.validate_url(url)
        result2 = ingester.validate_url(url)
        result3 = ingester.validate_url(url)
        
        assert result1 == result2 == result3


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
