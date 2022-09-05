# from Z2 import Event, Calendar
# import pytest
#
#
# def test_correct_input():
#     events = [Event('Meeting_1',9,12),
#               Event('Lunch',12,12.5),
#               Event('Nap',12.5,13),
#               Event('Meeting_2',13.5,15.5),
#               Event('Dinner',12,12.5)]
#     to_edit = [Event('Meeting_1',9,11),
#                Event('Meeting_2',14,15)]
#     cal = Calendar()
#     for event in events:
#         cal.add_event(event)
#     for event in to_edit:
#         cal.edit_event(event.name,event)
#     for event in events:
#         cal.remove_event(event.name)
# test_correct_input()
#
# # def test_parametric():
# #     for r in [-100,123.223,-1423,3242]:
# #         l = [(1,1),(1,2*r),(2*r,1)]
# #         assert 'Trójkąt prostokątny' == Z4.triangle(l)
# #
# # def test_error_catching():
# #     with pytest.raises(ValueError):
# #         Z4.triangle([(1,2),(0,2),(0,1),(0,0)])
