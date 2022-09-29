import numpy as np
import re
import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup


text = """Python is an interpreted high-level general-purpose programming language.
 Python is dynamically-typed and garbage-collected.
 Guido van Rossum began working on Python in the late 1980s, as a successor to the ABC programming language, and first released it in 1991 as Python 0.
[33] Python2?
 Python3 aaa!
 Python2 was discontinued with version2…
 Python consistently ranks as one of the most popular programming languages.
 13 Languages influenced by Python."""

def select(text, word):
    dot = re.findall(r"([^.]*?"+word+"[^.]*\.)",text)
    question = re.findall(r"([^.]*?"+word+"[^.]*\?)",text)
    exclamation = re.findall(r"([^.]*?"+word+"[^.]*\!)",text)
    return question+exclamation

def print_tuple(item):
    page, text = item
    print(repr(page))
    for sentence in text:
        print(sentence)

print_tuple(("none",select(text,"Python")))