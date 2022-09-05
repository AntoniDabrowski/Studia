class cls:
    def __init__(self):
        pass

    @staticmethod
    def remove(lst, s):
        if lst is None:
            raise TypeError("Lista ma wartość None")
        return [element for element in lst if element is None or element != s]
