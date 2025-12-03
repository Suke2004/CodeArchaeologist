"""
Property-based tests for repository ingestion.
Tests correctness properties using Hypothesis.
"""

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from services.repository_ingester import RepositoryIngester
from tests.test_generators import github_urls, invalid_urls


class TestRepositoryIngestionProperties:
    """Property-based tests for repository ingestion."""
    
    @pytest.fixture
    def ingester(self):
        """Create ingester instance."""
        return RepositoryIngester()
    
    # Feature: code-archaeologist, Property 2: Invalid input rejection
    @given(url=invalid_urls())
    @settings(max_examples=50)
    def test_invalid_urls_are_rejected(self, ingester, url):
        """
        Property 2: Invalid input rejection
        
        For any invalid URL, the system should reject it with False.
        Validates: Requirements 1.2
        """
        # Property: Invalid URLs should always be rejected
        assert ingester.validate_url(url) is False
    
    # Feature: code-archaeologist, Property 1: Repository ingestion completeness (partial)
    @given(url=github_urls())
    @settings(max_examples=20)
    def test_valid_github_urls_are_accepted(self, ingester, url):
        """
        Property 1: Repository ingestion completeness (URL validation part)
        
        For any valid GitHub URL, validation should return True.
        Validates: Requirements 1.1
        """
        # Property: Valid GitHub URLs should always be accepted
        assert ingester.validate_url(url) is True
    
    @given(url=github_urls())
    @settings(max_examples=20)
    def test_repo_info_extraction_is_consistent(self, ingester, url):
        """
        Property: Repository info extraction consistency
        
        For any valid URL, extracting info twice should give same result.
        """
        # Property: Extraction should be deterministic
        info1 = ingester.extract_repo_info(url)
        info2 = ingester.extract_repo_info(url)
        
        assert info1 == info2
        assert 'owner' in info1
        assert 'name' in info1
        assert len(info1['owner']) > 0
        assert len(info1['name']) > 0
    
    @given(url=github_urls())
    @settings(max_examples=20)
    def test_extracted_repo_name_is_in_url(self, ingester, url):
        """
        Property: Extracted repository name appears in URL
        
        For any valid URL, the extracted name should be part of the URL.
        """
        info = ingester.extract_repo_info(url)
        
        # Property: Extracted name should be in the URL
        assert info['name'] in url or info['name'].replace('-', '') in url.replace('-', '')
    
    @given(
        url=github_urls(),
        data=st.data()
    )
    @settings(max_examples=10)
    def test_url_validation_is_idempotent(self, ingester, url, data):
        """
        Property: URL validation is idempotent
        
        For any URL, validating it multiple times gives the same result.
        """
        # Property: f(x) = f(f(x)) for validation
        result1 = ingester.validate_url(url)
        result2 = ingester.validate_url(url)
        result3 = ingester.validate_url(url)
        
        assert result1 == result2 == result3


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
