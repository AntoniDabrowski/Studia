import numpy as np
import re
import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup
import spacy


url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

for script in soup(["script", "style"]):
    script.extract()

text = soup.get_text()
lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = '. '.join(chunk for chunk in chunks if chunk)[1:]
# for i, sentence in enumerate(nltk.tokenize.sent_tokenize(text)):
#     s = re.findall(r"([^.]*?Python[^.]*\.)",sentence)
#     for k in s:
#         print(k)


nlp = spacy.load("en_core_web_sm")

tokens = nlp(text)

for sent in tokens.sents:
    print(sent.string.strip())