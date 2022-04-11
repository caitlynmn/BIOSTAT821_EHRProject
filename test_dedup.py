"""Test dedup."""
import pytest

from dedup import is_in, dedup
from typing import TypeVar


def test_is_in():
    """Test is_in."""
    test_list = ["A", "D", 500, 60.78, [1, 2]]
    assert is_in(test_list, "D")
    assert is_in(test_list, 500)
    assert is_in(test_list, 60.78)
    assert is_in(test_list, [1, 2])


def test_bad_is_in():
    """Test bad is_in."""
    test_list = ["A", "D", 500, 60.78, [1, 2]]
    if not is_in(test_list, "E"):
        assert True
    if not is_in(test_list, 510):
        assert True
    if not is_in(test_list, 62.78):
        assert True
    if not is_in(test_list, [1, 3]):
        assert True


def test_dedup():
    """Test dedup."""
    test_list = ["A", "D", "A", 500, 60.78, [1, 2], 500]
    assert dedup(test_list) == ["A", "D", 500, 60.78, [1, 2]]
    test_list2 = [[6, 7], [5, 6], 120, 10, 120]
    assert dedup(test_list2) == [[6, 7], [5, 6], 120, 10]
