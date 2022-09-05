def is_palindrome(text):
    refactored = ''.join(letter.lower() for letter in text if letter.isalnum())
    return refactored == refactored[::-1]


if __name__ == '__main__':
    assert is_palindrome("Eine güldne, gute Tugend: Lüge nie!")
    assert is_palindrome("Kobyła ma mały bok.")
    assert not is_palindrome("Something wrong")
