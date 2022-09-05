def printRoman(number):
    if type(number) != int:
        raise TypeError
    if number >= 4000 or number <= 0:
        raise ValueError("Podaj liczbę z zakresu (0,4000)")
    num = [1, 4, 5, 9, 10, 40, 50, 90,
           100, 400, 500, 900, 1000]
    sym = ["I", "IV", "V", "IX", "X", "XL",
           "L", "XC", "C", "CD", "D", "CM", "M"]
    i = 12
    result = []
    while number:
        div = number // num[i]
        number %= num[i]

        while div:
            result.append(sym[i])
            div -= 1
        i -= 1
    return ''.join(result)


if __name__ == "__main__":
    from random import randint
    lst = []
    for _ in range(10):
        rand = randint(1,3999)
        result = printRoman(rand)
        lst.append((rand,result))
    print(repr(lst))
