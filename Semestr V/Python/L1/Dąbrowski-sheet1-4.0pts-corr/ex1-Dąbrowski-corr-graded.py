from decimal import Decimal


def vat_faktura(l):
    if l and isinstance(l[0], Decimal):
        return sum(l) * Decimal(0.23)
    return sum(l) * 0.23


def vat_paragon(l):
    if l and isinstance(l[0], Decimal):
        return sum([x * Decimal(0.23) for x in l])
    return sum([x * 0.23 for x in l])


if __name__ == '__main__':
    zakupy = [0.2, 0.5, 4.59, 6]
    print(vat_faktura(zakupy) == vat_paragon(zakupy))
    print(vat_faktura(zakupy))
    print(vat_paragon(zakupy))

    zakupy = list(map(Decimal, '0.2 0.5 4.59 6'.split()))
    print(vat_faktura(zakupy) == vat_paragon(zakupy))
    print(vat_faktura(zakupy))
    print(vat_paragon(zakupy))

    # Didactic notes:
    s = sum(zakupy)
    print(s)
    print(s * Decimal('0.23'))
    print(s == vat_faktura(zakupy))

    # Grade: 0.5

    # Contains:
    # 1. The bare minimum solution.
    # Deducted points for:
    # 1. No comments about what the code does. Why is it working for decimal and not for floats?
    # 2. Did not think about why are you getting "2.596700000000000112809761532" even in the decimal solution
    #    => which is actually due to an error in the homework.
    # 3. (Less of an issue for HW1) Only tested the sample input, didn't even try to run any further tests.
