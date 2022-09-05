def is_palindrom(text):
    refactored = ''.join(letter.lower() for letter in text if letter.isalnum())
    return refactored == refactored[::-1]


if __name__ == '__main__':
    assert is_palindrom("Eine güldne, gute Tugend: Lüge nie!")
    assert is_palindrom("Kobyła ma mały bok.")
    assert not is_palindrom("Something wrong")

# Grade: 1.5

# Didactic notes:
# Solution seems to work, but there is no discussion about what languages it supports,
# or what happens with let's say sharfes S in German.

# Also, a few more tests would be nice too.
