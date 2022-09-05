from urllib.request import urlopen
import re
from queue import PriorityQueue as Q
from bs4 import BeautifulSoup
from time import sleep


def crawl(start_page, distance, action, verbose=False):
    # Function performs breadth first traversing on websites starting from a given one and
    # going with specified depth. During this, on each page is performed action. I decided
    # to make this function as an iterator that dynamically evaluate following pages. It
    # enable tracking results while computation, which can take some time.
    adres = '([a-zA-Z]+.)*[a-zA-Z]+'
    automat = re.compile('http://' + adres)
    q = Q()
    q.put((0, start_page))
    all_pages = {start_page}
    while not q.empty():
        current_distance, current_page = q.get()
        try:
            with urlopen(current_page) as f:
                html = f.read()

            # Extracting text from html file
            soup = BeautifulSoup(html, features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '.'.join(chunk for chunk in chunks if chunk)[2:]

            # Providing raw text to given action
            results = action(text)

            if current_distance < distance:
                sub_pages = {url.group() for url in automat.finditer(html.decode('utf-8'))}
                for page in sub_pages - all_pages:
                    q.put((current_distance + 1, page))
                all_pages |= sub_pages
            yield (current_page, results)
            if verbose:
                print(current_distance, current_page)
        except Exception as err:
            if verbose:
                print("Error occurred while opening:" + current_page)
                print(err)


def remove_ugly_parts(sentence):
    # After checking results I found that parts within curly or square brackets mostly aren't part of the sentence,
    # but some meta text, I decided to remove them. I would use regex module but I wasn't sure how to find nested
    # brackets.
    def remove_brackets(text, bracket_type="[]"):
        new_s = ""
        in_brackets = 0
        for letter in text:
            if letter == bracket_type[0]:
                in_brackets += 1
            elif letter == bracket_type[1]:
                in_brackets -= 1
            elif in_brackets == 0:
                new_s += letter
        return new_s

    def remove_unwanted_characters(sentence, characters):
        return ''.join([letter for letter in sentence if letter not in characters])

    sentence = remove_brackets(sentence, "[]")
    sentence = remove_brackets(sentence, "{}")
    sentence = remove_unwanted_characters(sentence, "^")
    return sentence


def select(word):
    # Function is selecting all sentences containing certain word and cutting off some
    # ugly looking parts.
    # I don't know what more I could do with text not using some sort of artificial intelligence.
    def action(text):
        dot = re.findall(r"([^.]*?" + word + "[^.]*\.)", text)
        question = re.findall(r"([^.]*?" + word + "[^.]*\?)", text)
        exclamation = re.findall(r"([^.]*?" + word + "[^.]*\!)", text)
        with_python = dot + question + exclamation
        final = [remove_ugly_parts(sentence) for sentence in with_python]
        return final
    return action


def print_tuple(item, n):
    page, text = item
    print(repr(page))
    for sentence in text[:n]:
        print(sentence)


def count(word):
    # Action that counts number of occurrences of word in a given web text
    def action(text):
        items = re.findall(word, text)
        return len(items)

    return action


if __name__ == "__main__":
    n = 5


    # Experiment 1
    print("Experiment 1: \nsentences with word \"Python\" from wikipedia")
    start_page = "https://sites.google.com/cs.uni.wroc.pl/boehm/python_parsing"
    depth = 2
    it = crawl(start_page, depth, select("Python"), verbose=True)
    print_tuple(next(it), n)
    sleep(2)
    print_tuple(next(it), n)
    sleep(2)
    print_tuple(next(it), n)
    sleep(10)

    # # Experiment 1
    # print("Experiment 1: \nsentences with word \"Python\" from wikipedia")
    # start_page = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    # depth = 2
    # it = crawl(start_page, depth, select("Python"), verbose=False)
    # print_tuple(next(it), n)
    # sleep(2)
    # print_tuple(next(it), n)
    # sleep(2)
    # print_tuple(next(it), n)
    # sleep(10)

    # # Experiment 2
    # print("Experiment 2: \nsentences with word \"Covid\" from the guardian")
    # start_page = "https://www.theguardian.com/international"
    # depth = 2
    # it = crawl(start_page, depth, select("Covid"), verbose=False)
    # print_tuple(next(it), n)
    # print_tuple(next(it), n)
    # print_tuple(next(it), n)
    # sleep(10)
    #
    # # Experiment 3
    # print("Experiment 3: \ncounting words \"Python\" from python.org")
    # start_page = "https://www.python.org/"
    # depth = 3
    # it = crawl(start_page, depth, count("Python"), verbose=False)
    # while True:
    #     print(next(it))
