import Z5
import pytest
from Z3 import load_data

def test_correct_input():
    lst = load_data(r'C:\Users\user\Studia\Semestr VI\Testowanie gier\L6\Z5\test_data.txt')
    # lst = [(1255, 'MCCLV'), (195, 'CXCV'), (3891, 'MMMDCCCXCI'), (1749, 'MDCCXLIX'), (321, 'CCCXXI'), (1114, 'MCXIV'),
    #        (745, 'DCCXLV'), (2179, 'MMCLXXIX'), (715, 'DCCXV'), (2910, 'MMCMX')]
    for input, expected_output in lst:
        assert expected_output == Z5.printRoman(input)


def test_input_out_of_range():
    lst = [-100,0,4000,232332]
    for input in lst:
        with pytest.raises(ValueError):
            Z5.printRoman(input)


def test_wrong_type_input():
    lst = ['b',[],(),{},set()]
    for input in lst:
        with pytest.raises(TypeError):
            Z5.printRoman(input)
