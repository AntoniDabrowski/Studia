import Z1
import pytest


def test_correct_input():
    cls = Z1.cls()
    lst = ['jeden', 'dwa', 'jeden', 'trzy', 'dwa', 'cztery']
    s = 'dwa'
    assert ['jeden', 'jeden', 'trzy', 'cztery'] == cls.remove(lst, s)


def test_input_with_null():
    cls = Z1.cls()
    lst = ['jeden', 'dwa', 'jeden', 'trzy', 'dwa', None]
    s = 'dwa'
    assert ['jeden', 'jeden', 'trzy', None] == cls.remove(lst, s)


def test_error_catching():
    cls = Z1.cls()
    lst = None
    s = 'dwa'
    with pytest.raises(TypeError):
        cls.remove(lst, s)
