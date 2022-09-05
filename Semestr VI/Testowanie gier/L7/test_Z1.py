from unittest import mock
import pytest
from Z1 import CarDAO, Car
from collections import defaultdict as dd

input_1 = ([Car(),
           Car(dd(int, (('1970', 35000), ('1971', 54000), ('1972', 27200)))),
           Car(),
           Car()],
           (1,'1971','1972'))

input_2 = ([Car(),
           Car(dd(int, (('1970', 35000), ('1971', 54000), ('1972', 27200)))),
           Car(),
           Car()],
           (0,'1971','1972'))

input_3 = ([Car(),
           Car(dd(int, (('1970', 35000), ('1971', 54000), ('1972', 27200)))),
           Car(),
           Car()],
           (9,'1972','1972'))

input_4 = ([Car(),
           Car(),
           Car(dd(int, (('1970', 35000), ('1971', 54000), ('1972', 27200)))),
           Car()],
           (2,'1972','1970'))

@pytest.mark.parametrize("_input,expected", [(input_1, 81200),
                                             (input_2, 0),
                                             (input_3, 27200),
                                             (input_4, 0)])
@mock.patch('Z1.CarDAO.get_cars')
def test_findMileageBetweenYears(mock_get_cars, _input, expected):
    mock_get_cars.return_value = _input[0]
    records = CarDAO.findMileageBetweenYears(*_input[1])
    assert records == expected
