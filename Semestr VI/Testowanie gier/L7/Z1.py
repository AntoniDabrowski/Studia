from collections import defaultdict as dd
import gc


class Car:
    general_id = 0
    def __init__(self,YearMileage = dd(int)):
        self.id = Car.general_id
        self.YearMileage = YearMileage
        Car.general_id += 1

class CarDAO:
    def __init__(self):
        self.cars = []

    @staticmethod
    def get_cars(i):
        return [obj for obj in gc.get_objects() if isinstance(obj, Car)]

    @staticmethod
    def findMileageBetweenYears(car_id,startYear,endYear):
        for obj in CarDAO.get_cars(0):
            if obj.id == car_id:
                s = 0
                for k,v in obj.YearMileage.items():
                    if int(k) >= int(startYear) and int(k) <= int(endYear):
                        s += v
                return s
        return 0

if __name__ == '__main__':
    c1 = Car(dd(int,(('1970',35000),('1971',54000),('1972',27200))))
    c2 = Car()
    c3 = Car()
    c4 = Car()
    print(CarDAO.findMileageBetweenYears(0,'1971','1972'))