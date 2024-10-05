from simple_library_01.functions import add


def test_add():
    assert 4 == add(2, 2)

    assert 60 == add(-100, 160)
