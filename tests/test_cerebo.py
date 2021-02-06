import pytest

from coinPrice.cerebro import range_splitter, splitted_ranges_in_list_of_tuple #, adding_numbers


def test_range_splitter():
    """this is a basic test"""
    expected = list(range(2, 102, 2))
    assert range_splitter(100, 0) == expected


def test_range_splitter_fails():
    """this tests that an exception was raised"""
    with pytest.raises(TypeError) as error:
        range_splitter("100", "0")
    assert str(error.value) == "unsupported operand type(s) for -: 'str' and 'str'"


@pytest.mark.parametrize(
    "rsl, expected",
    [("abc", [(0, "a", "b"), (1, "b", "c")]), ("123", [(0, "1", "2"), (1, "2", "3")])],
)
def test_splitted_ranges_in_list_of_tuple(rsl, expected):
    """this is a parametrized test that tests many values"""
    assert splitted_ranges_in_list_of_tuple(rsl) == expected

'''
@pytest.mark.parametrize(
    "a,b, expected",
    [(1, 2, 3), (-10, 10, 0)],
)
def test_adding_numbers(a, b, expected):
    assert adding_numbers(a, b) == expected
'''