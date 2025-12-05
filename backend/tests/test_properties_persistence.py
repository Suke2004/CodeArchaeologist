"""
Property-based tests for data persistence.

Tests that data stored in the database can be retrieved without loss.
"""

import pytest
from hypothesis import given, settings, strategies as st, HealthCheck
from datetime import datetime, timezone
import uuid

from models.repository import LegacyRepo, RepoStatus
from models.analysis import AnalysisResult
from tests.test_generators import (
    generate_analysis_result,
    generate_repository_metadata,
)


@pytest.mark.property
@given(analysis_data=generate_analysis_result())
@settings(
    max_examples=100, 
    deadline=5000,
    suppress_health_check=[HealthCheck.function_scoped_fixture]
)
def test_analysis_persistence_round_trip(db_session, analysis_data):
    """
    Property 17: Data Persistence Round-Trip
    
    Feature: phase3-property-testing, Property 17: Data Persistence Round-Trip
    Validates: Requirements 6.1, 6.2, 6.3
    
    For any analysis result, storing it in the database and then retrieving it
    should return data that is equivalent to the original (all fields preserved,
    JSON structures intact).
    """
    # First create a repository to associate with the analysis
    # Use unique URL for each test iteration
    repo_id = str(uuid.uuid4())
    unique_url = f"https://github.com/test/{repo_id}.git"
    repo = LegacyRepo(
        id=repo_id,
        url=unique_url,
        name="test-repo",
        owner="test",
        user_id="test-user",
        status=RepoStatus.COMPLETE,
    )
    db_session.add(repo)
    db_session.commit()
    
    # Create analysis result with generated data
    analysis_id = str(uuid.uuid4())
    analysis = AnalysisResult(
        id=analysis_id,
        repo_id=repo_id,
        languages=analysis_data['languages'],
        frameworks=analysis_data['frameworks'],
        issues=analysis_data['issues'],
        tech_debt=analysis_data['tech_debt'],
        total_files=analysis_data['total_files'],
        total_lines=analysis_data['total_lines'],
    )
    
    # Store in database
    db_session.add(analysis)
    db_session.commit()
    
    # Retrieve from database
    retrieved = db_session.query(AnalysisResult).filter_by(id=analysis_id).first()
    
    # Verify all fields are preserved
    assert retrieved is not None, "Analysis result should be retrievable"
    assert retrieved.id == analysis_id
    assert retrieved.repo_id == repo_id
    assert retrieved.total_files == analysis_data['total_files']
    assert retrieved.total_lines == analysis_data['total_lines']
    
    # Verify JSON structures are intact
    assert retrieved.languages == analysis_data['languages'], \
        "Languages JSON should be preserved exactly"
    assert retrieved.frameworks == analysis_data['frameworks'], \
        "Frameworks JSON should be preserved exactly"
    assert retrieved.issues == analysis_data['issues'], \
        "Issues JSON should be preserved exactly"
    assert retrieved.tech_debt == analysis_data['tech_debt'], \
        "Tech debt JSON should be preserved exactly"
    
    # Verify language percentages still sum to 100%
    total_percentage = sum(lang['percentage'] for lang in retrieved.languages)
    assert abs(total_percentage - 100.0) < 0.1, \
        f"Language percentages should still sum to 100%, got {total_percentage}"
    
    # Verify file counts still sum to total_files
    total_file_count = sum(lang['file_count'] for lang in retrieved.languages)
    assert total_file_count == retrieved.total_files, \
        f"File counts should still sum to total_files"
    
    # Verify technical debt grade still matches score
    score = retrieved.tech_debt['maintainability_score']
    grade = retrieved.tech_debt['grade']
    
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
        f"Grade {grade} should match score {score} (expected {expected_grade})"


@pytest.mark.property
@given(repo_metadata=generate_repository_metadata())
@settings(
    max_examples=100, 
    deadline=5000,
    suppress_health_check=[HealthCheck.function_scoped_fixture]
)
def test_repository_metadata_persistence(db_session, repo_metadata):
    """
    Test that repository metadata is preserved during database round-trip.
    
    Validates: Requirements 6.1, 6.2
    
    For any repository metadata, storing it in the database and then retrieving it
    should return data that is equivalent to the original.
    """
    # Create repository with generated metadata
    # Use unique URL for each test iteration
    repo_id = str(uuid.uuid4())
    unique_url = f"https://github.com/test/{repo_id}.git"
    repo = LegacyRepo(
        id=repo_id,
        url=unique_url,
        name="test-repo",
        owner="test",
        user_id="test-user",
        status=RepoStatus.COMPLETE,
        repo_metadata=repo_metadata,
    )
    
    # Store in database
    db_session.add(repo)
    db_session.commit()
    
    # Retrieve from database
    retrieved = db_session.query(LegacyRepo).filter_by(id=repo_id).first()
    
    # Verify all metadata fields are preserved
    assert retrieved is not None, "Repository should be retrievable"
    assert retrieved.id == repo_id
    assert retrieved.repo_metadata == repo_metadata, \
        "Repository metadata JSON should be preserved exactly"
    
    # Verify specific metadata fields
    assert retrieved.repo_metadata['default_branch'] == repo_metadata['default_branch']
    assert retrieved.repo_metadata['last_commit'] == repo_metadata['last_commit']
    assert retrieved.repo_metadata['last_commit_date'] == repo_metadata['last_commit_date']
    assert retrieved.repo_metadata['size'] == repo_metadata['size']
    assert retrieved.repo_metadata['language'] == repo_metadata['language']
    assert retrieved.repo_metadata['stars'] == repo_metadata['stars']
    assert retrieved.repo_metadata['forks'] == repo_metadata['forks']



@pytest.mark.property
@given(
    days_ago=st.integers(0, 365),
    hours=st.integers(0, 23),
    minutes=st.integers(0, 59),
    seconds=st.integers(0, 59),
)
@settings(
    max_examples=100, 
    deadline=5000,
    suppress_health_check=[HealthCheck.function_scoped_fixture]
)
def test_timestamp_preservation(db_session, days_ago, hours, minutes, seconds):
    """
    Property 18: Timestamp Preservation
    
    Feature: phase3-property-testing, Property 18: Timestamp Preservation
    Validates: Requirements 6.4
    
    For any timestamp stored in the database, retrieving it should return
    the same moment in time with correct timezone information (UTC).
    """
    from datetime import timedelta
    
    # Generate a timestamp (naive datetime for SQLite compatibility)
    base_time = datetime.now()
    test_timestamp = base_time - timedelta(
        days=days_ago,
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )
    
    # Create repository with specific timestamp
    repo_id = str(uuid.uuid4())
    unique_url = f"https://github.com/test/{repo_id}.git"
    repo = LegacyRepo(
        id=repo_id,
        url=unique_url,
        name="test-repo",
        owner="test",
        user_id="test-user",
        status=RepoStatus.COMPLETE,
        cloned_at=test_timestamp,
    )
    
    # Store in database
    db_session.add(repo)
    db_session.commit()
    
    # Retrieve from database
    retrieved = db_session.query(LegacyRepo).filter_by(id=repo_id).first()
    
    # Verify timestamp is preserved
    assert retrieved is not None, "Repository should be retrievable"
    assert retrieved.cloned_at is not None, "Timestamp should not be None"
    
    # Check that the timestamp represents the same moment in time
    # Allow small tolerance for database precision (microseconds)
    # SQLite stores timestamps as naive datetimes, so both should be naive
    assert retrieved.cloned_at.tzinfo is None or retrieved.cloned_at.tzinfo == test_timestamp.tzinfo, \
        "Timezone info should match"
    
    time_diff = abs((retrieved.cloned_at - test_timestamp).total_seconds())
    assert time_diff < 0.001, \
        f"Timestamp should be preserved (diff: {time_diff}s)"


@pytest.mark.property
@given(analysis_data=generate_analysis_result())
@settings(
    max_examples=100, 
    deadline=5000,
    suppress_health_check=[HealthCheck.function_scoped_fixture]
)
def test_analysis_timestamps_preserved(db_session, analysis_data):
    """
    Test that analysis result timestamps (created_at, updated_at) are preserved.
    
    Validates: Requirements 6.4
    
    For any analysis result, the created_at and updated_at timestamps should
    be preserved accurately during database round-trip.
    """
    # Create repository
    repo_id = str(uuid.uuid4())
    unique_url = f"https://github.com/test/{repo_id}.git"
    repo = LegacyRepo(
        id=repo_id,
        url=unique_url,
        name="test-repo",
        owner="test",
        user_id="test-user",
        status=RepoStatus.COMPLETE,
    )
    db_session.add(repo)
    db_session.commit()
    
    # Create analysis result
    analysis_id = str(uuid.uuid4())
    analysis = AnalysisResult(
        id=analysis_id,
        repo_id=repo_id,
        languages=analysis_data['languages'],
        frameworks=analysis_data['frameworks'],
        issues=analysis_data['issues'],
        tech_debt=analysis_data['tech_debt'],
        total_files=analysis_data['total_files'],
        total_lines=analysis_data['total_lines'],
    )
    
    # Store in database
    db_session.add(analysis)
    db_session.commit()
    
    # Record the timestamps
    original_created_at = analysis.created_at
    original_updated_at = analysis.updated_at
    
    # Retrieve from database
    retrieved = db_session.query(AnalysisResult).filter_by(id=analysis_id).first()
    
    # Verify timestamps are preserved
    assert retrieved is not None, "Analysis result should be retrievable"
    assert retrieved.created_at is not None, "created_at should not be None"
    assert retrieved.updated_at is not None, "updated_at should not be None"
    
    # Check that timestamps represent the same moments in time
    created_diff = abs((retrieved.created_at - original_created_at).total_seconds())
    updated_diff = abs((retrieved.updated_at - original_updated_at).total_seconds())
    
    assert created_diff < 0.001, \
        f"created_at should be preserved (diff: {created_diff}s)"
    assert updated_diff < 0.001, \
        f"updated_at should be preserved (diff: {updated_diff}s)"
