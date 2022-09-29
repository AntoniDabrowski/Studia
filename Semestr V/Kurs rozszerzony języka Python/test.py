import decimal as d

def vat_faktura(l):
    return d.Decimal(0.23) * sum(l)

def vat_paragon(l):
    return sum([d.Decimal(0.23) * x for x in l])


if __name__ == '__main__':
    print(isinstance(d.Decimal('0.2'),d.Decimal))