def kompresja(tekst):
    # specification: function compress given text
    # input type: string
    # output type: list of tuples
    #              -> [(number_of_characters_in_a_row, character),(...),...]

    l = []
    if not tekst:
        return None
    current_element = [0, tekst[0]]
    for letter in tekst:
        if letter == current_element[1]:
            current_element[0] += 1
        else:
            l.append(tuple(current_element))
            current_element = [1, letter]
    l.append(tuple(current_element))
    return l


def dekompresja(tekst_skompresowany):
    # specification: function decompress given text
    # input type: list of tuples
    #              -> [(number_of_characters_in_a_row, character),(...),...]
    # output type: string
    return ''.join([val * letter for val, letter in tekst_skompresowany])


if __name__ == '__main__':
    print(kompresja("suuuper"))
    print(dekompresja(kompresja("suuuper")))

    # If you want to check my program for larger text, download from SKOS file Brave_New_World.txt,
    # place it in the same folder as this python file and run code below.
    # Book was downloaded from:
    # https://archive.org/stream/ost-english-brave_new_world_aldous_huxley/Brave_New_World_Aldous_Huxley_djvu.txt

    brave_new_world = ''.join([line for line in open(r"Brave_New_World.txt")])
    assert dekompresja(kompresja(brave_new_world)) == brave_new_world
