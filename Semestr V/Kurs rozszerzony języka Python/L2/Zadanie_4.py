import numpy as np


def split_sentences(text):
    result = []
    partial_sentence = ""
    for letter in text:
        if letter in ".!?":
            result.append(partial_sentence + " " + letter)
            partial_sentence = ""
        else:
            partial_sentence += letter
    return result


def uprosc_zdanie(tekst, dl_slowa, liczba_slow):
    sentences = split_sentences(tekst)
    for sentence in sentences:
        sentence = sentence.split()
        sentence = [word for word in sentence if len(word) < dl_slowa]
        if len(sentence) > liczba_slow:
            chosen_positions = np.sort(np.random.choice(np.arange(len(sentence)), liczba_slow))
            sentence = [sentence[i] for i in chosen_positions]
        print(''.join([" " + word for word in sentence][1:]))


if __name__ == '__main__':
    tekst = """Podział peryklinalny inicjałów wrzecionowatych
    kambium charakteryzuje sie sciana podziałowa inicjowana
    w płaszczyznie maksymalnej."""
    print(tekst)
    uprosc_zdanie(tekst, 10, 5)
