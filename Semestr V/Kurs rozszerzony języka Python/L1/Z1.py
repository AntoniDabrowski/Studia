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
