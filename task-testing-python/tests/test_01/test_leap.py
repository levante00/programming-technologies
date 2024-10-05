from simple_library_01.functions import is_leap
import pytest


def test_is_leap():
    assert True == is_leap(400 * 1)

    assert True == is_leap(400 * 2)

    assert True == is_leap(400 * 3)

    assert True == is_leap(400 * 4)
    # -------------------------------
    assert True == is_leap(400 + 4)

    assert True == is_leap(400 + 8)

    assert True == is_leap(400 + 12)

    assert True == is_leap(400 + 16)
    # -------------------------------
    assert False == is_leap(400 + 1)

    assert False == is_leap(400 + 2)

    assert False == is_leap(400 + 3)

    assert False == is_leap(400 + 5)
    # -------------------------------
    assert False == is_leap(100 * 5)

    assert False == is_leap(100 * 6)

    assert False == is_leap(100 * 7)

    assert False == is_leap(100 * 9)
    # -------------------------------
    year_out_of_range_error = "Year must be greater than 0"

    with pytest.raises(AttributeError) as error:
        assert is_leap(0)
    assert str(error.value) == year_out_of_range_error

    with pytest.raises(AttributeError) as error:
        assert is_leap(-400)
    assert str(error.value) == year_out_of_range_error

    with pytest.raises(AttributeError) as error:
        assert is_leap(-400 - 4)
    assert str(error.value) == year_out_of_range_error

    with pytest.raises(AttributeError) as error:
        assert is_leap(-100 * 5)
    assert str(error.value) == year_out_of_range_error
    # -------------------------------
