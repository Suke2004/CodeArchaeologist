"""
Simple test to verify Hypothesis is properly configured and working.
This test can be removed after confirming the setup is correct.
"""

import pytest
from hypothesis import given, strategies as st


@pytest.mark.property
def test_hypothesis_basic_setup():
    """
    Verify that Hypothesis is installed and basic functionality works.
    This is a simple sanity check test.
    """
    # Simple assertion that should always pass
    assert True


@pytest.mark.property
@given(st.integers())
def test_hypothesis_integer_generation(x):
    """
    Verify that Hypothesis can generate integers and run property tests.
    Property: Any integer should be equal to itself.
    """
    assert x == x


@pytest.mark.property
@given(st.text())
def test_hypothesis_text_generation(s):
    """
    Verify that Hypothesis can generate text strings.
    Property: The length of any string should be non-negative.
    """
    assert len(s) >= 0


@pytest.mark.property
@given(st.lists(st.integers()))
def test_hypothesis_list_generation(lst):
    """
    Verify that Hypothesis can generate lists.
    Property: Reversing a list twice should return the original list.
    """
    assert list(reversed(list(reversed(lst)))) == lst


@pytest.mark.property
@given(st.integers(min_value=0, max_value=100), st.integers(min_value=0, max_value=100))
def test_hypothesis_multiple_arguments(a, b):
    """
    Verify that Hypothesis can generate multiple arguments.
    Property: Addition is commutative.
    """
    assert a + b == b + a
