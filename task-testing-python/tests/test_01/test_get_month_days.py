from simple_library_01.functions import get_month_days
import pytest


def test_get_month_days():
    for month in range(1, 13):
        assert 30 == get_month_days(1930, month)

    assert 30 == get_month_days(1930, 13)

    assert 30 == get_month_days(1930, -1)

    assert 30 == get_month_days(1930, 0)
    # -------------------------------
    assert 28 == get_month_days(1931, 2)

    assert 29 == get_month_days(1932, 2)

    assert 28 == get_month_days(1933, 2)

    assert 29 == get_month_days(1940, 2)
    # -------------------------------
    for month in [4, 6, 9, 11]:
        assert 30 == get_month_days(1931, 4)

    # -------------------------------
    for month in [1, 3, 5, 7, 8, 12]:
        assert 31 == get_month_days(1931, month)
    # -------------------------------
    month_out_of_range_error = "Month should be in range [1-12]"

    with pytest.raises(AttributeError) as error:
        assert get_month_days(1931, 13)
    assert str(error.value) == month_out_of_range_error

    with pytest.raises(AttributeError) as error:
        assert get_month_days(1931, -1)
    assert str(error.value) == month_out_of_range_error

    with pytest.raises(AttributeError) as error:
        assert get_month_days(1931, 0)
    assert str(error.value) == month_out_of_range_error
