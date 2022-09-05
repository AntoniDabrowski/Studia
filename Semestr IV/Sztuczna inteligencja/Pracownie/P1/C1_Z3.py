import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import TweetTokenizer
import nltk


def tokenize():
    with open("Pan_Tadeusz_prawdziwy.txt", 'r', encoding='UTF-8') as input_file, open(
            "Pan_Tadeusz_prawdziwy_znormalizowany.txt", 'w', encoding="UTF-8") as output_file:
        for i, line in enumerate(input_file):
            if line != "\n":
                tokenizer = nltk.RegexpTokenizer(r"\w+")
                new_words = tokenizer.tokenize(line)
                output_file.write(''.join(num.lower() + " " if l < len(new_words) - 1 else num.lower() for l, num in
                                          enumerate(new_words)) + "\n")


def compare(file_1, file_2):
    first = [line for line in open(file_1, 'r', encoding='UTF-8')]
    second = [line for line in open(file_2, 'r', encoding='UTF-8')]
    equal, different = 0, 0
    for line_1, line_2 in zip(first, second):
        if line_1 == line_2:
            equal += 1
        else:
            different += 1
    return equal / (different + equal)


if __name__ == "__main__":
    print(compare("Pan_Tadeusz_ze_spacjami.txt", "Pan_Tadeusz_prawdziwy_znormalizowany.txt"))
    print(compare("Pan_Tadeusz_losowy.txt", "Pan_Tadeusz_prawdziwy_znormalizowany.txt"))
