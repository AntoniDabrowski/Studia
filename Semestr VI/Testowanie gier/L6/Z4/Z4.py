from math import sqrt,pow

def triangle(points):
    try:
        (x_1, y_1), (x_2, y_2), (x_3, y_3) = sorted(sorted(points, key=lambda t: t[0]), key=lambda t: t[1])
    except:
        raise ValueError

    # is it triangle
    if x_1 == x_2 == x_3 == 0 or y_1 == y_2 == y_3 == 0:
        is_not_triangle = True
    elif y_1 == y_3 != y_2 or y_1 == y_2 != y_3:
        is_not_triangle = False
    else:
        is_not_triangle = (x_2-x_1)/(y_2-y_1) == (x_3-x_1)/(y_3-y_1)

    if is_not_triangle:
        return 'To nie trójkąt'

    side_len = lambda x1,y1,x2,y2: sqrt(pow(x1-x2,2)+pow(y1-y2,2))
    sides = [side_len(x_1,y_1,x_2,y_2),side_len(x_2,y_2,x_3,y_3),side_len(x_1,y_1,x_3,y_3)]
    sides = sorted(sides)
    # print(sides)

    is_right_angled = pow(sides[0],2) + pow(sides[1],2) - pow(sides[2],2) < 0.01
    if is_right_angled:
        return 'Trójkąt prostokątny'

    if abs(sides[0]-sides[1]) < 0.01 and abs(sides[1]-sides[2]) < 0.01:
        if abs(sides[0]-sides[2]) < 0.01:
            return 'Trójkąt równoboczny'
        else:
            return 'Trójkąt równoramienny'
    elif (abs(sides[1]-sides[2]) < 0.01 and abs(sides[0]-sides[2]) < 0.01) or \
            (abs(sides[1]-sides[0]) < 0.01 and abs(sides[0]-sides[2]) < 0.01):
        return 'Trójkąt równoramienny'
    else:
        return 'Trójkąt różnoboczny'


if __name__ == '__main__':
    lst = [[(0,0),(0,1),(1,0)],
           [(1,1),(1,2),(2,1)],
           [(1,1),(1,3),(1+sqrt(3),2)],
           [(1,1),(1,2),(1,3)]]
    for l in lst:
        print(triangle(l))

