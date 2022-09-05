import Z4
import pytest
from math import sqrt


def test_correct_input():
    lst = [[(0,0),(0,1),(1,0)],
           [(1,1),(1,2),(2,1)],
           [(1,1),(1,3),(1+sqrt(3),2)],
           [(1,1),(1,2),(1,3)]]
    ans = ['Trójkąt prostokątny',
           'Trójkąt prostokątny',
           'Trójkąt równoboczny',
           'To nie trójkąt']
    for l, a in zip(lst,ans):
        assert a == Z4.triangle(l)

def test_parametric():
    for r in [-100,123.223,-1423,3242]:
        l = [(1,1),(1,2*r),(2*r,1)]
        assert 'Trójkąt prostokątny' == Z4.triangle(l)

def test_error_catching():
    with pytest.raises(ValueError):
        Z4.triangle([(1,2),(0,2),(0,1),(0,0)])
