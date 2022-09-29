


def kompresja(tekst):
    # specification: function compress given text
    # input type: string
    # output type: list of tuples
    #              -> [(number_of_characters_in_a_row, character),(...),...]

    l = []
    if not tekst:
        return None
    current_element = [0,tekst[0]]
    for letter in tekst:
        if letter == current_element[1]:
            current_element[0]+=1
        else:
            l.append(tuple(current_element))
            current_element = [1,letter]
    l.append(tuple(current_element))
    return l

def dekompresja(tekst_skompresowany):
    # specification: function decompress given text
    # input type: list of tuples
    #              -> [(number_of_characters_in_a_row, character),(...),...]
    # output type: string
    return ''.join([val*letter for val, letter in tekst_skompresowany])
    

if __name__ == '__main__':
    d = {}
    print(type(d))